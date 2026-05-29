"""``pt.editor`` — the currently focused editor tab.

Every function on `pt.editor` operates on whichever tab the user has the caret
in *right now*. If no tab is focused, the read functions return empty strings
and the write functions are a no-op.

All line and column numbers are **1-based**.

.. tip::
   For a whole-buffer transform, prefer reading the entire text into a Lua
   string with `text`, transforming it, and writing it back with `setText` in
   one go. That is one undo step and one redraw.

.. warning::
   Columns count **characters**, not bytes. ASCII assembly source is fine
   either way; if you start parsing UTF-8 text remember the distinction when
   you compute offsets.

.. danger::
   If no editor tab is focused, every reader returns an empty string and every
   writer is a no-op. Check `path` first if you need to know.

Examples:
    Uppercase every label identifier (one undo step via `setText`)::

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

    Wrap the current selection in a comment block::

        function run()
          local sel = pt.editor.selection()
          if sel == "" then return end
          pt.editor.replaceSelection("; -- BEGIN --\\n" .. sel .. "\\n; -- END --")
        end

    Jump to the first TODO comment. Passing ``from = 1`` forces the search to
    start at the beginning of the buffer regardless of the cursor::

        function run()
          local hit = pt.editor.find("TODO", { case = true, from = 1 })
          if hit then pt.editor.setCursor(hit.line, hit.col) end
        end

    Regex replace-all. Inside JSON-quoted Lua strings, ``\\b`` would be a
    backspace character — write ``\\\\b`` so it reaches the regex engine::

        function run()
          local n = pt.editor.replaceAll("\\\\bret\\\\b", "RET", { regex = true, case = true })
          pt.ui.notify(string.format("Replaced %d occurrences", n))
        end
"""

from __future__ import annotations

__docformat__ = "google"


class FindOpts:
    """Options for `find` and `replaceAll`."""

    regex: bool  #: Treat ``pattern`` as a `QRegularExpression <https://doc.qt.io/qt-6/qregularexpression.html>`_. Default ``False``.
    case: bool  #: Case-sensitive matching. Default ``False``.
    from_: int  #: 1-based **character offset** to start searching from. Spelled ``from`` in Lua. Defaults to the cursor position.


class FindResult:
    """A single match returned by `find`."""

    line: int  #: 1-based line number of the match.
    col: int  #: 1-based column of the match start.
    len: int  #: Length of the matched text in characters.
    pos: int  #: 1-based absolute character offset of the match.


def path() -> str | None:
    """Absolute path of the active tab.

    Returns:
        The path, or ``None`` for an untitled buffer.
    """
    ...


def text() -> str:
    """The entire buffer contents.

    Returns:
        The full text of the active buffer.
    """
    ...


def setText(s: str) -> bool:
    """Replace the entire buffer as a single undo step.

    Args:
        s: The new buffer contents.

    Returns:
        ``True`` on success.
    """
    ...


def selection() -> str:
    """The currently selected text.

    Returns:
        The selected text, or ``""`` if there is no selection.
    """
    ...


def replaceSelection(s: str) -> bool:
    """Replace the selection with ``s``.

    If nothing is selected, inserts ``s`` at the cursor.

    Args:
        s: The replacement text.

    Returns:
        ``True`` on success.
    """
    ...


def cursor() -> tuple[int, int]:
    """The caret position.

    Returns:
        ``(line, col)`` — both 1-based.
    """
    ...


def setCursor(line: int, col: int) -> bool:
    """Move the caret.

    Args:
        line: 1-based target line.
        col: 1-based target column.

    Returns:
        ``True`` on success.
    """
    ...


def insertAt(line: int, col: int, s: str) -> bool:
    """Insert ``s`` at the given position.

    Shifts existing text down; combine with `lineCount` to append at the end.

    Args:
        line: 1-based line to insert at.
        col: 1-based column to insert at.
        s: The text to insert.

    Returns:
        ``True`` on success.
    """
    ...


def deleteRange(l1: int, c1: int, l2: int, c2: int) -> bool:
    """Delete text between two positions.

    Args:
        l1: 1-based start line.
        c1: 1-based start column.
        l2: 1-based end line.
        c2: 1-based end column.

    Returns:
        ``True`` on success.
    """
    ...


def lineCount() -> int:
    """Number of lines in the buffer.

    Returns:
        The line count.
    """
    ...


def lineText(n: int) -> str:
    """Text of a given line.

    Args:
        n: 1-based line number.

    Returns:
        The text of line ``n``.
    """
    ...


def find(pattern: str, opts: FindOpts | None = None) -> FindResult | None:
    """Find the next match.

    Without ``from``, starts from the current cursor position.

    Args:
        pattern: The text (or regex, if ``opts.regex``) to search for.
        opts: Optional `FindOpts` controlling regex/case/start offset.

    Returns:
        A `FindResult`, or ``None`` if there is no match.
    """
    ...


def replaceAll(pattern: str, repl: str, opts: FindOpts | None = None) -> int:
    """Replace every match.

    Args:
        pattern: The text (or regex, if ``opts.regex``) to match.
        repl: The replacement text.
        opts: Optional `FindOpts` controlling regex/case/start offset.

    Returns:
        The number of replacements made.
    """
    ...


def save() -> tuple[bool, str | None]:
    """Save the active tab.

    Returns:
        ``(ok, err)`` — ``err`` is ``None`` on success.
    """
    ...
