"""``pt.file`` — disk-level file operations.

These bypass the editor buffer, so writing a file that's currently open closes
and reopens its tab to keep the on-screen view in sync with disk.

Most read functions return ``(value, err)``. Most mutating functions return
``(ok, err)``.

.. tip::
   `list` and `findInFiles` accept filename globs (``*.asm``, ``*.{asm,inc}``).
   For content matching use ``regex = true`` in `findInFiles`; the syntax is
   Qt's `QRegularExpression <https://doc.qt.io/qt-6/qregularexpression.html>`_.

.. warning::
   `write` reloads open tabs. Writing to a path that's currently open closes
   and reopens the tab; unsaved changes in that tab are discarded. Prompt or
   call `pt.tabs.saveAll` first if you're not sure.

.. note::
   Both ``/`` and ``\\`` work on Windows. Returning forward slashes from your
   code keeps things portable.

Examples:
    Scaffold a new ``.asm`` file::

        function run()
          local name = pt.ui.prompt("New file name (without .asm):")
          if not name then return end
          local path = pt.project.root() .. "/src/" .. name .. ".asm"
          if pt.file.exists(path) then
            pt.ui.alert("File already exists.")
            return
          end
          local body = 'SECTION "' .. name .. '", ROM0\\n\\n' .. name .. ':\\n    ret\\n'
          local ok, err = pt.file.write(path, body)
          if not ok then
            pt.ui.alert("Write failed: " .. err)
            return
          end
          pt.tabs.open(path)
        end

    Bulk-rename ``.s`` files to ``.asm``::

        function run()
          local files = pt.file.list(pt.project.root(), { recursive = true, glob = "*.s" })
          for _, p in ipairs(files) do
            pt.file.rename(p, (p:gsub("%.s$", ".asm")))
          end
          pt.ui.notify("Renamed " .. #files .. " files.")
        end

    Copy a binary asset (``copy``'s third arg defaults to ``false`` — copying
    onto an existing destination returns ``(false, "destination exists")``)::

        function run()
          local picked = pt.ui.pickFile({ filters = "PNG images (*.png)" })
          if not picked then return end
          local dest = pt.project.root() .. "/gfx/pokemon/bulbasaur/front.png"
          local ok, err = pt.file.copy(picked, dest, true)   -- overwrite
          if not ok then pt.ui.alert("Copy failed: " .. err); return end
          pt.ui.notify("Replaced " .. dest)
        end
"""

from __future__ import annotations

__docformat__ = "google"


class ListOpts:
    """Options for `list`."""

    recursive: bool  #: Descend into subdirectories. Default ``False``.
    glob: str | list[str]  #: Filename filter(s), e.g. ``"*.asm"`` or ``{"*.asm", "*.inc"}``.


class SearchOpts:
    """Options for `findInFiles`."""

    regex: bool  #: Treat ``pattern`` as a regular expression. Default ``False``.
    case: bool  #: Case-sensitive matching. Default ``False``.
    glob: list[str]  #: Restrict the search to files matching these filename patterns.


class SearchHit:
    """A single match returned by `findInFiles`."""

    path: str  #: Absolute path of the matching file.
    line: int  #: 1-based line number.
    col: int  #: 1-based column of the match start.
    text: str  #: Full text of the matching line.


def read(path: str) -> tuple[str | None, str | None]:
    """Read a UTF-8 file.

    Args:
        path: Absolute path of the file to read.

    Returns:
        ``(contents, err)`` — ``contents`` is ``None`` on failure.
    """
    ...


def write(path: str, contents: str) -> tuple[bool, str | None]:
    """Write a UTF-8 file. Reloads any open tab for ``path``.

    Args:
        path: Absolute path to write to.
        contents: The file contents.

    Returns:
        ``(ok, err)`` — ``err`` is ``None`` on success.
    """
    ...


def exists(path: str) -> bool:
    """Test whether the file exists.

    Args:
        path: Absolute path to test.

    Returns:
        ``True`` if the file exists.
    """
    ...


def delete(path: str) -> tuple[bool, str | None]:
    """Delete the file. Closes its tab if open. Succeeds silently if absent.

    Args:
        path: Absolute path to delete.

    Returns:
        ``(ok, err)`` — ``err`` is ``None`` on success.
    """
    ...


def rename(src: str, to: str) -> tuple[bool, str | None]:
    """Rename or move a file. Closes its tab if open.

    Args:
        src: Source path. Named ``from`` in Lua.
        to: Destination path.

    Returns:
        ``(ok, err)`` — ``err`` is ``None`` on success.
    """
    ...


def copy(src: str, to: str, overwrite: bool = False) -> tuple[bool, str | None]:
    """Copy a file.

    Args:
        src: Source path. Named ``from`` in Lua.
        to: Destination path.
        overwrite: Pass ``True`` to overwrite an existing destination.

    Returns:
        ``(ok, err)`` — ``err`` is ``None`` on success.
    """
    ...


def mkdir(path: str) -> tuple[bool, str | None]:
    """Create the directory **and all missing parents**.

    Args:
        path: Directory path to create.

    Returns:
        ``(ok, err)`` — ``err`` is ``None`` on success.
    """
    ...


def list(dir: str, opts: ListOpts | None = None) -> list[str]:
    """List files in ``dir``.

    Args:
        dir: Directory to list.
        opts: Optional `ListOpts` controlling recursion and globbing.

    Returns:
        Absolute paths of the matching files.
    """
    ...


def findInFiles(root: str, pattern: str, opts: SearchOpts | None = None) -> list[SearchHit]:
    """Grep-style recursive search across every file under ``root``.

    Args:
        root: Directory to search beneath.
        pattern: The text (or regex, if ``opts.regex``) to match.
        opts: Optional `SearchOpts` controlling regex/case/glob.

    Returns:
        A list of `SearchHit`.
    """
    ...
