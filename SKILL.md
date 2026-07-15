---
name: theme-quote-subthemes
description: Analyze theme JSON quote data in two approval-gated stages. First discover surprising, specific subthemes from raw quote text. After explicit user approval, add four more exact source quotes to every approved subtheme. Use for Reddit quote datasets or similar theme-specific JSON data with datapoints and quote_text fields.
---

# Theme Quote Subthemes

Use this skill when the input is a JSON file or directory of theme JSON files. Each file should contain a theme name and a `datapoints` array with `quote_text` values. Treat each `quote_text` as an individual quote, not as a full post.

## Workflow

### Round one, discover subthemes

1. Identify the input JSON files. If a directory is supplied, sort files by ascending datapoint count. Preserve the input file names and use the theme name from each JSON file for output routing.
2. Extract only `quote_text` from `datapoints`. Put one quote per line in the prompt corpus. Do not give agents topic labels, primary topics, keywords, or other metadata. Tell agents to infer patterns from raw quotes only.
3. Use three agents concurrently at a time. Assign one theme corpus to each agent. Ask each agent for three to five surprising, specific, useful subthemes. Reject common-sense themes such as generic annoyance, sleep effects, or cheating.
4. Require each subtheme to contain a descriptive name, a standalone detailed description, and one exact example quote. Require the example to be one contiguous substring of a source quote. Preserve all spelling, punctuation, capitalization, spacing, and wording. Do not allow paraphrase or added ellipses.
5. Verify every returned example against the source quote corpus before writing. If an example is not an exact substring, ask the same agent for a replacement or select a replacement only after checking it against the source.
6. Write one Markdown file per theme to a sibling `data/subthemes` directory when the input uses `data/themes`. Use this format.

```markdown
# Theme Name — Subthemes

### Subtheme Name
**Description:** Detailed standalone description.
**Example:** "Exact source quote."
```

7. Stop after round one. Report the files created and ask for explicit approval to continue. Do not infer approval from praise, silence, or a request unrelated to continuing. Accept clear instructions such as `approve`, `continue`, or `find more examples`.

### Round two, add examples after approval

1. Re-read the source JSON and the round one Markdown files. Build one task per subtheme. Give each agent the subtheme name, description, current example, and raw quote corpus for its theme.
2. Use five agents concurrently at a time. Assign one subtheme to each agent. Ask each agent for exactly four additional quotes. Prefer longer quotes with concrete detail and context. Do not repeat the current example.
3. Require each additional quote to be an exact contiguous substring of a source quote. Do not accept normalized spelling, corrected grammar, changed capitalization, altered punctuation, added ellipses, or quotes combined from separate datapoints.
4. Verify all four returned quotes against the source JSON before editing. If any fail, request replacements and re-check them. Do not write unverified quotes.
5. Add the verified quotes under the existing example using `Additional Example 2` through `Additional Example 5`. Preserve the original subtheme name, description, and first example.
6. Run the bundled validator in round two mode. It must report five examples for every subtheme and exact substring matches for every example.

## Output and approval rules

- Keep theme routing separate from analysis. Agents in round one should see raw quotes only.
- Use the theme name only for file naming and result organization in round one.
- Keep subtheme descriptions understandable without the source dataset.
- Prefer surprising mechanisms, tensions, and teen experiences over broad topic labels.
- Never overwrite source JSON files.
- If the output directory already contains round one files, ask whether to replace them before starting a new round one. For round two, update the existing files in place.
- If a quote contains a newline, preserve it exactly in the Markdown output and validate it as one contiguous source substring.

## Validation

Run the bundled validator from the skill directory.

```bash
python3 scripts/validate_subthemes.py SOURCE_THEME_DIR OUTPUT_SUBTHEME_DIR --phase round1
python3 scripts/validate_subthemes.py SOURCE_THEME_DIR OUTPUT_SUBTHEME_DIR --phase round2
```

Use round one mode after discovery. Use round two mode after adding examples. Treat any validation failure as incomplete work.
