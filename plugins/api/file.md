# `pt.file`

Disk-level file operations. These bypass the editor buffer, so
writing a file that's currently open closes and reopens its tab so
the on-screen view stays in sync with what's on disk.

Most read functions return `(value, err)`. Most mutating functions
return `(ok, err)`. See [Error handling](../errors.md) for the
pattern.

## Functions

| Function       | Parameters | Returns | Description |
| -------------- | ---------- | ------- | ----------- |
| `read`         | `path: string` | `string \| nil, err: string \| nil` | Read a UTF-8 file. |
| `write`        | `path: string, contents: string` | `ok: bool, err: string \| nil` | Write a UTF-8 file. Reloads any open tab for `path`. |
| `exists`       | `path: string` | `bool`              | Test whether the file exists. |
| `delete`       | `path: string` | `ok: bool, err: string \| nil` | Delete the file. Closes its tab if open. Succeeds silently if already absent. |
| `rename`       | `from: string, to: string` | `ok: bool, err: string \| nil` | Rename or move a file. Closes its tab if open. |
| `copy`         | `from: string, to: string, overwrite?: bool` | `ok: bool, err: string \| nil` | Copy a file. Pass `true` to overwrite an existing destination. |
| `mkdir`        | `path: string` | `ok: bool, err: string \| nil` | Create the directory **and all missing parents**. |
| `list`         | `dir: string, opts?: ListOpts` | `string[]` | List files in `dir`. |
| `findInFiles`  | `root: string, pattern: string, opts?: SearchOpts` | `SearchHit[]` | Grep-style recursive search across every file under `root`. |

## Types

### `ListOpts`

| Key         | Type                  | Default | Description |
| ----------- | --------------------- | ------- | ----------- |
| `recursive` | bool                  | `false` | Descend into subdirectories. |
| `glob`      | string or `string[]`  | —       | Filename filter(s), e.g. `"*.asm"` or `{"*.asm", "*.inc"}`. |

### `SearchOpts`

| Key     | Type       | Default | Description |
| ------- | ---------- | ------- | ----------- |
| `regex` | bool       | `false` | Treat `pattern` as a regular expression. |
| `case`  | bool       | `false` | Case-sensitive matching. |
| `glob`  | `string[]` | —       | Restrict search to files matching these filename patterns. |

### `SearchHit`

| Key    | Type   | Description |
| ------ | ------ | ----------- |
| `path` | string | Absolute path of the matching file. |
| `line` | int    | 1-based line number. |
| `col`  | int    | 1-based column of the match start. |
| `text` | string | Full text of the matching line. |

## Examples

### Scaffold a new `.asm` file

```lua
function run()
  local name = pt.ui.prompt("New file name (without .asm):")
  if not name then return end

  local path = pt.project.root() .. "/src/" .. name .. ".asm"
  if pt.file.exists(path) then
    pt.ui.alert("File already exists.")
    return
  end

  local body = 'SECTION "' .. name .. '", ROM0\n\n' .. name .. ':\n    ret\n'
  local ok, err = pt.file.write(path, body)
  if not ok then
    pt.ui.alert("Write failed: " .. err)
    return
  end

  pt.tabs.open(path)
end
```

`pt.file.write` will create the parent directory if it's missing
**only** because `pt.file.mkdir` is recursive. If you need to ensure
a nested folder exists first, call `pt.file.mkdir` explicitly:

```lua
pt.file.mkdir(pt.project.root() .. "/src/generated")
pt.file.write(pt.project.root() .. "/src/generated/a.asm", body)
```

### Bulk-rename `.s` files to `.asm`

```lua
function run()
  local files = pt.file.list(pt.project.root(), {
    recursive = true,
    glob = "*.s",
  })
  for _, p in ipairs(files) do
    pt.file.rename(p, (p:gsub("%.s$", ".asm")))
  end
  pt.ui.notify("Renamed " .. #files .. " files.")
end
```

### Find every reference to a label

```lua
function run()
  local label = pt.ui.prompt("Symbol to find:")
  if not label then return end

  local hits = pt.file.findInFiles(pt.project.root(), label, {
    glob = { "*.asm", "*.inc" },
    case = true,
  })
  for _, h in ipairs(hits) do
    pt.ui.notify(string.format("%s:%d:%d  %s", h.path, h.line, h.col, h.text))
  end
end
```

For a one-off label rename, combine `findInFiles` (to discover
files), `pt.file.read`+`gsub`+`pt.file.write` to rewrite them, and
display a summary.

### Copy a binary asset

```lua
function run()
  local picked = pt.ui.pickFile({ filters = "PNG images (*.png)" })
  if not picked then return end

  local dest = pt.project.root() .. "/gfx/pokemon/bulbasaur/front.png"
  local ok, err = pt.file.copy(picked, dest, true)   -- overwrite
  if not ok then pt.ui.alert("Copy failed: " .. err); return end
  pt.ui.notify("Replaced " .. dest)
end
```

`copy`'s third argument defaults to `false` — without it, copying
onto an existing destination returns `(false, "destination exists")`.

## Tips

!!! tip "Globs vs regex"

    `list` and `findInFiles` accept filename globs (`*.asm`,
    `*.{asm,inc}`). For content matching use `regex = true` in
    `findInFiles`; the syntax is Qt's
    [QRegularExpression](https://doc.qt.io/qt-6/qregularexpression.html).

!!! warning "`write` reloads open tabs"

    Writing to a path that's currently open closes and reopens the
    tab. If the user had unsaved changes in that tab, they're
    discarded — the tab now reflects what was just written. Prompt
    or call `pt.tabs.saveAll` first if you're not sure.

!!! info "Path separators"

    Both `/` and `\` work on Windows. Returning forward slashes from
    your code keeps things portable.
