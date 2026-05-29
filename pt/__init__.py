"""PoryTools plugin API (``pt``).

PoryTools is a purpose-built IDE for the **pokered** and **pokecrystal** Game
Boy disassemblies, with a **Lua 5.4 plugin system**. Every host-provided
function a plugin can call lives under one global table called ``pt``, grouped
into six modules. This reference documents that surface.

.. note::

   This package is a set of typed Python *stubs*. The PoryTools plugin API is
   implemented in the IDE and called from **Lua**, not Python — these modules
   exist only so the API can be documented. Signatures use Python types
   (``str``, ``int``, ``bool``, ``list``, ``None``) as stand-ins for the Lua
   types (``string``, ``int``, ``bool``, ``string[]``, ``nil``).

The modules
===========

- `pt.editor` — the active editor buffer: read text, move the cursor, replace
  selections, find and replace, save.
- `pt.tabs` — open, close, and enumerate editor tabs.
- `pt.file` — read, write, copy, rename, and list files on disk; grep-style
  recursive search.
- `pt.project` — the open project: root path and file enumeration.
- `pt.ui` — native dialogs (alert, confirm, prompt, file picker) and the
  dockable widget system.
- `pt.cmd` — thin wrappers over the IDE's own menu commands (save, undo, redo).

Anatomy of a plugin
===================

A plugin is a folder dropped into the IDE's plugins directory, containing at
minimum a ``manifest.json`` (metadata: name, hotkey, entry script) and a
``plugin.lua`` that defines a global ``run()`` function::

    function run()
      pt.ui.alert("Hello from a PoryTools plugin!")
    end

The IDE runs each plugin in its own sandboxed ``sol::environment``, so globals
don't leak between plugins. The following Lua 5.4 standard libraries are
available: ``base``, ``string``, ``table``, ``math``, ``os``, ``io``,
``package``. ``debug`` and ``coroutine`` are intentionally not exposed.
"""

__docformat__ = "google"
