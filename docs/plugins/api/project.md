# `pt.project`

Information about the currently open project. A project is a folder
opened via **File → Open Project…**; for pokered or pokecrystal that's
the repo root.

## Functions

| Function | Parameters | Returns | Description |
| -------- | ---------- | ------- | ----------- |
| `isOpen` | —          | `bool`              | `true` when a project is loaded. |
| `root`   | —          | `string \| nil`     | Absolute path to the project root, or `nil` if no project is open. |
| `files`  | `opts?: FilesOpts` | `string[]`  | Every file under the project root. **Always recursive.** |

## Types

### `FilesOpts`

| Key   | Type       | Description |
| ----- | ---------- | ----------- |
| `ext` | `string[]` | Only return files whose extension matches, e.g. `{".asm", ".inc"}`. |

## Examples

### Bail early if no project is open

Almost every plugin that touches the project should start with this:

```lua
function run()
  if not pt.project.isOpen() then
    pt.ui.alert("Open a project first.")
    return
  end
  -- ...
end
```

### Count `.asm` files in the project

```lua
function run()
  if not pt.project.isOpen() then return end
  local files = pt.project.files({ ext = { ".asm" } })
  pt.ui.notify("Project has " .. #files .. " .asm files.")
end
```

### Resolve a path relative to the project root

```lua
local function resolve(rel)
  local root = pt.project.root()
  if not root then return nil end
  local guess = root .. "/" .. rel
  if pt.file.exists(guess) then return guess end
  return nil
end

function run()
  local statsDir = resolve("data/pokemon/base_stats")
  if not statsDir then
    pt.ui.alert("Couldn't find data/pokemon/base_stats.")
    return
  end
  -- ...
end
```

This `resolve` helper is the pattern used throughout the **Edit
Pokémon** example plugin to handle both pokered and pokecrystal
layouts without special-casing each one — they share most paths, so
the helper just succeeds for whichever fork the user has open.

## `pt.project.files` vs `pt.file.list`

Both walk directories and return absolute paths, but they have
different jobs:

| | `pt.project.files` | `pt.file.list` |
| --- | --- | --- |
| Root | the project root, always | any directory you name |
| Recursion | always recursive | opt-in via `recursive = true` |
| Filter | by extension | by glob (e.g. `*.asm`) |
| Needs project? | yes | no |

Use `pt.project.files` for "give me every X in the project" and
`pt.file.list` for "give me every X under this specific folder".

## Tips

!!! tip "Use `pt.project.root()` as your anchor"

    Resolving file paths from `pt.project.root()` is the safest way
    to write plugins that work across forks. The two disassemblies
    share enough structure that a path like
    `data/pokemon/base_stats/bulbasaur.asm` exists in both — the
    helper above tries the path and lets `pt.file.exists` decide.

!!! warning "No project, no root"

    `pt.project.root()` returns `nil` when no project is open. Guard
    with `isOpen()` (or check the `nil`) before concatenating it
    into a path string — otherwise you'll get a Lua "attempt to
    concatenate a nil value" error.
