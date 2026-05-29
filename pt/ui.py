"""``pt.ui`` — dialogs, the Output dock, and the dockable-widget system.

Everything user-facing: modal dialogs, the IDE's **Output** dock, and the
dockable-widget system you use to build a custom panel.

This is the biggest module, split into two halves:

- **Dialogs** — modal popups you can fire from anywhere. Every dialog is modal
  and synchronous: the call blocks until the user closes it, and cancelling
  returns ``None``. There are no callbacks for dialogs — they just return.
- **Dockable widgets** — long-lived panels you build once and reuse.
  `createWidget` returns a `PluginWidget` (a Qt ``QDockWidget`` you can drag,
  float, hide, or close). Widgets are owned by the engine and live until
  **Reload Plugins**.

.. tip::
   One widget object per plugin. Build the panel once in ``run()`` and store
   every child reference in ``local`` variables (or fields on a table) outside
   the function. ``run()`` only needs to call ``panel:show()`` on subsequent
   invocations.

.. warning::
   **Reload Plugins** destroys every dock the plugin opened. If your user has
   unsaved work in a `PluginTextArea`, that work is gone. Write it to disk (or
   the editor buffer) before relying on reload during development.

.. note::
   There is no automatic layout. Child widgets are placed with absolute pixel
   coordinates via ``setPosition(x, y)``; if you change a panel's size or a
   field's width you may need to nudge other coordinates too.

Examples:
    Multi-step interaction — ``choose``, ``prompt``, and ``confirm`` all run to
    completion before the next line of Lua executes::

        function run()
          local section = pt.ui.choose("Pick a section bank:", { "ROM0", "ROMX", "WRAM0", "HRAM" })
          if not section then return end
          local name = pt.ui.prompt("Symbol name:")
          if not name then return end
          if not pt.ui.confirm(string.format("Generate skeleton for %s in %s?", name, section)) then
            return
          end
          pt.editor.replaceSelection(string.format('SECTION "%s", %s\\n%s:\\n    ret\\n', name, section, name))
        end

    A persistent counter panel — the locals survive across ``run()`` calls, so
    re-opening the menu entry brings back the same panel and count::

        local panel

        function run()
          if panel then panel:show(); return end
          panel = pt.ui.createWidget("Counter")
          panel:setSize(220, 120)
          local label = panel:addLabel("Count: 0")
          label:setPosition(12, 12)
          local btn = panel:addButton("Increment")
          btn:setPosition(12, 50)
          local count = 0
          btn:onClick(function()
            count = count + 1
            label:setText("Count: " .. count)
          end)
          panel:show()
        end
"""

from __future__ import annotations

from typing import Callable

__docformat__ = "google"


# --------------------------------------------------------------------------- #
# Dialogs
# --------------------------------------------------------------------------- #

class PickFileOpts:
    """Options for `pickFile`."""

    save: bool  #: Show a Save dialog instead of Open. Default ``False``.
    dir: str  #: Initial directory the dialog opens in. Default ``""``.
    filters: str  #: Qt filter string, e.g. ``"GBA (*.gba);;All Files (*)"``. Default ``"All Files (*)"``.


def alert(msg: str, title: str | None = None) -> None:
    """Information box. Returns when the user clicks OK.

    Args:
        msg: The message to display.
        title: Optional window title.
    """
    ...


def confirm(msg: str, title: str | None = None) -> bool:
    """Yes/No question.

    Args:
        msg: The question to display.
        title: Optional window title.

    Returns:
        ``True`` if the user chose Yes.
    """
    ...


def prompt(label: str, default: str | None = None, title: str | None = None) -> str | None:
    """Single-line text input.

    Args:
        label: The prompt label.
        default: Optional pre-filled text.
        title: Optional window title.

    Returns:
        The entered text, or ``None`` if cancelled.
    """
    ...


def choose(label: str, items: list[str], title: str | None = None) -> str | None:
    """Pick one item from a list.

    Args:
        label: The prompt label.
        items: The options to choose from.
        title: Optional window title.

    Returns:
        The chosen item, or ``None`` if cancelled.
    """
    ...


def pickFile(opts: PickFileOpts | None = None) -> str | None:
    """Native file picker.

    Args:
        opts: Optional `PickFileOpts` controlling save mode, directory, filters.

    Returns:
        The chosen path, or ``None`` if cancelled.
    """
    ...


def pickFolder(label: str | None = None) -> str | None:
    """Native folder picker.

    Args:
        label: Optional dialog label.

    Returns:
        The chosen folder, or ``None`` if cancelled.
    """
    ...


def notify(msg: str) -> None:
    """Append a line to the **Output** dock under the **Plugins** channel.

    The preferred way to report progress and success — it doesn't interrupt the
    user the way `alert` does.

    Args:
        msg: The line to append.
    """
    ...


def createWidget(title: str) -> "PluginWidget":
    """Create a dockable panel attached to the main window.

    Store the returned widget in a ``local`` outside ``run()`` so the same
    instance is reused when the user re-opens the menu entry.

    Args:
        title: The dock header title.

    Returns:
        A `PluginWidget`.
    """
    ...


# --------------------------------------------------------------------------- #
# Dockable widgets
# --------------------------------------------------------------------------- #

class PluginWidget:
    """A dockable panel (Qt ``QDockWidget``) created by `createWidget`.

    Child controls are added with the ``add*`` methods and placed with absolute
    coordinates — there is no layout system.
    """

    def setSize(self, w: int, h: int) -> None:
        """Set the initial content area size."""
        ...

    def setTitle(self, s: str) -> None:
        """Change the dock header title."""
        ...

    def show(self) -> None:
        """Show the dock."""
        ...

    def hide(self) -> None:
        """Hide the dock."""
        ...

    def close(self) -> None:
        """Close the dock."""
        ...

    def addLabel(self, text: str) -> "PluginLabel":
        """Add a static text label.

        Args:
            text: The initial label text.

        Returns:
            A `PluginLabel`.
        """
        ...

    def addButton(self, text: str) -> "PluginButton":
        """Add a clickable button.

        Args:
            text: The button label.

        Returns:
            A `PluginButton`.
        """
        ...

    def addLineEdit(self, default: str | None = None) -> "PluginLineEdit":
        """Add a single-line text input.

        Args:
            default: Optional initial text.

        Returns:
            A `PluginLineEdit`.
        """
        ...

    def addTextArea(self, default: str | None = None) -> "PluginTextArea":
        """Add a multi-line plain-text editor.

        Args:
            default: Optional initial text.

        Returns:
            A `PluginTextArea`.
        """
        ...

    def addSelection(self, placeholder: str | None = None) -> "PluginSelection":
        """Add a dropdown (combo box).

        Args:
            placeholder: Optional placeholder text.

        Returns:
            A `PluginSelection`.
        """
        ...

    def addImage(self, path: str | None = None) -> "PluginImage":
        """Add an image pane (PNG, JPG, GIF, BMP, SVG).

        Args:
            path: Optional initial image path.

        Returns:
            A `PluginImage`.
        """
        ...


class PluginLabel:
    """A static text label inside a `PluginWidget`.

    The only child widget that exposes `setVisible`. To hide a group of other
    controls, move them off-screen with ``setPosition(-9999, -9999)`` and
    restore the coordinates later.
    """

    def setPosition(self, x: int, y: int) -> None:
        """Move the label (absolute pixels from the dock's top-left)."""
        ...

    def setSize(self, w: int, h: int) -> None:
        """Resize the label."""
        ...

    def setText(self, s: str) -> None:
        """Set the display text."""
        ...

    def text(self) -> str:
        """Read the current text.

        Returns:
            The label text.
        """
        ...

    def setVisible(self, v: bool) -> None:
        """Show or hide the label."""
        ...


class PluginButton:
    """A clickable button inside a `PluginWidget`."""

    def setPosition(self, x: int, y: int) -> None:
        """Move the button (absolute pixels from the dock's top-left)."""
        ...

    def setSize(self, w: int, h: int) -> None:
        """Resize the button."""
        ...

    def setText(self, s: str) -> None:
        """Set the button label."""
        ...

    def onClick(self, fn: Callable[[], None]) -> None:
        """Connect a Lua callback, called with no arguments on click.

        Args:
            fn: The click handler.
        """
        ...


class PluginLineEdit:
    """A single-line text input inside a `PluginWidget`."""

    def setPosition(self, x: int, y: int) -> None:
        """Move the input field (absolute pixels from the dock's top-left)."""
        ...

    def setSize(self, w: int, h: int) -> None:
        """Resize the input field."""
        ...

    def setText(self, s: str) -> None:
        """Set the current text."""
        ...

    def text(self) -> str:
        """Read the current text.

        Returns:
            The field contents.
        """
        ...

    def setPlaceholder(self, s: str) -> None:
        """Set placeholder/hint text shown when empty."""
        ...


class PluginTextArea:
    """A multi-line plain-text editor inside a `PluginWidget`."""

    def setPosition(self, x: int, y: int) -> None:
        """Move the text area (absolute pixels from the dock's top-left)."""
        ...

    def setSize(self, w: int, h: int) -> None:
        """Resize the text area."""
        ...

    def setText(self, s: str) -> None:
        """Replace all text."""
        ...

    def text(self) -> str:
        """Read all text.

        Returns:
            The text area contents.
        """
        ...

    def append(self, s: str) -> None:
        """Append ``s`` to the end (followed by a newline)."""
        ...


class PluginImage:
    """An image pane inside a `PluginWidget`."""

    def setPosition(self, x: int, y: int) -> None:
        """Move the image pane (absolute pixels from the dock's top-left)."""
        ...

    def setSize(self, w: int, h: int) -> None:
        """Resize the pane. The image is rescaled preserving aspect ratio."""
        ...

    def setImage(self, path: str) -> bool:
        """Load an image from disk.

        Args:
            path: Path to the image file.

        Returns:
            ``False`` if the file can't be read.
        """
        ...

    def imagePath(self) -> str:
        """Path of the currently loaded image.

        Returns:
            The image path, or ``""`` if none is loaded.
        """
        ...

    def clear(self) -> None:
        """Unload the current image."""
        ...


class PluginSelection:
    """A dropdown (combo box) inside a `PluginWidget`."""

    def setPosition(self, x: int, y: int) -> None:
        """Move the dropdown (absolute pixels from the dock's top-left)."""
        ...

    def setSize(self, w: int, h: int) -> None:
        """Resize the dropdown."""
        ...

    def addItem(self, s: str) -> None:
        """Append one option."""
        ...

    def setItems(self, items: list[str]) -> None:
        """Replace all options."""
        ...

    def clear(self) -> None:
        """Remove all options."""
        ...

    def count(self) -> int:
        """Number of options.

        Returns:
            The option count.
        """
        ...

    def currentIndex(self) -> int:
        """1-based index of the selected option.

        Returns:
            The selected index, or ``0`` when empty.
        """
        ...

    def currentText(self) -> str:
        """Display text of the selected option.

        Returns:
            The selected option's text.
        """
        ...

    def setCurrentIndex(self, i: int) -> None:
        """Select by 1-based index."""
        ...

    def setCurrentText(self, s: str) -> None:
        """Select by display text."""
        ...

    def onChange(self, fn: Callable[[int, str], None]) -> None:
        """Connect a callback fired when the selection changes.

        Args:
            fn: Handler called with ``(index, text)``.
        """
        ...
