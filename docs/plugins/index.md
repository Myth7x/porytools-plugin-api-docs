# Plugins

PoryTools plugins are folders of Lua code that the IDE loads at
startup. A plugin can add a menu entry, a keyboard shortcut, and one
or more dockable panels — and from inside its code it can read,
search, and rewrite files in the open project.

## Anatomy of a plugin

```
my-plugin/
├── manifest.json     -- metadata (name, hotkey, entry script)
└── plugin.lua        -- the code; must define a `run()` function
```

That's the minimum. Larger plugins typically split the Lua across
multiple files; see [Multi-file plugins](multi-file.md) for how.

### `manifest.json`

A small JSON file telling the IDE what to call your plugin and how to
launch it. The full field list is on the [Manifest](manifest.md)
page; here's a representative example:

```json
{
  "name": "My Plugin",
  "description": "Does something cool.",
  "version": "1.0.0",
  "author": "you",
  "entry": "plugin.lua",
  "command": "run",
  "hotkey": "Ctrl+Alt+M",
  "menu": "Tools"
}
```

### `plugin.lua`

Whatever your `command` field names (default: `run`) must be a global
function. The IDE calls it every time the user clicks your menu entry
or presses your hotkey.

```lua
function run()
  pt.ui.alert("Hello from a PoryTools plugin!")
end
```

## How loading works

1. On startup the IDE scans the [plugins folder](#where-plugins-live)
   for sub-directories.
2. Each sub-directory's `manifest.json` is parsed.
3. The entry script is executed inside a fresh sandbox — every plugin
   gets its own `sol::environment`, so your globals don't leak into
   anyone else's.
4. The IDE adds a menu entry for the plugin under **Plugins** (or
   under a submenu if `manifest.menu` is set).
5. When the user clicks it, the IDE calls your `command` function.

**You can reload at any time** with **Plugins → Reload Plugins**.
That wipes every plugin environment, re-scans the directory, and
re-evaluates each plugin's entry script — no IDE restart needed.

## Where plugins live { #where-plugins-live }

| Platform | Path |
| -------- | ---- |
| Windows  | `%APPDATA%\PoryTools\PoryTools\plugins\` |
| Linux    | `~/.local/share/PoryTools/PoryTools/plugins/` |
| macOS    | `~/Library/Application Support/PoryTools/PoryTools/plugins/` |

You can open the folder straight from the IDE: **Plugins → Open
Plugins Folder…**.

## The `pt` table

All host-provided functions live under one global table called `pt`,
grouped into six modules:

<div class="grid cards" markdown>

-   :material-pencil-box-outline:{ .lg .middle } **[`pt.editor`](api/editor.md)**

    ---

    The active editor buffer — read text, set the cursor, replace
    selections, find and replace, save.

-   :material-tab:{ .lg .middle } **[`pt.tabs`](api/tabs.md)**

    ---

    Open, close, and enumerate editor tabs.

-   :material-file-document:{ .lg .middle } **[`pt.file`](api/file.md)**

    ---

    Read, write, copy, rename and list files on disk. Grep-style
    recursive search.

-   :material-folder-search:{ .lg .middle } **[`pt.project`](api/project.md)**

    ---

    The open project — root path, file enumeration.

-   :material-application:{ .lg .middle } **[`pt.ui`](api/ui.md)**

    ---

    Native dialogs (alert, confirm, prompt, file picker) and the
    dockable widget system.

-   :material-keyboard-return:{ .lg .middle } **[`pt.cmd`](api/cmd.md)**

    ---

    Wrappers over IDE menu commands (save, undo, redo).

</div>

## Lua standard library

The following Lua 5.4 standard libraries are loaded in every plugin's
sandbox:

`base` · `string` · `table` · `math` · `os` · `io` · `package`

`debug` and `coroutine` are intentionally not exposed.

## Where to go next

- [Quickstart](quickstart.md) — a "Hello, plugin" in 30 seconds.
- [Multi-file plugins](multi-file.md) — splitting a larger plugin.
- [Cookbook](cookbook.md) — copy-paste recipes for common patterns.
- [Example plugins](examples.md) — annotated walkthroughs of the
  example folders bundled with the repo.
