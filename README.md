# What It Is
Sublime Text plugin to do simple render to html with styles, primarily for printing.

- Line wrap with optional line numbers.
- Version to render markdown file to html using [Markdeep](https://casual-effects.com/markdeep/).
- Note that relative links (like graphics) are currently broken. If it's important, you can manually copy them to the temp directory.

Built for Windows and ST4. Other OSes and ST versions will require some hacking.

## Commands
| Command                  | Implementation | Description |
|:--------                 |:-------        |:-------     |
| sbot_render_to_html      | Context        | Render current open file including scope colors and highlights to html, arg is include line numbers |
| sbot_render_markdown     | Context        | Render current open markdown file to html |

## Settings
| Setting                  | Description |
|:--------                 |:-------     |
| sel_all                  | Option for selection defaults: if true and no user selection, assumes the whole document (like ST) |
| html_font_face           | For rendered html - usually monospace |
| html_md_font_face        | For rendered markdown - usually prettier than html_font_face |
| html_font_size           | For rendered html/markdown |
| html_background          | Color name if you need to change the bg color (not done automatically from color scheme) |
| render_output            | Where to render to.<br/>`'clipboard'`<br/>`'file'` fn/temp + .html<br/>`'show'`in browser |
| render_max_file          | Max file size in Mb to render |
