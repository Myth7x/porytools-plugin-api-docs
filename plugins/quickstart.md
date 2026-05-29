# Quickstart

Build a plugin from scratch in under a minute. By the end you'll have
a working **Plugins → Hello → Say hi** menu entry that prompts for
your name and writes a friendly message into the active editor.

## 1. Make the folder

Open the plugins folder from the IDE:

**Plugins → Open Plugins Folder…**

Create a new sub-folder called `hello`. The exact name doesn't matter
— it just has to be unique among your plugins.

## 2. Write `manifest.json`

Drop this file at `hello/manifest.json`:

```json
{
  "name": "Say hi",
  "description": "Inserts a greeting at the cursor.",
  "version": "0.1.0",
  "entry": "plugin.lua",
  "command": "run",
  "menu": "Hello"
}
```

The fields you'll touch most often:

- `name` — what the user sees in the **Plugins** menu.
- `entry` — the Lua file to load (default: `plugin.lua`).
- `command` — the name of the global function the IDE calls (default: `run`).
- `menu` — optional submenu under **Plugins**. Plugins without a menu
  end up at the top level.

The full reference is on the [Manifest](manifest.md) page.

## 3. Write `plugin.lua`

```lua
-- plugin.lua
function run()
  local name = pt.ui.prompt("What's your name?", "world")
  if not name then return end                     -- user cancelled

  local greeting = string.format("-- hello, %s!\n", name)
  pt.editor.replaceSelection(greeting)

  pt.ui.notify("Inserted greeting for " .. name)
end
```

What's happening:

1. `pt.ui.prompt` opens a modal text input. The default is `"world"`
   so the user just has to hit Enter to accept it. `nil` comes back
   when the user clicks Cancel.
2. `pt.editor.replaceSelection` overwrites whatever is currently
   selected in the active editor with your string. If nothing is
   selected, it inserts at the cursor.
3. `pt.ui.notify` writes a single line to the IDE's **Output** dock
   under the **Plugins** channel — a low-noise way to confirm what
   happened without popping a dialog.

## 4. Load it

In the IDE, click **Plugins → Reload Plugins**. Your new entry
appears under **Plugins → Hello → Say hi**.

Open any file, click it, type your name, and watch the greeting
appear at the cursor.

!!! tip "Edit-reload-test"

    Every time you save a change to `plugin.lua`, click **Reload
    Plugins** again. The IDE will re-evaluate every plugin from
    scratch. If your script has a syntax error, the IDE shows a
    message box and writes the full error to the **Plugins** channel
    in the **Output** dock — nothing crashes.

## 5. Bind a hotkey

Add a `hotkey` field to `manifest.json` and reload:

```json
{
  "name": "Say hi",
  "entry": "plugin.lua",
  "command": "run",
  "menu": "Hello",
  "hotkey": "Ctrl+Alt+H"
}
```

The first plugin to register a given key sequence wins; conflicts are
logged but never silently overwrite a previous plugin's binding.

## 6. Where to go next

- Learn about the [available APIs](api/editor.md) — read the buffer,
  walk the project, build a dockable panel.
- See [Multi-file plugins](multi-file.md) when your `plugin.lua`
  starts getting long.
- Read [Error handling & reloading](errors.md) for how errors flow
  back to the user.
- Skim the [Cookbook](cookbook.md) for finished snippets you can
  paste in.
