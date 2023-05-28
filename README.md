# What It Is

Sublime Text plugin to do simple render to html with styles and highlights, primarily for printing.

Built for ST4 on Windows.

- Line wrap with optional line numbers.
- Version to render markdown file to html using [Markdeep](https://casual-effects.com/markdeep/).
- Note that relative links (like graphics) are currently broken. If it's important, you should manually copy them to the temp directory.
- The setting `highlight_scopes` should match [SbotHighlight](https://github.com/cepthomas/SbotHighlight) if you are using it. The defaults are just a wild guess and need to be customized.


## Commands

| Command                    | Implementation | Description                          | Args                                  |
| :--------                  | :-------       | :-------                             | :-----                                |
| sbot_render_to_html        | Context        | Render current file                  | line_numbers = include line numbers   |
| sbot_render_markdown       | Context        | Render current markdown file to html |                                       |

## Settings

| Setting              | Description                              | Options                                                               |
| :--------            | :-------                                 | :------                                                               |
| sel_all              | Selection default                        | if true and no user selection, assumes the whole document (like ST)   |
| html_font_face       | For rendered html                        | font name - usually monospace                                         |
| html_font_size       | For rendered html/markdown               | point size                                                            |
| html_background      | Background olor                          | color name                                                            |
| output               | Where to render to                       | clipboard OR file (fn/temp + .html) OR show (in browser)              |
| max_file             | Max file size to render                  | in Mb                                                                 |
| highlight_scopes     | List of up to 6 scope names for commands |                                                                       |
