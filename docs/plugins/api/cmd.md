# `pt.cmd`

Thin wrappers over the IDE's own menu actions. Use these when you
want the same side effects a user would get from clicking the menu
item — including any prompts, dirty-state tracking, and undo
history.

## Functions

| Function | Parameters | Returns | Description |
| -------- | ---------- | ------- | ----------- |
| `save`   | — | — | Save the active tab. |
| `undo`   | — | — | Undo in the active editor. |
| `redo`   | — | — | Redo in the active editor. |

Every function operates on the **currently focused editor tab** — the
same tab `pt.editor` operates on. If no tab is focused, the call is a
no-op.

## Examples

### Expand tabs, then save

```lua
function run()
  pt.editor.setText(pt.editor.text():gsub("\t", "    "))
  pt.cmd.save()
end
```

`pt.cmd.save()` and `pt.editor.save()` do almost the same thing. The
difference: `pt.editor.save()` returns `(ok, err)` so you can react to
a save failure, while `pt.cmd.save()` mirrors the menu action and
just runs.

### Bulk fix-up with manual undo points

```lua
function run()
  -- Tab-expand pass.
  pt.editor.setText(pt.editor.text():gsub("\t", "    "))

  -- Mistake — undo the whole pass.
  pt.cmd.undo()

  -- Try again with a different replacement.
  pt.editor.setText(pt.editor.text():gsub("\t", "  "))
end
```

`pt.editor.setText` performs the replacement as a single undo step,
so one `pt.cmd.undo` is enough to roll the whole transformation back.

## Tips

!!! tip "Use the API that fits"

    | Want to… | Use |
    | -------- | --- |
    | Save the active tab and react to failures | `pt.editor.save` |
    | Mimic the user clicking File → Save | `pt.cmd.save` |
    | Save every dirty tab at once | `pt.tabs.saveAll` |

!!! info "No keyboard shortcuts here"

    `pt.cmd` only exposes the actions that have menu entries. There
    is no `pt.cmd.cut`, `pt.cmd.paste`, etc. — use
    `pt.editor.selection`, `pt.editor.replaceSelection`, and friends
    for clipboard-free transformations.
