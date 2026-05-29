# `manifest.json`

The manifest tells the IDE how to install your plugin in the menu and
which Lua function to call when the user activates it. It's a plain
JSON file at the root of your plugin folder.

## Minimal example

```json
{
  "name": "My Plugin",
  "entry": "plugin.lua",
  "command": "run"
}
```

Everything in the manifest is optional — even `name`. With an empty
manifest the IDE falls back to the folder name for the display name
and `plugin.lua` / `run` for the entry script and command.

## Full reference

| Key           | Type   | Default       | Description |
| ------------- | ------ | ------------- | ----------- |
| `name`        | string | folder name   | Display name shown in the **Plugins** menu. |
| `description` | string | `""`          | One-line summary shown in the **Plugin Settings** dialog. |
| `version`     | string | `""`          | Free-form version label. Not parsed by the IDE. |
| `author`      | string | `""`          | Free-form author label. |
| `entry`       | string | `plugin.lua`  | Script file to load, relative to the plugin folder. |
| `command`     | string | `run`         | Global Lua function the IDE calls when the menu entry is activated. |
| `hotkey`      | string | —             | Qt key sequence, e.g. `Ctrl+Alt+U`. The first-loaded plugin wins on conflict. |
| `menu`        | string | —             | Optional submenu under **Plugins** for grouping. |

## Practical notes

### `name`

Whatever string you pick shows up verbatim in the **Plugins** menu —
emoji and Unicode are fine.

### `entry` and `command`

Together these point at the function the IDE calls. With the defaults
(`entry = "plugin.lua"`, `command = "run"`), you need a global `run`
function in `plugin.lua`. If you'd rather call your function
something else, override both:

```json
{
  "entry": "main.lua",
  "command": "main"
}
```

```lua
-- main.lua
function main()
  pt.ui.alert("called!")
end
```

### `hotkey`

Uses Qt's [key sequence
syntax](https://doc.qt.io/qt-6/qkeysequence.html). Common patterns:

| Sequence             | Meaning |
| -------------------- | ------- |
| `Ctrl+Alt+U`         | Hold Ctrl and Alt, press U. |
| `F8`                 | A single function key. |
| `Ctrl+Shift+P`       | Ctrl + Shift + P. |
| `Ctrl+K, Ctrl+S`     | Two-step chord: Ctrl+K then Ctrl+S. |

The first plugin loaded with a given binding wins. Conflicts are
logged in the **Output** dock under the **Plugins** channel.

### `menu`

If `menu` is set, the IDE creates (or reuses) a submenu under
**Plugins** with that label and puts your entry there. Plugins
without a `menu` field land at the top level.

Useful if you ship several related plugins and want them grouped:

```json
{ "name": "Edit Pokémon", "menu": "Gen 1/2" }
{ "name": "Edit Trainers", "menu": "Gen 1/2" }
```

The IDE will end up with **Plugins → Gen 1/2 → Edit Pokémon** and
**Plugins → Gen 1/2 → Edit Trainers**.

## Manifest pitfalls

!!! warning "JSON, not JavaScript"

    The manifest is strict JSON: double-quoted keys and string
    values, no trailing commas, no `//` comments. If parsing fails
    the IDE logs a warning and skips the plugin.

!!! info "Don't quote the version like `1.0`"

    `version` is a string — write `"1.0.0"`, not `1.0`. Quotes are
    cheap, JSON's number parser is not.

!!! tip "Reload after every change"

    The manifest is only read at startup or when you click **Plugins
    → Reload Plugins**. Editing `manifest.json` without reloading
    leaves the IDE on the old metadata.
