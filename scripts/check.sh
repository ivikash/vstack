#!/usr/bin/env bash
# Repository invariants for the kernel. No model calls.
#   identity   every commit author uses the public e-mail
#   no-org     no company-specific term, internal host, ticket or channel id
#   schemas    every JSON file parses; example cells pass kernel check against the example graph
#   skills     every SKILL.md has frontmatter
set -euo pipefail
cd "$(dirname "$0")/.."
fail=0
say() { printf '%-10s %s\n' "$1" "$2"; }
ALLOWED_EMAIL="${ALLOWED_EMAIL:-vikashagrawal1990@gmail.com}"
if git rev-parse -q --verify HEAD >/dev/null 2>&1; then
  bad=$(git log --format='%ae' | sort -u | grep -v "^${ALLOWED_EMAIL}$" || true)
  [ -n "$bad" ] && { say identity "FAIL: commits by $bad"; fail=1; } || say identity "ok"
fi
cur=$(git config user.email || true)
[ "$cur" != "$ALLOWED_EMAIL" ] && { say identity "FAIL: user.email is '$cur'"; fail=1; }

DENY='amazon|quip|slackbot|midway|mwinit|phonetool|kingpin|chorus\.aws|pippin|taskei|krakenmare|cloudwatch|code\.amazon|w\.amazon|\.corp\.|@amazon\.com|\bHV[123]\b|\bOV\b|\bC0[0-9A-Z]{8,10}\b|\b[A-Z]{1,3}-?[0-9]{6,}\b'
hits=$(grep -rniE "$DENY" --exclude-dir=.git --exclude-dir=scripts . || true)
[ -n "$hits" ] && { say no-org "FAIL:"; echo "$hits" | cut -c1-160; fail=1; } || say no-org "ok"

for f in $(git ls-files '*.json' 2>/dev/null || find . -name '*.json' -not -path './.git/*'); do
  python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$f" || { say schemas "FAIL: $f"; fail=1; }
done
python3 bin/kernel check --graph graph/example.graph.json --cells cells/example >/dev/null || { say schemas "FAIL: example cells break the invariants"; fail=1; }
[ $fail -eq 0 ] && say schemas "ok"

for f in skills/*/SKILL.md; do
  head -1 "$f" | grep -q '^---$' && grep -q '^name:' "$f" && grep -q '^description:' "$f" || { say skills "FAIL: $f frontmatter"; fail=1; }
done
[ $fail -eq 0 ] && say skills "ok"
exit $fail
