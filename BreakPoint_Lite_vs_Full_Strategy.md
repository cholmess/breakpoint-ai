# BreakPoint Strategy Recap — Lite vs Full Mode

## 🎯 Core Idea

BreakPoint supports two operating modes:

- Lite Mode (default): Simple, opinionated, zero-friction safety layer
- Full Mode (advanced): Configurable, enforcement-ready policy engine

This structure balances:
- Indie developer adoption
- Power-user flexibility
- Future enterprise expansion

---

# 🟢 Lite Mode (Default)

Designed for indie devs and fast iteration.

## Characteristics
- No config required
- Runs locally
- Opinionated defaults
- Minimal cognitive load
- Immediate value

## Policies Included
- Cost delta
- PII detection
- Basic drift detection (length + similarity)

## CLI Usage
```
breakpoint evaluate baseline.json candidate.json
```

## Behavior
- Clear ALLOW / WARN / BLOCK output
- Deterministic aggregation
- Clean, readable terminal output
- Exit codes consistent with decision

---

# 🔵 Full Mode (Advanced)

Designed for power users and CI enforcement.

Enabled via:
```
breakpoint evaluate baseline.json candidate.json   --mode full   --config policies.json   --preset strict
```

## Additional Capabilities
- Output contract enforcement
- Latency thresholds
- Presets
- Environments
- Waivers
- Custom pricing models
- Strict mode (WARN → BLOCK)
- CI enforcement behavior

---

# 🔁 Aggregation Logic

Deterministic hierarchy:

BLOCK > WARN > ALLOW

If any policy returns BLOCK → Final = BLOCK  
Else if any policy returns WARN → Final = WARN  
Else → ALLOW

---

# 🧠 Product Identity

BreakPoint is:

"A local decision engine that tells developers whether an AI change is safe to ship."

Lite Mode → Safety tool  
Full Mode → Deployment gatekeeper

---

# 📌 Design Philosophy

- Keep Lite powerful but simple
- Hide complexity unless explicitly requested
- Avoid premature enterprise positioning
- Earn authority before enforcing pipelines

---

# 📈 Strategic Advantage

Two-mode structure provides:

- Clean onboarding
- Progressive disclosure
- Future extensibility
- Clear UX separation
- No need to remove features already built

---

# 🚀 Optional Evolution

Full mode may later require:
- Additional installation steps
- Optional plugins
- Separate configuration files
- CI-focused tooling

Lite remains the stable, frictionless entry point.

---

End of Strategy Document
