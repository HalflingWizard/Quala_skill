#!/usr/bin/env python3
"""Validate subtheme Markdown examples against theme JSON quote text."""

import argparse
import json
from pathlib import Path

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(items, **kwargs):
        return items


def read_examples(block_lines):
    examples = []
    i = 0
    while i < len(block_lines):
        line = block_lines[i]
        if line.startswith("**Example:** ") or line.startswith("**Additional Example "):
            value = line.split(":** ", 1)[1]
            if value.startswith('"'):
                value = value[1:]
            i += 1
            while i < len(block_lines) and block_lines[i] and not block_lines[i].startswith("**") and not block_lines[i].startswith("### "):
                value += "\n" + block_lines[i]
                i += 1
            if value.endswith('"'):
                value = value[:-1]
            examples.append(value.replace('\\"', '"'))
            continue
        i += 1
    return examples


def read_blocks(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    blocks = []
    i = 0
    while i < len(lines):
        if not lines[i].startswith("### "):
            i += 1
            continue
        name = lines[i][4:]
        j = i + 1
        while j < len(lines) and not lines[j].startswith("### "):
            j += 1
        blocks.append((name, read_examples(lines[i:j])))
        i = j
    return blocks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_theme_dir", type=Path)
    parser.add_argument("output_subtheme_dir", type=Path)
    parser.add_argument("--phase", choices=("round1", "round2"), required=True)
    args = parser.parse_args()

    errors = []
    theme_files = sorted(args.source_theme_dir.glob("*.json"))
    for source_path in tqdm(theme_files, desc="validating themes"):
        output_path = args.output_subtheme_dir / f"{source_path.stem}.md"
        if not output_path.exists():
            errors.append(f"missing output {output_path}")
            continue
        data = json.loads(source_path.read_text(encoding="utf-8"))
        quotes = [item.get("quote_text", "") for item in data.get("datapoints", [])]
        blocks = read_blocks(output_path)
        for name, examples in blocks:
            expected = 3 <= len(examples) <= 5 if args.phase == "round1" else len(examples) == 5
            if not expected:
                errors.append(f"{output_path} subtheme {name!r} has {len(examples)} examples")
            for example in examples:
                if not any(example in quote for quote in quotes):
                    errors.append(f"{output_path} subtheme {name!r} has a non-source example {example[:80]!r}")

    if errors:
        print("VALIDATION FAILED")
        print("\n".join(errors))
        return 1
    print(f"VALIDATION PASSED for {len(theme_files)} theme files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
