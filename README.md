# Sbot Render

Sublime Text plugin to do simple render to html with styles and highlights.

Built for ST4 on Windows and Linux.

- Useful for printing in full color. First render to html, then print from browser.
- Compatible with [SbotHighlight](https://github.com/cepthomas/SbotHighlight) (recommended) and
  [Notr](https://github.com/cepthomas/Notr).
- Line wrap with optional line numbers.
- Version to render markdown file to html using [Markdeep](https://casual-effects.com/markdeep/).
- Note that relative links (like graphics) are currently broken. If it's important, you should manually copy them to the work directory.

## Commands

See `Context.sublime-menu` for usage.

| Command                    | Type     | Description                          | Args                                       |
| :--------                  | :------- | :-------                             | :-----                                     |
| sbot_render_to_html        | Context  | Render current file to html          | line_numbers:T/F                           |
| sbot_render_markdown       | Context  | Render current markdown file to html |                                            |


## Settings

| Setting              | Description                       | Options                              |
| :--------            | :-------                          | :------                              |
| html_font_face       | For rendered html                 | font name - usually monospace        |
| html_font_size       | For rendered html/markdown        | point size                           |
| html_background      | Background olor                   | color name                           |
| md_render_css        | Optional css style                |                                      |
| prompt               | Ask for a render file name        | T/F                                  |
| max_file             | Max file size to render           | in Mb                                |
| log_level            | Min level to log                  | CRITICAL ERROR WARNING INFO DEBUG    |

## Colors

New scopes have been added to support this application. Adjust these to taste and add
to your `Packages\User\your.sublime-color-scheme` file. Note that these are shared with other
members of the sbot family.

```
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
