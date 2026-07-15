# Theme Quote Subthemes — opencode Skill

An [opencode](https://opencode.ai) skill for analyzing theme JSON quote data in two approval-gated stages:

1. **Discover subthemes** — Extract surprising, specific subthemes from raw quote text (3–5 per theme, with one exact example quote each)
2. **Add examples** — After explicit approval, find 4 additional exact source quotes per approved subtheme (5 total per subtheme)

Designed for Reddit quote datasets or similar theme-specific JSON data with `datapoints` arrays containing `quote_text` fields.

---

## Quick Start

```bash
# Install opencode if you haven't
curl -fsSL https://opencode.ai/install | bash

# Add this skill to your opencode config
opencode skill add https://github.com/YOUR_USERNAME/Quala_skill

# Or add locally
opencode skill add /path/to/Quala_skill
```

---

## Input Format

Place theme JSON files in `data/themes/`. Each file must contain:

```json
{
  "theme_name": "Theme Name",
  "datapoints": [
    { "quote_text": "First quote text here" },
    { "quote_text": "Second quote text here" }
  ]
}
```

- Each `datapoint` has a `quote_text` field (one quote per datapoint)
- If passing a directory, files are processed in ascending datapoint count order
- Filenames and `theme_name` are preserved for output routing

---

## Workflow

### Round 1 — Discover Subthemes

```bash
# In opencode chat:
use theme-quote-subthemes on data/themes/
```

What happens:
1. Three agents run concurrently, one theme each
2. Each agent reads raw `quote_text` only (no topic labels, keywords, or metadata)
3. Each returns 3–5 **surprising, specific, useful** subthemes (no generic themes like "annoyance" or "sleep issues")
3. Each subtheme gets: descriptive name, standalone description, **one exact source quote**
4. Markdown files written to `data/subthemes/{theme_name}.md`:

```markdown
# Theme Name — Subthemes

### Subtheme Name
**Description:** Detailed standalone description.
**Example:** "Exact source quote with original spelling, punctuation, capitalization."
```

5. **Stops and asks for explicit approval** (`approve`, `continue`, or `find more examples`)

---

### Round 2 — Add Examples (after approval)

```bash
# In opencode chat after approval:
approve
# or
continue
```

What happens:
1. Five agents run concurrently, one subtheme each
2. Each agent receives: subtheme name, description, current example, full quote corpus
3. Each returns **4 additional exact quotes** (longer, concrete, contextual preferred)
3. All 5 quotes verified as exact contiguous substrings of source quotes
4. Markdown updated in place with `Additional Example 2` … `Additional Example 5`
5. Validator runs automatically

Output format:

```markdown
### Subtheme Name
**Description:** Detailed standalone description.
**Example:** "Original exact source quote."
**Additional Example 2:** "Second exact source quote."
**Additional Example 3:** "Third exact source quote."
**Additional Example 4:** "Fourth exact source quote."
**Additional Example 5:** "Fifth exact source quote."
```

---

## Validation

Run the bundled validator from the skill directory:

```bash
# After round 1
python3 scripts/validate_subthemes.py data/themes data/subthemes --phase round1

# After round 2
python3 scripts/validate_subthemes.py data/themes data/subthemes --phase round2
```

**Round 1 checks:**
- Each subtheme has 3–5 examples
- Every example is an exact substring of a source `quote_text`

**Round 2 checks:**
- Every subtheme has exactly 5 examples
- Every example is an exact substring of a source `quote_text`

Any failure = incomplete work.

---

## Output Structure

```
data/
├── themes/           # INPUT: your theme JSON files
│   ├── theme_a.json
│   └── theme_b.json
└── subthemes/        # OUTPUT: generated markdown
    ├── theme_a.md    # Round 1 + Round 2 combined
    └── theme_b.md
```

- Round 1 writes new `.md` files (prompts before overwriting)
- Round 2 updates existing `.md` files in place
- Source JSON files are **never modified**

---

## Design Principles

- **Agents see raw quotes only** — no topic labels, keywords, or metadata in round 1
- **Exact quotes only** — exact substrings including spelling, punctuation, capitalization, newlines; no paraphrase, ellipses, or stitching
- **Surprising > generic** — prefer mechanisms, tensions, specific experiences over broad topic labels
- **Standalone descriptions** — subtheme descriptions must make sense without the source dataset
- **Explicit approval gate** — round 2 never runs without explicit `approve`/`continue`
- **Validation required** — both rounds must pass validation

---

## Validator Usage

```bash
python3 scripts/validate_subthemes.py SOURCE_THEME_DIR OUTPUT_SUBTHEME_DIR --phase round1
python3 scripts/validate_subthemes.py SOURCE_THEME_DIR OUTPUT_SUBTHEME_DIR --phase round2
```

Dependencies: Python 3.8+, `tqdm` (optional, for progress bar)

---

## Project Structure

```
Quala_skill/
├── SKILL.md                    # Skill definition (opencode reads this)
├── README.md                   # This file
├── agents/
│   └── openai.yaml             # OpenAI agent config
├── scripts/
│   └── validate_subthemes.py   # Validation script
└── data/                       # Your data goes here (gitignored)
    ├── themes/                 # Input JSON files
    └── subthemes/              # Output markdown files
```

---

## License

MIT — use freely.