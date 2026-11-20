from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")


def check_markdown(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")

    fence: tuple[str, int, int] | None = None
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = FENCE_RE.match(line)
        if not match:
            continue
        marker = match.group(1)
        if fence is None:
            fence = (marker[0], len(marker), line_number)
        elif marker[0] == fence[0] and len(marker) >= fence[1]:
            fence = None
    if fence is not None:
        errors.append(f"{path.relative_to(ROOT)}:{fence[2]}: bloc de code non referme")

    for target in LINK_RE.findall(text):
        parsed = urlsplit(target)
        if parsed.scheme or target.startswith("//") or not parsed.path:
            continue
        relative = unquote(parsed.path)
        destination = (path.parent / relative).resolve()
        try:
            destination.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"{path.relative_to(ROOT)}: lien sortant du depot: {target}")
            continue
        if not destination.exists():
            errors.append(f"{path.relative_to(ROOT)}: lien interne introuvable: {target}")
    return errors


def main() -> int:
    files = sorted(ROOT.rglob("*.md"))
    errors: list[str] = []
    for path in files:
        errors.extend(check_markdown(path))
    if errors:
        print("Échec du contrôle de documentation :", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    print(f"OK — {len(files)} fichiers Markdown vérifiés (liens internes et blocs de code).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
