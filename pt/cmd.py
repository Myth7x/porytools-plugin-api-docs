"""``pt.cmd`` — thin wrappers over the IDE's own menu actions.

Use these when you want the same side effects a user would get from clicking
the menu item — including any prompts, dirty-state tracking, and undo history.

Every function operates on the **currently focused editor tab** — the same tab
`pt.editor` operates on. If no tab is focused, the call is a no-op.

.. tip::
   Use the API that fits:

   - Save the active tab and react to failures → `pt.editor.save`.
   - Mimic the user clicking File → Save → `save`.
   - Save every dirty tab at once → `pt.tabs.saveAll`.

.. note::
   `pt.cmd` only exposes the actions that have menu entries. There is no
   ``pt.cmd.cut`` / ``pt.cmd.paste`` — use `pt.editor.selection`,
   `pt.editor.replaceSelection`, and friends for clipboard-free transforms.

Examples:
    Expand tabs, then save::

        function run()
          pt.editor.setText(pt.editor.text():gsub("\\t", "    "))
          pt.cmd.save()
        end

    Bulk fix-up with a manual undo point (`pt.editor.setText` is one undo step,
    so one `undo` rolls the whole pass back)::

        function run()
          pt.editor.setText(pt.editor.text():gsub("\\t", "    "))
          pt.cmd.undo()                                    -- mistake — roll it back
          pt.editor.setText(pt.editor.text():gsub("\\t", "  "))
        end
"""

from __future__ import annotations

__docformat__ = "google"


def save() -> None:
    """Save the active tab.

    Mirrors the File → Save menu action. Unlike `pt.editor.save`, it returns
    nothing — use `pt.editor.save` if you need to react to a save failure.
    """
    ...


def undo() -> None:
    """Undo in the active editor."""
    ...


def redo() -> None:
    """Redo in the active editor."""
    ...
