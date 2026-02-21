# ChatGPT Instructions: Create BreakPoint Blog Post

Copy and paste the following prompt to ChatGPT. Adjust tone/length as needed.

---

## Prompt

**Task:** Write a technical blog post titled **"How We Gate LLM Changes in CI"**. The post promotes BreakPoint, an open-source tool for evaluating AI/LLM outputs before they reach production.

**Target audience:** Developers and engineers who ship LLM-powered features and care about cost, PII leaks, and output drift.

**Length:** 5–8 minutes read (~800–1200 words).

**Structure:**

1. **Opening (problem):** Start with a relatable scenario: you swap an LLM model or tweak a prompt, the output *looks* fine, but then cost spikes, a phone number slips into the response, or the format breaks your downstream parser. No traditional tests catch this.

2. **The gap:** Explain briefly that unit tests don't cover non-deterministic model output, and manual review doesn't scale. You need a deterministic gate: compare candidate output vs. a baseline and block risky changes.

3. **Introduce BreakPoint:** 
   - One sentence: "BreakPoint is a local-first decision engine that compares baseline vs. candidate LLM output and returns `ALLOW`, `WARN`, or `BLOCK`."
   - Zero-config "Lite" mode: cost thresholds (WARN +20%, BLOCK +40%), PII detection (email, phone, credit card, SSN), drift detection. All deterministic from saved artifacts.
   - Runs locally—no SaaS, no API keys.
   - Exit codes: 0=ALLOW, 1=WARN, 2=BLOCK.

4. **Quick example:** Include a minimal CLI example:
   ```bash
   pip install breakpoint-ai
   breakpoint evaluate baseline.json candidate.json
   ```
   Show sample output: `STATUS: BLOCK` with reasons (e.g., cost +38%, phone number detected).

5. **CI integration:** Show the GitHub Action example (pre-merge gate). Include this YAML:
   ```yaml
   - name: BreakPoint Evaluate
     uses: cholmess/breakpoint-ai@v1
     with:
       baseline: baseline.json
       candidate: candidate.json
       fail_on: warn
   ```
   Explain: `fail_on: warn` means any WARN or BLOCK fails the workflow.

6. **Real-world scenarios:** Briefly mention 4 cases BreakPoint catches:
   - Cost regression after model swap
   - Structured output format regression
   - PII in candidate output
   - Small prompt change → big cost blowup

7. **Closing:** One paragraph: ship with confidence, all local and deterministic. Link to repo and PyPI. CTA: try it in 60 seconds with `pip install breakpoint-ai` and `make demo` (or the install_worthy examples).

**Tone:** Clear, practical, no hype. Focus on the problem and the solution.

**Links to include (fill in or keep placeholders):**
- Repo: https://github.com/cholmess/breakpoint-ai
- PyPI: https://pypi.org/project/breakpoint-ai/
- GitHub Action: https://github.com/marketplace/actions/breakpoint-evaluate

---

## Optional: Shorter Versions

**For LinkedIn/X thread (4–6 posts):**
- Post 1: The problem (cost spike, PII leak, format drift after model change)
- Post 2: Traditional tests don't catch it
- Post 3: BreakPoint in one line: local baseline vs. candidate, returns ALLOW/WARN/BLOCK
- Post 4: One YAML snippet (GitHub Action)
- Post 5: Link to repo + "try in 60 seconds"
- Post 6: (optional) One concrete scenario (e.g., cost +38% blocked)

**For Hacker News "Show HN" (title + first comment):**
- Title: "Show HN: BreakPoint – Gate LLM releases in CI (cost, PII, drift)"
- First comment: 2–3 sentences on what it does, link to repo, mention `make demo` or `pip install breakpoint-ai` for quick try.
