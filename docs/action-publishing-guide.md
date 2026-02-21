# Publishing BreakPoint Evaluate to GitHub Marketplace

## Prerequisites

- Public repository
- Repository owned by you or an organization
- `action.yml` at repo root (or in action subdirectory)
- README with usage and inputs documented

## 1. Tagging and Versioning

### Best practice: semantic version tags

Use `v1`, `v1.0`, `v1.0.0` style tags. Users pin versions for stability.

```bash
# Create and push a release tag
git tag -a v1 -m "BreakPoint Evaluate Action v1"
git push origin v1
```

### Major vs minor vs patch

- **v1**, **v2**: Major – breaking input/output changes
- **v1.1**: Minor – new optional inputs, backward compatible
- **v1.0.1**: Patch – bug fixes, no behavior change

**Recommendation:** Start with `v1` for the first Marketplace release. Use `v1` as the floating tag users pin to; create `v1.0.0` if you want strict semver.

```bash
# First release
git tag -a v1 -m "Initial Marketplace release"
git push origin v1
```

## 2. Publish to Marketplace

1. **Releases:** Go to your repo → **Releases** → **Draft a new release**
2. **Tag:** Choose existing tag (e.g. `v1`) or create a new one
3. **Release title:** e.g. `BreakPoint Evaluate v1`
4. **Description:** Add changelog or link to docs
5. **Publish:** Click **Publish release**

6. **Marketplace:** Go to **Actions** tab → **Publish to Marketplace** (or visit `https://github.com/YOUR_ORG/YOUR_REPO/actions` and look for the publish prompt)

7. **Marketplace form:**
   - **Category:** Code quality, or Other
   - **Short description:** (max 72 chars) – from `action.yml` `description`
   - **Long description:** Markdown – use `docs/action-marketplace-README.md` content or your README
   - **Icon:** `shield` (from branding in action.yml)
   - **Color:** `red`
   - Accept Marketplace terms

## 3. After Publishing

- Action URL: `https://github.com/marketplace/actions/breakpoint-evaluate`
- Usage: `uses: YOUR_ORG/breakpoint-library@v1`
- Update README with correct org/repo in usage examples

## 4. Making Scripts Executable

Ensure `entrypoint.sh` is executable before committing:

```bash
git add --chmod=+x entrypoint.sh
git add action.yml entrypoint.sh
git commit -m "Add Marketplace-ready BreakPoint Evaluate action"
```

## 5. Directory Layout

For publishing from this repo, recommended layout:

```
breakpoint-library/
├── action.yml
├── entrypoint.sh
├── README.md
├── docs/
│   ├── action-marketplace-README.md
│   └── action-publishing-guide.md
├── breakpoint/
└── pyproject.toml
```

Users run the action; the action installs `breakpoint-ai` from PyPI. The action does not need the local `breakpoint/` source.
