# Cookbook

Copy-paste recipes for patterns that come up in almost every plugin.
Each recipe is self-contained — drop it in `plugin.lua`, tweak the
specifics, reload.

## Persistent panel

Build the dock once, re-show it on subsequent invocations.

```lua
local panel

function run()
  if panel then panel:show(); return end

  panel = pt.ui.createWidget("My Panel")
  panel:setSize(360, 240)

  -- ... build child widgets here ...

  panel:show()
end
```

The `panel` local is **outside** `run()` so its value survives
between calls — the next time the user clicks the menu entry the
same dock comes back exactly where the user left it.

## Bail when there's no project

Most project-touching plugins should start with this:

```lua
function run()
  if not pt.project.isOpen() then
    pt.ui.alert("Open a project first.")
    return
  end
  -- ...
end
```

## Resolve a path relative to the project root

```lua
local function projectPath(rel)
  local root = pt.project.root()
  if not root then return nil end
  local guess = root .. "/" .. rel
  if pt.file.exists(guess) then return guess end
  return nil
end
```

Returns `nil` when the project isn't open **or** when the file
doesn't exist — so a single `if not p then return end` after the call
handles both.

## Read → transform → write

A safe in-place file edit:

```lua
local function rewrite(path, transform)
  local text, err = pt.file.read(path)
  if not text then
    pt.ui.alert("Read failed: " .. err)
    return false
  end

  local new = transform(text)
  if new == text then return true end       -- nothing to do

  local ok, werr = pt.file.write(path, new)
  if not ok then
    pt.ui.alert("Write failed: " .. werr)
    return false
  end
  return true
end
```

Now you can write transformations as plain functions:

```lua
rewrite(path, function(text)
  return text:gsub("\t", "    ")
end)
```

## Walk every file in the project, with progress

```lua
function run()
  local files = pt.project.files({ ext = { ".asm", ".inc" } })
  local count = #files
  local touched = 0

  for i, path in ipairs(files) do
    local ok = rewrite(path, function(text)
      return text:gsub("foo", "bar")
    end)
    if ok then touched = touched + 1 end
    pt.ui.notify(string.format("[%d/%d] %s", i, count, path))
  end

  pt.ui.alert(string.format("Updated %d of %d files.", touched, count))
end
```

`pt.ui.notify` writes to the **Output** dock without popping a
dialog, so the user can watch progress without each line interrupting
them.

## Confirm before destructive actions

```lua
function run()
  if not pt.ui.confirm("Reformat every .asm file in the project?") then
    return
  end
  -- ... do the work ...
end
```

`pt.ui.confirm` returns `true` only for an explicit Yes — Cancel and
the Escape key both return `false`.

## Section helper: show and hide a group of widgets

Only `PluginLabel` exposes `setVisible`. For other widget types,
moving them off-screen is the workaround. Wrap it in a small helper
and the rest of your code never sees the magic:

```lua
local OFFSCREEN_X, OFFSCREEN_Y = -9999, -9999
local Section = {}

function Section.new()
  return { entries = {} }
end

function Section.add(section, widget, x, y)
  widget:setPosition(x, y)
  table.insert(section.entries, { widget = widget, x = x, y = y })
end

function Section.show(section)
  for _, entry in ipairs(section.entries) do
    entry.widget:setPosition(entry.x, entry.y)
  end
end

function Section.hide(section)
  for _, entry in ipairs(section.entries) do
    entry.widget:setPosition(OFFSCREEN_X, OFFSCREEN_Y)
  end
end
```

Usage in your panel:

```lua
local statsSec = Section.new()
Section.add(statsSec, panel:addLabel("HP:"), 12, 40)
Section.add(statsSec, panel:addLineEdit(""), 100, 40)

local movesSec = Section.new()
Section.add(movesSec, panel:addTextArea(""), 12, 40)

-- Switch tabs:
Section.hide(statsSec)
Section.show(movesSec)
```

## Label + input "form" generator

Building the same label-and-input row a dozen times gets ugly fast.
Drive the layout from a data table instead:

```lua
local function buildForm(panel, defs, startY)
  local form = {}
  local y = startY
  for _, def in ipairs(defs) do
    local label = panel:addLabel(def.label .. ":")
    label:setPosition(12, y + 4)
    label:setSize(110, 22)

    local input = panel:addLineEdit("")
    input:setPosition(130, y)
    input:setSize(200, 26)

    form[def.key] = input
    y = y + 32
  end
  return form, y
end

-- Build:
local form, nextY = buildForm(panel, {
  { key = "name",  label = "Name" },
  { key = "hp",    label = "HP" },
  { key = "atk",   label = "Attack" },
}, 60)

-- Read:
local hp = tonumber(form.hp:text())
```

The Edit Pokémon example plugin's
[`buildForm`](https://github.com/Myth7x/porytools/blob/main/example-plugins/edit-pokemon/edit_pokemon/ui.lua)
is a generalised version of this pattern that also supports
dropdowns.

## Validate before saving

```lua
local function readInt(input, fieldName)
  local text = input:text():gsub("^%s+", ""):gsub("%s+$", "")
  if text == "" then return nil end
  local n = tonumber(text)
  if not n then
    pt.ui.alert(string.format("Field '%s' must be a number (got '%s').", fieldName, text))
    return false
  end
  return n
end

-- Caller:
local hp = readInt(form.hp, "HP")
if hp == false then return end       -- bad input, alerted, abort
local hpFinal = hp or fallback       -- empty: use previous value
```

Returning **three** sentinel states — `nil` for empty, `false` for
invalid (with an alert already shown), and a number for valid — keeps
the caller's logic compact: a single equality check against `false`
covers "abort", a single `or` covers "fall back".

## Re-read after writing

After saving, immediately re-read the file so the panel reflects
what's on disk:

```lua
local function saveStats(mon, edits)
  local ok, err = pt.file.write(mon.file, serialize(mon.parsed, edits))
  if not ok then pt.ui.alert("Write failed: " .. err); return end
  loadStats(mon)              -- refresh the form from disk
end
```

It's defensive against subtle bugs in your serializer, and shows
the user the canonical version of their data.

## Open a file in a tab

```lua
local ok, err = pt.tabs.open(path)
if not ok then pt.ui.alert("Open failed: " .. err) end
```

`open` focuses the existing tab if `path` is already open — clicking
a "Open ASM" button twice doesn't pile up duplicate tabs.

## Tag tab close on plugin shutdown

PoryTools destroys every dock you opened when **Reload Plugins**
fires, but doesn't close editor tabs your plugin opened. If you want
to clean those up:

```lua
local openedByUs = {}

local function openTracked(path)
  if not openedByUs[path] then
    pt.tabs.open(path)
    openedByUs[path] = true
  end
end

local function closeAll()
  for path in pairs(openedByUs) do
    pt.tabs.close(path)
    openedByUs[path] = nil
  end
end
```

Bind `closeAll` to a "Close" button or call it before re-opening a
different project.
