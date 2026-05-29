# Multi-file plugins

Once a plugin is more than a couple hundred lines, keeping everything
in one `plugin.lua` stops being fun. The IDE supports splitting your
plugin across as many files as you like with plain Lua `require()`.

## How the host wires it up

When the IDE loads your plugin it does two things specifically to
make multi-file plugins work:

1. It sets a **global** called `__plugin_dir` in your plugin's sandbox
   to the absolute path of your plugin folder.

2. It **temporarily prepends** your plugin folder to `package.path`
   while your entry script is being evaluated:

    ```
    <plugin_dir>/?.lua
    <plugin_dir>/?/init.lua
    ...the host's original package.path...
    ```

So as soon as `plugin.lua` starts executing, `require("util")` finds
`<plugin_dir>/util.lua`, and `require("ui.panel")` finds
`<plugin_dir>/ui/panel.lua`. No setup code.

After your entry script finishes loading, `package.path` is restored
to its original value. That's fine because every module you
`require()` at the top of `plugin.lua` is **cached** in
`package.loaded`, so later calls return the cached copy without
hitting `package.path`.

!!! warning "`require()` at the top of `plugin.lua`"

    The temporary `package.path` only lasts for the load of your
    entry script. If you call `require()` from inside `run()` or a
    button callback for a module you've never `require()`d before,
    Lua won't be able to find it. The fix is simple: do all your
    `require()` calls at the top of `plugin.lua`, the same way most
    Lua and Python code organises imports.

## Recommended layout

```
my-plugin/
├── manifest.json
├── plugin.lua                  -- entry: requires modules, defines run()
└── my_plugin/                  -- namespace folder, see warning below
    ├── util.lua
    ├── parser.lua
    └── ui.lua
```

```lua
-- plugin.lua
local Util   = require("my_plugin.util")
local Parser = require("my_plugin.parser")
local UI     = require("my_plugin.ui")

function run()
  UI.show()
end
```

```lua
-- my_plugin/util.lua
local Util = {}

function Util.trim(s)
  return (s:gsub("^%s+", ""):gsub("%s+$", ""))
end

return Util
```

Each module follows the standard Lua pattern: build a local table,
attach functions to it, and `return` it.

## Why the namespace folder?

The IDE runs every plugin in its own sandbox, **but** the underlying
`package.loaded` cache is shared across the whole Lua state. If two
plugins both `require("util")`, the second one gets the first one's
cached module instead of its own.

The fix is to put your modules under a folder named after your plugin
(e.g. `my_plugin/`) and `require("my_plugin.util")` — the cache key
becomes `"my_plugin.util"` instead of `"util"`, and you can't clash
with anyone else as long as the folder name is unique.

## Reading your plugin's directory

You don't need to read `__plugin_dir` to make `require()` work — the
host already set up `package.path` for you. But it's useful if you
want to ship data files alongside your code (a JSON config, a
template `.asm` file, etc.):

```lua
local templatePath = __plugin_dir .. "/templates/skeleton.asm"
local text, err = pt.file.read(templatePath)
```

`__plugin_dir` uses forward slashes regardless of platform.

## Worked example

The bundled `example-plugins/edit-pokemon` plugin is a complete
multi-file example. Its layout looks like this:

```
edit-pokemon/
├── manifest.json
├── plugin.lua
└── edit_pokemon/
    ├── util.lua
    ├── constants.lua
    ├── pokemon.lua
    ├── base_stats_file.lua
    ├── evos_attacks_file.lua
    ├── egg_moves_file.lua
    └── ui.lua
```

And its `plugin.lua` opens like this:

```lua
local Constants    = require("edit_pokemon.constants")
local Pokemon      = require("edit_pokemon.pokemon")
local BaseStats    = require("edit_pokemon.base_stats_file")
local EvosAttacks  = require("edit_pokemon.evos_attacks_file")
local EggMoves     = require("edit_pokemon.egg_moves_file")
local UI           = require("edit_pokemon.ui")
```

The full annotated walkthrough is on the [Example
plugins](examples.md#edit-pokemon) page.
