"""``pt.tabs`` — open, close, enumerate, and save the IDE's editor tabs.

`pt.editor` operates on the **currently focused** tab; ``pt.tabs`` is how you
change which tab that is.

`close` always succeeds silently — it returns ``True`` whether it actually
closed a tab or there was no matching tab to close. Use it when you want to
clean up regardless of state.

.. tip::
   `open` is also focus: ``pt.tabs.open(path)`` opens ``path`` if it isn't
   already open, or focuses its existing tab if it is — the same behaviour you
   get from clicking the file in the project tree.

.. warning::
   A new tab that hasn't been saved has no path. It won't appear in `list`
   (which returns absolute paths only), and `current` returns ``None`` for it.

Examples:
    Save every dirty tab, then report::

        function run()
          pt.tabs.saveAll()
          pt.ui.notify("Saved " .. #pt.tabs.list() .. " files.")
        end

    Open every file that mentions a symbol. The ``seen`` set avoids
    re-focusing the same file once per hit::

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

    Close every tab outside the active project::

        function run()
          local root = pt.project.root()
          if not root then return end
          for _, path in ipairs(pt.tabs.list()) do
            if not path:find(root, 1, true) then     -- plain substring match
              pt.tabs.close(path)
            end
          end
        end
"""

from __future__ import annotations

__docformat__ = "google"


def open(path: str) -> tuple[bool, str | None]:
    """Open ``path`` in a tab, or focus its existing tab if already open.

    Args:
        path: Absolute path of the file to open.

    Returns:
        ``(ok, err)`` — ``err`` is ``None`` on success.
    """
    ...


def close(path: str) -> bool:
    """Close the tab for ``path`` without a save prompt.

    Args:
        path: Absolute path whose tab should be closed.

    Returns:
        ``True`` — always, whether or not a matching tab existed.
    """
    ...


def list() -> list[str]:
    """Absolute paths of every currently open tab.

    Returns:
        The list of open tab paths (untitled buffers are excluded).
    """
    ...


def current() -> str | None:
    """Absolute path of the focused tab.

    Returns:
        The path, or ``None`` for an untitled buffer.
    """
    ...


def saveAll() -> bool:
    """Save every dirty tab that has a path.

    Returns:
        ``False`` if any save failed, ``True`` otherwise.
    """
    ...
