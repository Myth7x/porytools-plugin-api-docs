---
title: PoryTools
hide:
  - navigation
---

# PoryTools

A purpose-built IDE for the **pokered** and **pokecrystal** Game Boy
disassemblies — with an embedded RGBDS pipeline, project-aware editing,
a BGB debug bridge, and a **Lua plugin system** that lets you ship your
own tools right inside the IDE.

These pages are the developer reference for that plugin system.

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **Quickstart**

    ---

    Write a "Hello, plugin" in 30 seconds and watch it load.

    [:octicons-arrow-right-24: Get started](plugins/quickstart.md)

-   :material-book-open-page-variant:{ .lg .middle } **API reference**

    ---

    Every `pt.*` function the host gives your plugin, grouped by
    module.

    [:octicons-arrow-right-24: Browse the API](plugins/api/editor.md)

-   :material-folder-multiple:{ .lg .middle } **Multi-file plugins**

    ---

    Split a plugin across many files with plain `require()`.

    [:octicons-arrow-right-24: How it works](plugins/multi-file.md)

-   :material-puzzle:{ .lg .middle } **Cookbook**

    ---

    Copy-paste recipes for the patterns that come up over and over.

    [:octicons-arrow-right-24: Read recipes](plugins/cookbook.md)

</div>

## What a PoryTools plugin can do

- Read, edit, search, and save files in the active project — both
  through the editor buffer and directly on disk.
- Add a **dockable panel** with its own forms, buttons, text areas, and
  image previews to the IDE.
- Expose a menu entry under **Plugins**, optionally with a keyboard
  shortcut, that runs your code.
- Drive the IDE's own commands (save, undo, redo) and open or close
  tabs programmatically.

Plugins are written in **Lua 5.4**. Each one runs in its own sandboxed
environment so they don't leak globals into each other.

## Why a plugin and not a fork?

You probably don't need to recompile the IDE. Most repetitive
disassembly workflows — renaming a label, regenerating a constants
table, swapping a sprite, editing every species' base stats — are a
~30-line Lua file. The plugin folder lives in your roaming app data,
not in the IDE binary, so you can iterate without rebuilding anything.

## Where plugins live

| Platform | Location |
| -------- | -------- |
| Windows  | `%APPDATA%\PoryTools\PoryTools\plugins\` |
| Linux    | `~/.local/share/PoryTools/PoryTools/plugins/` |
| macOS    | `~/Library/Application Support/PoryTools/PoryTools/plugins/` |

Each plugin is a folder with at minimum a `manifest.json` and a
`plugin.lua`. Drop the folder in, click **Plugins → Reload Plugins**,
and the new entry appears in the menu.

## Project links

- [Source code on GitHub](https://github.com/Myth7x/porytools)
- [Issue tracker](https://github.com/Myth7x/porytools/issues)
- [Example plugins](https://github.com/Myth7x/porytools/tree/main/example-plugins)
