# Render View

Sublime Text plugin renders the text in a view to html with all scheme colors.

The primary purpose is for wysiwyg printing in full color: first render to html, then print from the browser.

Built for ST4 on Windows and Linux.


## Features

- Lines wrap properly.
- Line numbers are optional.
- If the text is markdown, renders to html using [Markdeep](https://casual-effects.com/markdeep/).
  There is a basic default style or specify a custom css file.
- Note that relative links (like graphics) are currently unsupported. If it's important, they can be
  manually copied to the output directory.
- Supports scheme colors from [Highlight Token](https://github.com/cepthomas/SbotHighlight) (recommended)
  and [Notr](https://github.com/cepthomas/Notr).


## Commands and Menus

| Command                    | Description                          | Args                        |
| :--------                  | :-------                             | :-----                      |
| sbot_render_to_html        | Render current file to html          | line_numbers:true OR false  |
| sbot_render_markdown       | Render current markdown file to html |                             |

There is no default `Context.sublime-menu` file in this plugin.
Add the commands you like to your own `User\Context.sublime-menu` file. Typical entries are:
``` json
{ "caption": "Render",
    "children":
    [
        { "caption": "Html", "command": "sbot_render_to_html", "args" : { "line_numbers": false } },
        { "caption": "Html + Lines", "command": "sbot_render_to_html", "args" : { "line_numbers": true } },
        { "caption": "Markdown", "command": "sbot_render_markdown" },
    ]
}
```


## Settings

| Setting         | Description                | Options                                 |
| :--------       | :-------                   | :------                                 |
| html_font_face  | For rendered html          | font name - usually monospace           |
| html_font_size  | For rendered html/markdown | point size                              |
| html_background | Background color           | color name                              |
| max_file        | Max file size to render    | in Mb                                   |
| md_css          | Optional css file for md   |                                         |
| output_dir      | Output dir for rendered files - if null asks user for a file name. | |


## Colors

New scopes have been added to support this application. Adjust these to taste and add
to your `Packages\User\your.sublime-color-scheme` file.  Note that these are also used by other
members of the sbot family.

``` json
{ "scope": "markup.user_hl1", "background": "red", "foreground": "white" },
{ "scope": "markup.user_hl2", "background": "green", "foreground": "white" },
{ "scope": "markup.user_hl3", "background": "blue", "foreground": "white" },
{ "scope": "markup.user_hl4", "background": "yellow", "foreground": "black" },
{ "scope": "markup.user_hl5", "background": "lime", "foreground": "black" },
{ "scope": "markup.user_hl6", "background": "cyan", "foreground": "black" },
{ "scope": "markup.fixed_hl1", "background": "gainsboro", "foreground": "red" },
{ "scope": "markup.fixed_hl2", "background": "gainsboro", "foreground": "green" },
{ "scope": "markup.fixed_hl3", "background": "gainsboro", "foreground": "blue" },
```
