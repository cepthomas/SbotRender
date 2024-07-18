import os
import math
import textwrap
import pathlib
import webbrowser
import html
import sublime
import sublime_plugin
from . import sbot_common as sc


RENDER_SETTINGS_FILE = "SbotRender.sublime-settings"


#-----------------------------------------------------------------------------------
class SbotRenderToHtmlCommand(sublime_plugin.TextCommand):
    ''' Make a pretty. '''

    _rows = 0
    _row_num = 0
    _line_numbers = False

    def run(self, edit, line_numbers=False):
        ''' Go. '''
        self._line_numbers = line_numbers
        settings = sublime.load_settings(RENDER_SETTINGS_FILE)

        max_file = settings.get('max_file')
        fsize = self.view.size() / 1024.0 / 1024.0
        if fsize > max_file:
            sublime.message_dialog('File too large to render. If you really want to, change your settings')
        else:
            self._do_render()
            # Actually would like to run in a thread but takes 10x time, probably the GIL.
            # t = threading.Thread(target=self._do_render)
            # t.start()

    def _update_status(self):
        ''' Runs in main thread. '''
        if self._row_num == 0:
            self.view.set_status('render', 'Render setting up')
            sublime.set_timeout(self._update_status, 100)
        elif self._row_num >= self._rows:
            self.view.set_status('render', 'Render done')
        else:
            if self._rows % 100 == 0:
                self.view.set_status('render', f'Render {self._row_num} of {self._rows}')

            sublime.set_timeout(self._update_status, 100)

    def _do_render(self):
        '''
        The worker thread. (not)
        html render msec per line:
          - medium (5000 dense lines) 1.25
          - small (1178 sparse lines) 0.40
          - biggish (20616 dense lines = 3Mb) 1.36
        '''

        # Get prefs.
        settings = sublime.load_settings(RENDER_SETTINGS_FILE)
        html_background = settings.get('html_background')

        # Collect scope/style info. Styles will be turned into html styles.
        all_styles = {}  # k:style v:id
        region_styles = []  # One [(Region, style)] per line
        highlight_regions = []  # (Region, style))

        self._rows, _ = self.view.rowcol(self.view.size())
        self._row_num = 0

        # Local helpers.
        def _add_style(style):
            # Add style to our collection.
            if style not in all_styles:
                all_styles[style] = len(all_styles)

        def _get_style(style):
            # Locate the style and return the id.
            return all_styles.get(style, -1)

        def _view_style_to_tuple(view_style):
            tt = (view_style['foreground'],
                  view_style.get('background', None),
                  view_style.get('bold', False),
                  view_style.get('italic', False),
                  view_style.get('underline', False))
            return tt

        # Start progress.
        sublime.set_timeout(self._update_status, 100)

        # If there are SbotHighlight highlights, collect them.
        hl_info = sc.get_highlight_info('all')

        for hl in hl_info:
            ss = self.view.style_for_scope(hl.scope_name)
            background = ss['background'] if 'background' in ss else None
            foreground = ss['foreground'] if 'foreground' in ss else None
            hl_style = (foreground, background, False, False, False)
            _add_style(hl_style)

            # Assign style to the highlight regions.
            for region in self.view.get_regions(hl.region_name):
                highlight_regions.append((region, hl_style))

        # Put all regions in order.
        highlight_regions.sort(key=lambda r: r[0].a)

        # Tokenize selection by syntax scope.
        # pc = SbotPerfCounter('render_html')
        settings = sublime.load_settings(RENDER_SETTINGS_FILE)
        for region in sc.get_sel_regions(self.view, settings):
            for line_region in self.view.split_by_newlines(region):
                # pc.start()
                self._row_num += 1

                line_styles = []  # (Region, style))

                # Start a new line.
                current_style = None
                current_style_start = line_region.a  # current chunk

                # Process the individual line chars.
                point = line_region.a

                while point < line_region.b:
                    # Check if it's a highlight first as they take precedence.
                    if len(highlight_regions) > 0 and point >= highlight_regions[0][0].a:
                        # Start a highlight.
                        new_style = highlight_regions[0][1]

                        # Save last maybe.
                        if point > current_style_start:
                            line_styles.append((sublime.Region(current_style_start, point), current_style))

                        # Save highlight info.
                        line_styles.append((highlight_regions[0][0], new_style))

                        _add_style(new_style)

                        # Bump ahead.
                        point = highlight_regions[0][0].b
                        current_style = new_style
                        current_style_start = point

                        # Remove from the list.
                        del highlight_regions[0]
                    else:
                        # Plain ordinary style. Did it change?
                        new_style = _view_style_to_tuple(self.view.style_for_scope(self.view.scope_name(point)))

                        if new_style != current_style:
                            # Save last chunk maybe.
                            if point > current_style_start:
                                line_styles.append((sublime.Region(current_style_start, point), current_style))

                            current_style = new_style
                            current_style_start = point

                            _add_style(new_style)

                        # Bump ahead.
                        point += 1

                # Done with this line. Save last chunk maybe.
                if point > current_style_start:
                    line_styles.append((sublime.Region(current_style_start, point), current_style))

                # Add to master list.
                region_styles.append(line_styles)
                # pc.stop()

        # Done all lines.

        # Create css.
        style_text = ""
        for style, stid in all_styles.items():
            props = f'{{ color:{style[0]}; '
            if style[1] is not None:
                props += f'background-color:{style[1]}; '
            if style[2]:
                props += 'font-weight:bold; '
            if style[3]:
                props += 'font-style:italic; '
            if style[4]:
                props += 'text-decoration:underline; '
            props += '}'
            style_text += f'            .st{stid} {props}\n'

        # Content text.
        content = []
        line_num = 1

        # Iterate collected lines.
        gutter_size = math.ceil(math.log(len(region_styles), 10))
        padding1 = 1.4 + gutter_size * 0.5
        padding2 = padding1

        for line_styles in region_styles:
            # Start line.
            content.append(f'            <p>{line_num:0{gutter_size}} ' if self._line_numbers else f'            <p>')

            if len(line_styles) == 0:
                content.append('<br>')
            else:
                for region, style in line_styles:
                    #[(Region, style(ref))]
                    text = self.view.substr(region)

                    # Locate the style.
                    stid = _get_style(style)
                    content.append(f'<span class=st{stid}>{html.escape(text)}</span>' if stid >= 0 else text)

            # Done line.
            content.append('</p>\n')
            line_num += 1

        # Give it a name.
        name = self.view.name()
        if (name is None or name == '') and self.view.file_name() is not None:
            name = os.path.basename(os.path.splitext(self.view.file_name())[0])
        if (name is None or name == ''):
            name = 'temp'

        # Output html.
        html1 = f'''
<!doctype html>
<html lang="en">
    <head>
        <title>{name}</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style  type="text/css">
            .contentpane {{ font-family: {settings.get('html_font_face')}; font-size: {settings.get('html_font_size')}; background-color: {html_background}; text-indent: -{padding1}em; padding-left: {padding2}em; }}
            p {{ white-space: pre-wrap; margin: 0em; }}
'''

        html2 = '''
        </style>
    </head>
    <body>
        <div class="container">
        <div class="contentpane">
'''

        html3 = '''
        </div>
        </div>
    </body>
</html>
'''
        _gen_html(self.view.file_name(), [html1, style_text, html2, ''.join(content), html3])


#-----------------------------------------------------------------------------------
class SbotRenderMarkdownCommand(sublime_plugin.TextCommand):
    ''' Turn md into html.'''

    def is_visible(self):
        return self.view.settings().get('syntax') == 'Packages/Markdown/Markdown.sublime-syntax'

    def run(self, edit):
        # Get prefs.
        settings = sublime.load_settings(RENDER_SETTINGS_FILE)
        md_render_css = settings.get('md_render_css')

        css_file = md_render_css \
            if md_render_css is not None and len(md_render_css) > 0 \
            else os.path.join(sublime.packages_path(), "SbotRender", "md_render.css")

        html = []
        html.append("<meta charset=\"utf-8\">")
        # html.append("<style class=\"fallback\">body{visibility:hidden}</style>")
        html.append(f"<link rel=\"stylesheet\" href=\"{css_file}?\">")

        for region in sc.get_sel_regions(self.view, settings):
            html.append(self.view.substr(region))

        html.append("<!-- Markdeep: --><style class=\"fallback\">body{visibility:hidden;white-space:pre}</style><script src=\"markdeep.min.js\" charset=\"utf-8\"></script><script src=\"https://casual-effects.com/markdeep/latest/markdeep.min.js\" charset=\"utf-8\"></script><script>window.alreadyProcessedMarkdeep||(document.body.style.visibility=\"visible\")</script>")
        _gen_html(self.view.file_name(), html)


#-----------------------------------------------------------------------------------
def _gen_html(fn, content):
    ''' Common html file output generator. '''

    s = "========== NO CONTENT ==========" if content is None else ''.join(content)

    settings = sublime.load_settings(RENDER_SETTINGS_FILE)
    prompt = settings.get('prompt')
    save_fn = os.path.basename(fn) + '.html'

    def _on_save_file(fn):
        with open(fn, 'w', encoding='utf-8') as f:  # need to explicitly set encoding because default windows is ascii
            f.write(s)
        webbrowser.open_new_tab(fn)

    if prompt:
        # print(f'save_fn:{save_fn}')
        sublime.save_dialog(_on_save_file, directory=os.path.dirname(fn), name=save_fn)
        # sublime.save_dialog(_on_save_file, file_types=[('Html File', ['*.html'])], directory=os.path.dirname(fn), name=save_fn, extension='.html')
    else:
        _on_save_file(fn + '.html')
