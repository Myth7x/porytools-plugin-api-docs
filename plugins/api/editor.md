# `pt.editor`

The currently focused editor tab. Every function on `pt.editor`
operates on whichever tab the user has the caret in *right now* — if
no tab is focused, the read functions return empty strings and the
write functions are a no-op.

All line and column numbers are **1-based**.

## Functions

| Function           | Parameters | Returns | Description |
| ------------------ | ---------- | ------- | ----------- |
| `path`             | —          | `string \| nil`               | Absolute path of the active tab; `nil` for an untitled buffer. |
| `text`             | —          | `string`                      | The entire buffer contents. |
| `setText`          | `s: string` | `bool`                        | Replace the entire buffer as a single undo step. |
| `selection`        | —          | `string`                      | The currently selected text, or `""` if there's no selection. |
| `replaceSelection` | `s: string` | `bool`                        | Replace the selection with `s`. If nothing is selected, inserts at the cursor. |
| `cursor`           | —          | `line: int, col: int`         | The caret position. |
| `setCursor`        | `line: int, col: int` | `bool`              | Move the caret. |
| `insertAt`         | `line: int, col: int, s: string` | `bool`   | Insert `s` at the given position. |
| `deleteRange`      | `l1: int, c1: int, l2: int, c2: int` | `bool` | Delete text between two positions. |
| `lineCount`        | —          | `int`                         | Number of lines in the buffer. |
| `lineText`         | `n: int`   | `string`                      | Text of line `n`. |
| `find`             | `pattern: string, opts?: FindOpts` | `FindResult \| nil` | Find the next match. Without `from`, starts from the current cursor position. |
| `replaceAll`       | `pattern: string, repl: string, opts?: FindOpts` | `int` | Replace every match; returns the replacement count. |
| `save`             | —          | `ok: bool, err: string \| nil` | Save the active tab. |

## Types

### `FindOpts`

| Key     | Type | Default          | Description |
| ------- | ---- | ---------------- | ----------- |
| `regex` | bool | `false`          | Treat `pattern` as a [QRegularExpression](https://doc.qt.io/qt-6/qregularexpression.html). |
| `case`  | bool | `false`          | Case-sensitive matching. |
| `from`  | int  | cursor position  | 1-based **character offset** to start searching from. |

### `FindResult`

| Key    | Type | Description |
| ------ | ---- | ----------- |
| `line` | int  | 1-based line number of the match. |
| `col`  | int  | 1-based column of the match start. |
| `len`  | int  | Length of the matched text in characters. |
| `pos`  | int  | 1-based absolute character offset of the match. |

## Examples

### Uppercase every label identifier

```lua
function run()
  local text = pt.editor.text()
  local count = 0
  local new = text:gsub("([%w_]+)(%s*:)", function(name, colon)
    count = count + 1
    return name:upper() .. colon
  end)
  if count > 0 then pt.editor.setText(new) end
  pt.ui.notify(string.format("Renamed %d labels", count))
end
```

`setText` replaces the entire buffer as one undo step, so the user
can revert the whole pass with a single Ctrl+Z.

### Wrap the current selection in a comment block

```lua
function run()
  local sel = pt.editor.selection()
  if sel == "" then return end
  pt.editor.replaceSelection("; -- BEGIN --\n" .. sel .. "\n; -- END --")
end
```

### Jump to the first TODO comment

```lua
function run()
  local hit = pt.editor.find("TODO", { case = true, from = 1 })
  if hit then pt.editor.setCursor(hit.line, hit.col) end
end
```

Passing `from = 1` forces the search to start at the beginning of the
buffer regardless of where the cursor currently is.

### Regex replace-all

```lua
function run()
  local n = pt.editor.replaceAll("\\bret\\b", "RET", { regex = true, case = true })
  pt.ui.notify(string.format("Replaced %d occurrences", n))
end
```

!!! info "Word boundaries with `\b`"

    Inside JSON-quoted Lua strings, `\b` would be a backspace
    character — write `\\b` so it reaches the regex engine as `\b`.

### Insert at a specific line

```lua
function run()
  -- Add a comment as line 2.
  pt.editor.insertAt(2, 1, "; auto-generated banner\n")
end
```

`insertAt` shifts existing text down; combine with `lineCount` to
append at the end.

## Tips

!!! tip "`text()` once, `setText()` once"

    For a whole-buffer transform, prefer reading the entire text into
    a Lua string, transforming, and writing it back in one go. That's
    one undo step and one redraw.

!!! warning "Unicode and `col`"

    Columns count **characters**, not bytes. ASCII assembly source is
    fine either way; if you start parsing UTF-8 text remember the
    distinction when you compute offsets.

!!! danger "No tab open"

    If no editor tab is focused, every reader returns an empty string
    and every writer is a no-op. Check `pt.editor.path()` first if
    you need to know.
