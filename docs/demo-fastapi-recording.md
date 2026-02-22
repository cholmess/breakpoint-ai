# Recording the FastAPI Demo GIF

Replace `docs/demo-fastapi.gif` with a 15–30 second terminal recording using **asciinema + agg**.

## Why asciinema + agg?

- Crisp, text-based output — no screen-capture lag or artifacts
- Small files (<1 MB easy); ideal for CLI demos
- Open-source; works on Mac, Windows, Linux

## One-time install

**asciinema:**

```bash
brew install asciinema   # macOS/Linux
# or
pip install asciinema   # if Homebrew has permission issues
```

**agg** (converts .cast → GIF):

```bash
brew install agg         # macOS (preferred if Homebrew works)
# or
cargo install agg        # if you have Rust
# or download a prebuilt binary: https://github.com/asciinema/agg/releases
```

If `brew` fails with permission errors, fix ownership first:
`sudo chown -R $(whoami) /opt/homebrew`

## Demo script (15–25 seconds)

**Important:** Resize your terminal to at least 35–40 rows before recording. A short terminal (e.g. 14 rows) will clip the output and the GIF will appear mostly blank.

From the repo root:

1. `cd examples/fastapi-llm-demo`
2. `make install` (wait for pip to finish)
3. `make good` → green PASS
4. (Optional) `make show-cost-diff` or `cat candidates/bad_tokens.json` — quick "what changed" moment
5. `make bad-tokens` → red BLOCK + reason ("Cost +68%")
6. `exit` or Ctrl+D to end recording

## Record and convert

From repo root:

```bash
asciinema rec docs/demo-fastapi.cast
cd examples/fastapi-llm-demo
# Run: make install → make good → make show-cost-diff → make bad-tokens → exit
# Ctrl+D to stop (from fastapi-llm-demo dir, or cd .. first)
```

Convert to GIF (from repo root):

```bash
agg --theme monokai --cols 95 --rows 40 docs/demo-fastapi.cast docs/demo-fastapi.gif
```

Or if you recorded from `examples/fastapi-llm-demo` and the cast is there:

```bash
cd examples/fastapi-llm-demo
agg --theme monokai demo-fastapi.cast ../../docs/demo-fastapi.gif
mv demo-fastapi.cast ../../docs/   # keep for future re-renders
```

## Agg options (tweak for readability/size)

- `--speed 0.9` — slightly slower playback
- `--font-size 18` — larger text
- `--cols 100 --rows 30` — fit terminal dimensions
- `--fps 10` — smooth but keeps file size down; use 8 if still too large

Example:

```bash
agg --theme monokai --speed 0.9 --font-size 18 --fps 10 docs/demo-fastapi.cast docs/demo-fastapi.gif
```

## Output

Save the GIF as `docs/demo-fastapi.gif`. Keep `docs/demo-fastapi.cast` for future re-renders. Commit:

```bash
git add docs/demo-fastapi.gif docs/demo-fastapi.cast
git commit -m "Add terminal demo GIF showing cost regression block"
```
