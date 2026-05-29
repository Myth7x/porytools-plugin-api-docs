# Error handling & reloading

PoryTools tries hard to make plugin failures **visible but
non-fatal**. A plugin that throws an exception, calls a function with
the wrong arguments, or has a syntax error will:

- Show a non-blocking message box describing the failure.
- Append the full Lua traceback to the **Output** dock under the
  **Plugins** channel.
- Never bring the IDE down.

This page covers how to handle errors inside your plugin, and how to
iterate quickly with the reload feature.

## The IDE's error path

Whenever the host calls your code — at load time, when the user
clicks your menu entry, or when a widget callback fires — that call
is wrapped in a Lua `pcall`. Any uncaught error is forwarded to the
**Plugins** output channel.

So `error("boom")` from inside a button callback won't crash
anything; it just shows up in the Output dock and the IDE stays
running.

## Returning errors instead of throwing

Most mutating `pt.*` functions return a **(ok, err)** tuple instead
of throwing:

```lua
local ok, err = pt.file.write(path, contents)
if not ok then
  pt.ui.alert("Save failed: " .. err)
  return
end
```

Read-style functions tend to return **(value, err)** with `value =
nil` on failure:

```lua
local text, err = pt.file.read(path)
if not text then
  pt.ui.alert("Read failed: " .. (err or "unknown"))
  return
end
```

This pattern means most user-visible errors are handled with a plain
`if` instead of `pcall`.

## When you want a hard error

If a precondition is genuinely broken — your manifest got out of sync
with your code, or a constant the plugin needs is missing — calling
`error("clear message")` is fine. The IDE will surface it the same
way it surfaces any other exception.

```lua
function run()
  if not pt.project.isOpen() then
    error("Open a project first.")
  end
  -- ...
end
```

`pt.ui.alert("message")` is the friendlier alternative when you'd
rather show the message and `return` than throw.

## Catching errors yourself

If you want to keep going after a failure (say, looping over many
files and recording the ones that failed), use `pcall`:

```lua
local failed = {}
for _, path in ipairs(paths) do
  local ok, err = pcall(processOneFile, path)
  if not ok then
    table.insert(failed, { path = path, err = err })
  end
end

if #failed > 0 then
  pt.ui.alert(string.format("%d files failed; see Output for details.", #failed))
  for _, f in ipairs(failed) do
    pt.ui.notify(f.path .. ": " .. f.err)
  end
end
```

## Reloading plugins

PoryTools has no plugin "watch mode" — instead, the **Reload
Plugins** action wipes every plugin sandbox and re-evaluates every
entry script from scratch.

You can trigger it from:

- **Plugins → Reload Plugins** in the menu bar.
- The **Reload** button in **Plugins → Plugin Settings…**.

Reloading is **destructive** — it closes any dock widget your plugin
opened, drops every cached require, and forgets every Lua local. If
you have a panel with edit state the user cares about, save it
somewhere durable (a file, the editor buffer) before relying on
reload during development.

## Workflow tips

!!! tip "Iterate fast"

    Keep `manifest.json` open in one editor pane, your script in
    another, and the IDE's **Output** dock pinned. Save your script
    → click **Reload Plugins** → trigger your menu entry → read the
    Output for any complaints.

!!! tip "Strict-mode catches typos"

    Lua silently treats undefined globals as `nil`. To catch typos
    early, add this at the top of your `plugin.lua` while you're
    developing:

    ```lua
    setmetatable(_ENV, { __index = function(_, key)
      error("undefined global: " .. tostring(key), 2)
    end })
    ```

    Remove it before shipping if you intentionally rely on
    auto-creating globals.

!!! warning "`safe_script_file` errors are loud"

    A parse error or top-level exception during load is reported in
    a message box. The plugin's menu entry won't appear because the
    sandbox never finished setting up. Fix the script and reload.
