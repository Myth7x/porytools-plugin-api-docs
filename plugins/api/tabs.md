# `pt.tabs`

Open, close, enumerate, and save the IDE's editor tabs.
[`pt.editor`](editor.md) operates on the **currently focused** tab;
`pt.tabs` is how you change which tab that is.

## Functions

| Function   | Parameters       | Returns                          | Description |
| ---------- | ---------------- | -------------------------------- | ----------- |
| `open`     | `path: string`   | `ok: bool, err: string \| nil`   | Open `path` in a tab, or focus its existing tab if already open. |
| `close`    | `path: string`   | `bool`                           | Close the tab for `path` without a save prompt. |
| `list`     | —                | `string[]`                       | Absolute paths of every currently open tab. |
| `current`  | —                | `string \| nil`                  | Absolute path of the focused tab; `nil` for an untitled buffer. |
| `saveAll`  | —                | `bool`                           | Save every dirty tab that has a path. Returns `false` if any save failed. |

`close` always succeeds silently — it returns `true` whether it
actually closed a tab or there was no matching tab to close. Use it
when you want to clean up regardless of state.

## Examples

### Save every dirty tab, then report

```lua
function run()
  pt.tabs.saveAll()
  pt.ui.notify("Saved " .. #pt.tabs.list() .. " files.")
end
```

### Open every file that mentions a symbol

```lua
function run()
  local hits = pt.file.findInFiles(pt.project.root(), "OAMBuffer", { case = true })
  local seen = {}
  for _, h in ipairs(hits) do
    if not seen[h.path] then
      pt.tabs.open(h.path)
      seen[h.path] = true
    end
  end
end
```

The `seen` set avoids re-opening (re-focusing) the same file once per
hit when there are multiple matches in one file.

### Close every tab outside the active project

```lua
function run()
  local root = pt.project.root()
  if not root then return end

  for _, path in ipairs(pt.tabs.list()) do
    if not path:find(root, 1, true) then     -- plain substring match
      pt.tabs.close(path)
    end
  end
end
```

### Round-trip a tab through disk

```lua
function run()
  local path = pt.tabs.current()
  if not path then
    pt.ui.alert("Save the buffer first so it has a path.")
    return
  end

  pt.tabs.close(path)
  pt.tabs.open(path)              -- now reflects on-disk state
end
```

`pt.file.write` also reloads the open tab for the file it writes, so
you only need this dance if you've edited the file behind the IDE's
back (e.g. via an external process).

## Tips

!!! tip "`open` is also focus"

    `pt.tabs.open(path)` opens `path` if it isn't already open, or
    focuses its existing tab if it is — the same behaviour you get
    from clicking the file in the project tree.

!!! warning "Untitled tabs"

    A new tab that hasn't been saved has no path. It won't appear in
    `pt.tabs.list()` (which returns absolute paths only), and
    `pt.tabs.current()` returns `nil` for it.
