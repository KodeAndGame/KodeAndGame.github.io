# KodeAndGame.github.io

Jekyll static site + Connections Board project.

## Backlog: connections-board.html

- [ ] **Fix stale positions bug** — validate saved tile positions fit current viewport before restoring; if any tile's `x`/`y` lands outside `window.innerWidth` / `window.innerHeight`, fall back to `defaultPositions()`. Was interrupted mid-implementation.
- [ ] **Animate tile reflow** — add `transition: left 0.2s, top 0.2s` to `.tile` during resize reflow; strip it during drag (`.dragging` already removes transitions). Makes viewport resize feel smooth instead of tiles teleporting.
- [ ] **Keyboard date navigation** — `←` / `→` arrow keys call the existing `prevBtn` / `nextBtn` click handlers. Two `keydown` listeners, trivial.
- [ ] **Dark mode** — `@media (prefers-color-scheme: dark)` block overriding CSS custom properties (`--bg`, `--dot-color`, `--tile-bg`, `--ink`, etc.). Design system is already variable-driven so mostly a re-skin.
- [ ] **CSS grid rewrite** — replace absolute positioning with CSS grid + drag-to-reorder (swap DOM order on drop). Eliminates `getLayout()` / `defaultPositions()` math; responsive sizing becomes automatic. Larger lift — treat as its own task.
