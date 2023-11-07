# What It Is

Sublime Text plugin to do simple render to html with styles and highlights, primarily for printing.

Built for ST4 on Windows.

- Line wrap with optional line numbers.
- Version to render markdown file to html using [Markdeep](https://casual-effects.com/markdeep/).
- Note that relative links (like graphics) are currently broken. If it's important, you should manually copy them to the temp directory.


## Commands

| Command                    | Type     | Description                          | Args                                       |
| :--------                  | :------- | :-------                             | :-----                                     |
| sbot_render_to_html        | Context  | Render current file                  | line_numbers: true include line numbers    |
| sbot_render_markdown       | Context  | Render current markdown file to html |                                            |

## Settings

| Setting              | Description                              | Options                                                               |
| :--------            | :-------                                 | :------                                                               |
| sel_all              | Selection default                        | if true and no user selection, assumes the whole document (like ST)   |
| html_font_face       | For rendered html                        | font name - usually monospace                                         |
| html_font_size       | For rendered html/markdown               | point size                                                            |
| html_background      | Background olor                          | color name                                                            |
| output               | Where to render to                       | path or "clipboard"                                                   |
| max_file             | Max file size to render                  | in Mb                                                                 |

## Colors
You need to supply something like these in your sublime-color-scheme file:
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
These work for all members of the sbot family.
See [Color customization](https://www.sublimetext.com/docs/color_schemes.html#customization).
