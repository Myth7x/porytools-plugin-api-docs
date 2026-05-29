"""``pt.project`` — information about the currently open project.

A project is a folder opened via **File → Open Project…**; for pokered or
pokecrystal that's the repo root.

`files` vs `pt.file.list`: both walk directories and return absolute paths, but
they have different jobs. `files` always walks the project root, is always
recursive, and filters by extension; `pt.file.list` walks any directory you
name, recurses only with ``recursive = true``, and filters by glob. Use `files`
for "give me every X in the project" and `pt.file.list` for "give me every X
under this specific folder".

.. tip::
   Use `root` as your anchor. Resolving paths from ``pt.project.root()`` is the
   safest way to write plugins that work across forks — pokered and pokecrystal
   share enough structure that a path like
   ``data/pokemon/base_stats/bulbasaur.asm`` exists in both.

.. warning::
   `root` returns ``None`` when no project is open. Guard with `isOpen` (or
   check the ``None``) before concatenating it into a path string — otherwise
   you'll get a Lua "attempt to concatenate a nil value" error.

Examples:
    Bail early if no project is open — almost every plugin should start here::

        function run()
          if not pt.project.isOpen() then
            pt.ui.alert("Open a project first.")
            return
          end
          -- ...
        end

    Count ``.asm`` files in the project::

        function run()
          if not pt.project.isOpen() then return end
          local files = pt.project.files({ ext = { ".asm" } })
          pt.ui.notify("Project has " .. #files .. " .asm files.")
        end

    Resolve a path relative to the project root::

        local function resolve(rel)
          local root = pt.project.root()
          if not root then return nil end
          local guess = root .. "/" .. rel
          if pt.file.exists(guess) then return guess end
          return nil
        end
"""

from __future__ import annotations

__docformat__ = "google"


class FilesOpts:
    """Options for `files`."""

    ext: list[str]  #: Only return files whose extension matches, e.g. ``{".asm", ".inc"}``.


def isOpen() -> bool:
    """Whether a project is loaded.

    Returns:
        ``True`` when a project is open.
    """
    ...


def root() -> str | None:
    """Absolute path to the project root.

    Returns:
        The root path, or ``None`` if no project is open.
    """
    ...


def files(opts: FilesOpts | None = None) -> list[str]:
    """Every file under the project root. **Always recursive.**

    Args:
        opts: Optional `FilesOpts` to filter by extension.

    Returns:
        Absolute paths of the matching files.
    """
    ...
