# Example plugins

The repo ships with annotated examples under
[`example-plugins/`](https://github.com/Myth7x/porytools/tree/main/example-plugins).
Each one is meant to be read, copied, and modified. To try one
locally, copy its folder into your plugins directory (see [where
plugins live](index.md#where-plugins-live)) and click **Plugins →
Reload Plugins**.

## edit-pokemon

A beginner-friendly multi-file editor for pokered / pokecrystal
species data: base stats, moves, evolutions, egg moves, and sprites.

[**Source on GitHub**](https://github.com/Myth7x/porytools/tree/main/example-plugins/edit-pokemon){ .md-button }
[**In-folder dev guide**](https://github.com/Myth7x/porytools/blob/main/example-plugins/edit-pokemon/DOC.md){ .md-button }

### Layout

```
edit-pokemon/
├── manifest.json
├── plugin.lua                       -- entry, run(), controller
├── DOC.md                           -- developer guide
└── edit_pokemon/                    -- namespace folder
    ├── util.lua                     -- string + line helpers
    ├── constants.lua                -- loads constants/*.asm
    ├── pokemon.lua                  -- a Pokémon record + folder scan
    ├── base_stats_file.lua          -- parse / rewrite base_stats/*.asm
    ├── evos_attacks_file.lua        -- parse / rewrite evos_attacks.asm
    ├── egg_moves_file.lua           -- parse / rewrite egg_moves.asm
    └── ui.lua                       -- the dockable panel
```

### What it demonstrates

- **[Multi-file plugins](multi-file.md)** with one
  `require("edit_pokemon.X")` per concern.
- A **model / view / controller** split: file modules know nothing
  about widgets; the UI module knows nothing about ASM; `plugin.lua`
  wires them together.
- A **plain-table OOP** style (`Module.new(...)` factories returning
  data tables, plus `Module.method(self, ...)` functions). No
  metatables, no `self:` syntax.
- A **tolerant ASM parser** — walks line-by-line, records the line
  index of every recognised field, and rewrites only those lines.
  Comments and unknown directives survive unchanged.
- A **Section helper** that wraps the "move widgets off-screen to
  hide them" trick. See
  [Cookbook → Section helper](cookbook.md#section-helper-show-and-hide-a-group-of-widgets).
- **Forgiving gen detection** — counts the integers in the first
  base stats `db` line to tell pokered (5 stats) apart from
  pokecrystal (6 stats), with a fallback based on whether
  `egg_moves.asm` exists.

### Notable bits to read

| File | Why look |
| ---- | -------- |
| `plugin.lua` | The shape of a controller: one `state` table, one `run()`, save handlers wired to the UI's callback hooks. |
| `edit_pokemon/base_stats_file.lua` | A parser that records line indices, plus a serializer that only touches those lines. |
| `edit_pokemon/ui.lua` | The `Section` helper and the `buildForm` generator. |

### Try it

1. Open pokered or pokecrystal in PoryTools (**File → Open Project…**).
2. **Plugins → Gen 1/2 → Edit Pokémon**.
3. Pick a species in the dropdown, edit HP on the **Stats** tab,
   click **Save Stats**.
4. Use the **Sprites** tab's **Open base_stats .asm** button to jump
   to the file you just changed — confirm only the `db HP, …` line
   was rewritten.

---

## tools-edit-pokemon (legacy)

The original single-file version of the Edit Pokémon plugin. It does
the same thing as `edit-pokemon` above, but in **one 1,145-line
`plugin.lua`** with no module split. Keep it around if you want to
compare the two styles side-by-side, or fork it as a starting point
for a smaller plugin that doesn't need multiple files.

[**Source on GitHub**](https://github.com/Myth7x/porytools/tree/main/example-plugins/tools-edit-pokemon){ .md-button }

---

## Adding your own example

If you write a plugin you'd like to share, the easiest path is:

1. Drop it under `example-plugins/` in a fork of the repo.
2. Include a short `DOC.md` like the one in `edit-pokemon/` so
   readers can navigate it without launching the IDE.
3. Open a PR.

PRs adding small, focused examples are very welcome — even a 50-line
plugin that shows how to combine three `pt.*` calls is useful as
reference material for new plugin authors.
