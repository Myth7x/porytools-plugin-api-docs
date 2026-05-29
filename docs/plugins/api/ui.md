# `pt.ui`

Everything user-facing: modal dialogs, the IDE's **Output** dock, and
the dockable-widget system you use to build a custom panel.

`pt.ui` is the biggest module — this page is split into two halves:

1. **[Dialogs](#dialogs)** — modal popups you can fire from anywhere.
2. **[Dockable widgets](#dockable-widgets)** — long-lived panels you
   build once and reuse.

## Dialogs

Every dialog is **modal and synchronous**: the call blocks until the
user closes the dialog. Cancelling returns `nil`.

| Function     | Parameters | Returns | Description |
| ------------ | ---------- | ------- | ----------- |
| `alert`      | `msg: string, title?: string` | — | Information box. Returns when the user clicks OK. |
| `confirm`    | `msg: string, title?: string` | `bool` | Yes/No question. |
| `prompt`     | `label: string, default?: string, title?: string` | `string \| nil` | Single-line text input. |
| `choose`     | `label: string, items: string[], title?: string` | `string \| nil` | Pick one item from a list. |
| `pickFile`   | `opts?: PickFileOpts` | `string \| nil` | Native file picker. |
| `pickFolder` | `label?: string` | `string \| nil` | Native folder picker. |
| `notify`     | `msg: string` | — | Append a line to the **Output** dock under the **Plugins** channel. |

### `PickFileOpts`

| Key       | Type   | Default                | Description |
| --------- | ------ | ---------------------- | ----------- |
| `save`    | bool   | `false`                | Show a Save dialog instead of Open. |
| `dir`     | string | `""`                   | Initial directory the dialog opens in. |
| `filters` | string | `"All Files (*)"`      | Qt filter string, e.g. `"GBA (*.gba);;All Files (*)"`. |

### Dialog examples

#### Multi-step interaction

```lua
function run()
  local section = pt.ui.choose("Pick a section bank:", {
    "ROM0", "ROMX", "WRAM0", "HRAM",
  })
  if not section then return end

  local name = pt.ui.prompt("Symbol name:")
  if not name then return end

  if not pt.ui.confirm(string.format(
       "Generate skeleton for %s in %s?", name, section)) then
    return
  end

  pt.editor.replaceSelection(string.format(
    'SECTION "%s", %s\n%s:\n    ret\n', name, section, name))
end
```

`choose`, `prompt`, and `confirm` all run to completion before the
next line of Lua executes. There are no callbacks for dialogs — they
just return.

#### Export the active buffer to a user-chosen file

```lua
function run()
  local out = pt.ui.pickFile({
    save    = true,
    filters = "Text (*.txt);;All Files (*)",
  })
  if not out then return end

  local ok, err = pt.file.write(out, pt.editor.text())
  if not ok then pt.ui.alert("Write failed: " .. err); return end
  pt.ui.notify("Wrote " .. out)
end
```

#### Quiet status updates

`pt.ui.notify` is the preferred way to report progress and successful
operations — it doesn't interrupt the user the way `alert` does:

```lua
function run()
  for i, p in ipairs(pt.project.files({ ext = { ".asm" } })) do
    -- ... do work ...
    pt.ui.notify(string.format("[%d/%d] processed %s", i, count, p))
  end
end
```

---

## Dockable widgets

`pt.ui.createWidget(title)` returns a `PluginWidget` — a Qt
`QDockWidget` you can drag, float, hide, or close. You add child
controls to it (labels, buttons, inputs, dropdowns, images) and place
them with absolute coordinates.

| Function       | Parameters | Returns | Description |
| -------------- | ---------- | ------- | ----------- |
| `createWidget` | `title: string` | `PluginWidget` | Create a dockable panel attached to the main window. |

Widgets are owned by the engine and live until **Reload Plugins**.
**Store the widget in a `local` outside `run()`** so the same instance
is reused when the user re-opens the menu entry.

### `PluginWidget`

| Method        | Parameters | Returns | Description |
| ------------- | ---------- | ------- | ----------- |
| `setSize`     | `w: int, h: int` | — | Set the initial content area size. |
| `setTitle`    | `s: string` | — | Change the dock header title. |
| `show`        | — | — | Show the dock. |
| `hide`        | — | — | Hide the dock. |
| `close`       | — | — | Close the dock. |
| `addLabel`    | `text: string` | `PluginLabel`     | Add a static text label. |
| `addButton`   | `text: string` | `PluginButton`    | Add a clickable button. |
| `addLineEdit` | `default?: string` | `PluginLineEdit` | Add a single-line text input. |
| `addTextArea` | `default?: string` | `PluginTextArea` | Add a multi-line plain-text editor. |
| `addSelection`| `placeholder?: string` | `PluginSelection` | Add a dropdown (combo box). |
| `addImage`    | `path?: string` | `PluginImage`    | Add an image pane (PNG, JPG, GIF, BMP, SVG). |

Every child widget supports `setPosition(x, y)` and `setSize(w, h)`
with **absolute coordinates** measured in pixels from the top-left of
the dock's content area. There is no layout system — you pick the
positions yourself.

### `PluginLabel`

| Method        | Parameters | Returns | Description |
| ------------- | ---------- | ------- | ----------- |
| `setPosition` | `x: int, y: int` | — | Move the label. |
| `setSize`     | `w: int, h: int` | — | Resize the label. |
| `setText`     | `s: string` | — | Set the display text. |
| `text`        | — | `string` | Read the current text. |
| `setVisible`  | `v: bool` | — | Show or hide the label. |

!!! info "Only `PluginLabel` has `setVisible`"

    The other widget types don't currently expose `setVisible`. A
    common workaround for "hide a group of controls" is to move them
    off-screen with `setPosition(-9999, -9999)` and restore the
    coordinates later — see the [Section helper
    pattern](../cookbook.md#section-helper-show-and-hide-a-group-of-widgets).

### `PluginButton`

| Method        | Parameters | Returns | Description |
| ------------- | ---------- | ------- | ----------- |
| `setPosition` | `x: int, y: int` | — | Move the button. |
| `setSize`     | `w: int, h: int` | — | Resize the button. |
| `setText`     | `s: string` | — | Set the button label. |
| `onClick`     | `fn: function` | — | Connect a Lua callback; called with no arguments on click. |

### `PluginLineEdit`

| Method           | Parameters | Returns | Description |
| ---------------- | ---------- | ------- | ----------- |
| `setPosition`    | `x: int, y: int` | — | Move the input field. |
| `setSize`        | `w: int, h: int` | — | Resize the input field. |
| `setText`        | `s: string` | — | Set the current text. |
| `text`           | — | `string` | Read the current text. |
| `setPlaceholder` | `s: string` | — | Set placeholder/hint text shown when empty. |

### `PluginTextArea`

| Method        | Parameters | Returns | Description |
| ------------- | ---------- | ------- | ----------- |
| `setPosition` | `x: int, y: int` | — | Move the text area. |
| `setSize`     | `w: int, h: int` | — | Resize the text area. |
| `setText`     | `s: string` | — | Replace all text. |
| `text`        | — | `string` | Read all text. |
| `append`      | `s: string` | — | Append `s` to the end (followed by a newline). |

### `PluginImage`

| Method        | Parameters | Returns | Description |
| ------------- | ---------- | ------- | ----------- |
| `setPosition` | `x: int, y: int` | — | Move the image pane. |
| `setSize`     | `w: int, h: int` | — | Resize the pane. The image is rescaled preserving aspect ratio. |
| `setImage`    | `path: string` | `bool` | Load an image from disk. Returns `false` if the file can't be read. |
| `imagePath`   | — | `string` | Path of the currently loaded image, or `""` if none. |
| `clear`       | — | — | Unload the current image. |

### `PluginSelection`

| Method            | Parameters | Returns | Description |
| ----------------- | ---------- | ------- | ----------- |
| `setPosition`     | `x: int, y: int` | — | Move the dropdown. |
| `setSize`         | `w: int, h: int` | — | Resize the dropdown. |
| `addItem`         | `s: string` | — | Append one option. |
| `setItems`        | `items: string[]` | — | Replace all options. |
| `clear`           | — | — | Remove all options. |
| `count`           | — | `int` | Number of options. |
| `currentIndex`    | — | `int` | 1-based index of the selected option; `0` when empty. |
| `currentText`     | — | `string` | Display text of the selected option. |
| `setCurrentIndex` | `i: int` | — | Select by 1-based index. |
| `setCurrentText`  | `s: string` | — | Select by display text. |
| `onChange`        | `fn: function(index, text)` | — | Callback fired when the selection changes. |

### Widget examples

#### Persistent counter panel

```lua
local panel

function run()
  -- Re-show the existing panel instead of building a second one.
  if panel then panel:show(); return end

  panel = pt.ui.createWidget("Counter")
  panel:setSize(220, 120)

  local label = panel:addLabel("Count: 0")
  label:setPosition(12, 12)

  local btn = panel:addButton("Increment")
  btn:setPosition(12, 50)

  local count = 0
  btn:onClick(function()
    count = count + 1
    label:setText("Count: " .. count)
  end)

  panel:show()
end
```

The `panel`, `label`, `btn` and `count` locals live for as long as
the plugin is loaded. They survive across `run()` calls, so clicking
the menu entry again brings back the same panel with the same count.

#### A search-as-you-type filter

```lua
local panel, input, results

function run()
  if panel then panel:show(); return end

  panel = pt.ui.createWidget("Quick find")
  panel:setSize(360, 320)

  input = panel:addLineEdit("")
  input:setPlaceholder("Type a label name…")
  input:setPosition(12, 12)
  input:setSize(336, 26)

  results = panel:addTextArea("")
  results:setPosition(12, 48)
  results:setSize(336, 260)

  -- Refresh the result list every time the user changes the input
  -- via a click on the (re-purposed) panel button.
  local refresh = panel:addButton("Search")
  refresh:setPosition(264, 12)
  refresh:setSize(84, 26)
  refresh:onClick(function()
    local q = input:text()
    if q == "" then results:setText(""); return end

    local hits = pt.file.findInFiles(pt.project.root(), q, { case = false })
    local lines = {}
    for _, h in ipairs(hits) do
      table.insert(lines, string.format("%s:%d  %s", h.path, h.line, h.text))
    end
    results:setText(table.concat(lines, "\n"))
  end)

  panel:show()
end
```

The same dock will keep its place in the layout across reloads of the
panel (open → close → re-open from the menu) because `panel` lives at
file scope.

## Tips

!!! tip "One widget object per plugin"

    Build the panel once in `run()` and store every child reference
    in `local` variables (or fields on a table) outside the function.
    `run()` only needs to call `panel:show()` on subsequent
    invocations.

!!! warning "Cleanup on reload"

    **Reload Plugins** destroys every dock the plugin opened. If
    your user has unsaved work in a `PluginTextArea`, that work is
    gone. Write it to disk (or the editor buffer) before relying on
    reload during development.

!!! info "Absolute positioning"

    There is no automatic layout. If you change your panel's size or
    a field's label width, you may need to nudge other coordinates
    too. The Edit Pokémon example plugin shows one way to keep
    related controls together: build them through a helper that
    advances a running `y` cursor.
