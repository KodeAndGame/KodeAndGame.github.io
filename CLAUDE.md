# KodeAndGame.github.io

Jekyll static site + Connections Board project.

## Project basics

- **Deploy:** push to `main` — GitHub Pages auto-deploys. No build step, plain JS only, no npm/node.
- **Run locally:** `bundle exec jekyll serve`
- **Branch convention:** PRs against `main`. Branch ruleset enforces: no force push, no deletion, PR required. CI must pass before merge. **Never commit directly to `main`** — always create a feature branch first.
- **CI:** `.github/workflows/ci.yml` — runs `jekyll build` on PRs to main. Add this as a required status check in the branch ruleset.
- **Puzzle data:** fetched daily by GHA (`.github/workflows/fetch-puzzle.yml`) and committed to `puzzles/YYYY-MM-DD.json`. Board loads local file first, falls back to corsproxy.io for dates not in repo. GHA runs free (public repo = unlimited minutes).

## Key decisions

- Connections Board uses **absolute positioning** for freeform drag-and-drop, not CSS grid. Don't suggest switching unless tackling the CSS grid rewrite item below.
- Puzzle words are cached in `localStorage` under `cx-puzzle-${date}` so NYT isn't hit on every refresh. Position reset must not clear puzzle cache.

## Backlog: connections-board.html

- [ ] **Fix stale positions bug** — validate saved tile positions fit current viewport before restoring; if any tile's `x`/`y` lands outside `window.innerWidth` / `window.innerHeight`, fall back to `defaultPositions()`. Was interrupted mid-implementation.
- [ ] **Animate tile reflow** — add `transition: left 0.2s, top 0.2s` to `.tile` during resize reflow; strip it during drag (`.dragging` already removes transitions). Makes viewport resize feel smooth instead of tiles teleporting.
- [ ] **Keyboard date navigation** — `←` / `→` arrow keys call the existing `prevBtn` / `nextBtn` click handlers. Two `keydown` listeners, trivial.
- [ ] **Dark mode** — `@media (prefers-color-scheme: dark)` block overriding CSS custom properties (`--bg`, `--dot-color`, `--tile-bg`, `--ink`, etc.). Design system is already variable-driven so mostly a re-skin.
- [ ] **CSS grid rewrite** — replace absolute positioning with CSS grid + drag-to-reorder (swap DOM order on drop). Eliminates `getLayout()` / `defaultPositions()` math; responsive sizing becomes automatic. Larger lift — treat as its own task.

## Backlog: site layout (_layouts/default.html)

- [ ] **Readability on dot grid** — dot grid background makes body text hard to read across all pages (index, posts, etc.). Connections Board has its own standalone layout (`layout: none`) and must not be changed. Fix options: tone down dot opacity, restrict dot grid to a decorative strip, or give the content column a solid/semi-opaque surface so prose sits on a clean background.
