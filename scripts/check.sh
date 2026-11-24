#!/usr/bin/env bash
# vstack repository invariants. No model calls, runs in seconds. Exit 1 if any group fails.
#
#   identity    every commit author uses the public (non-company) e-mail, and so does git config
#   no-org      no company-specific term, internal host, ticket id, chat id, account id or e-mail domain
#   schemas     every JSON file parses; the example instance passes `vstack check`
#   frontmatter every SKILL.md has name + description
#   loop        every writer skill carries the validation loop (gate, min 2, max 5, reads house-rules)
#   glossary    every glossary key a skill references is defined in leadership-writing/glossary.md
#   triggers    every skill description wins its own prompts and loses the others (evals/triggers.json)
#   rules       every row in docs/RULES.md names an enforcer that exists
#   promo-lint  scripts/promo-lint.py fails the red promo-doc fixture and passes the green one
#   instance    the instance pointed at by VSTACK_INSTANCE (if set) is NOT inside this repo and is
#               NOT a remote of it, so private files cannot be committed here by mistake
set -euo pipefail
cd "$(dirname "$0")/.."
fail=0
say() { printf '%-12s %s\n' "$1" "$2"; }

# identity -------------------------------------------------------------------------------------
ALLOWED_EMAIL="${ALLOWED_EMAIL:-vikashagrawal1990@gmail.com}"
if git rev-parse -q --verify HEAD >/dev/null 2>&1; then
  bad=$(git log --format='%ae' | sort -u | grep -v "^${ALLOWED_EMAIL}$" || true)
  if [ -n "$bad" ]; then say identity "FAIL: commits by $bad"; fail=1; else say identity "ok ($(git rev-list --count HEAD) commits, all $ALLOWED_EMAIL)"; fi
fi
cur=$(git config user.email || true)
[ "$cur" = "$ALLOWED_EMAIL" ] || { say identity "FAIL: git config user.email is '$cur'"; fail=1; }

# no-org ---------------------------------------------------------------------------------------
# Union of the two source repos' denylists plus account-id, chat-id, doc-id and people-alias shapes.
# Add a term here the moment it appears in a private file; never the other way round.
# Generic shapes (round 1c): a bare 12-character document id (letters and digits mixed, no
# punctuation) and a bare people alias written `alias@` with no domain after it. Both are the
# forms a reviewer pastes into a results file by habit. evals/results/*.md is scanned with every
# pattern, the same as evals/fixtures/*.md.
DENY='amazon|quip|slackbot|midway|mwinit|phonetool|kingpin|chorus\.aws|pippin|taskei|krakenmare|cloudwatch|code\.amazon|w\.amazon|\.corp\.|@amazon\.com|isengard|brazil-build|gitfarm|git\.amazon|\bHV[123]\b|\bOV\b|Leadership Principle(s)? (demonstrated|language)|\bLP-anchored|\bSTO\b|\bL[4-8]\b(?!\s*(·|-|RUNNERS|harness|skills|kernel|instance|state|\d))|\bC0[0-9A-Z]{8,10}\b|\b[A-Z]{1,3}-?[0-9]{6,}\b|\b[0-9]{12}\b|\bP[0-9]{8,}\b|\bV[0-9]{8,}\b|\b(?=[A-Za-z0-9]{12}\b)(?=[A-Za-z]*[0-9])(?=[0-9]*[A-Za-z])[A-Za-z0-9]{12}\b|\b[a-z][a-z0-9]{1,15}@(?![a-z0-9-]+(\.[a-z0-9-]+)*\.[a-z]{2,})'
hits=$( { grep -rniIP "$DENY" --exclude-dir=.git --exclude-dir=scripts --exclude-dir=evals . ; \
          grep -niIP "$DENY" evals/fixtures/*.md evals/results/*.md scripts/*.py ; } \
  | grep -v 'glossary.md:.*for example `Leadership Principles`' \
  | grep -vP 'docs/social/.*\.py:.*(<path|markerWidth)' \
  | grep -vP 'scripts/check.sh:' || true)
if [ -n "$hits" ]; then say no-org "FAIL:"; echo "$hits" | cut -c1-160; fail=1; else say no-org "ok (no company-specific terms or ids)"; fi

# schemas --------------------------------------------------------------------------------------
for f in $(git ls-files '*.json'); do
  python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$f" || { say schemas "FAIL: $f"; fail=1; }
done
out=$(python3 bin/vstack check --instance example 2>/dev/null)
echo "$out" | grep -q '^invariants: PASS$' \
  || { say schemas "FAIL: example instance breaks the invariants (or vstack check printed no verdict)"; echo "$out" | sed 's/^/    /'; fail=1; }
[ $fail -eq 0 ] && say schemas "ok ($(echo "$out" | head -1))"

# frontmatter (Agent Skills spec, agentskills.io/specification) --------------------------------
# name: required, max 64 chars, lowercase letters, digits and hyphens, equals the directory name.
# description: required, non-empty, max 1024 chars.
# the block must parse as YAML: an unquoted value may not contain ': ' (GitHub shows
# "mapping values are not allowed in this context" and drops the whole frontmatter).
for f in skills/*/SKILL.md; do
  d=$(basename "$(dirname "$f")")
  head -1 "$f" | grep -q '^---$' || { say frontmatter "FAIL: $f no frontmatter"; fail=1; }
  n=$(grep -m1 '^name:' "$f" | sed 's/^name: *//; s/ *$//')
  [ "$n" = "$d" ] || { say frontmatter "FAIL: $f name '$n' must equal directory '$d'"; fail=1; }
  echo "$n" | grep -qE '^[a-z0-9]([a-z0-9-]{0,62}[a-z0-9])?$' || { say frontmatter "FAIL: $f name '$n' is not lowercase-hyphen, max 64"; fail=1; }
  desc=$(grep -m1 '^description:' "$f" | sed 's/^description: *//')
  [ -n "$desc" ] && [ ${#desc} -le 1024 ] || { say frontmatter "FAIL: $f description empty or over 1024 chars"; fail=1; }
done
out=$(python3 bin/vstack verify-skills --dirs skills --skills $(ls skills) 2>&1) \
  || { echo "$out" | grep '^  FAIL' | while read -r e; do say frontmatter "$e"; done; fail=1; }
[ $fail -eq 0 ] && say frontmatter "ok ($(ls skills/*/SKILL.md | wc -l | tr -d ' ') skills, spec-conformant names and descriptions, frontmatter parses)"

# loop -----------------------------------------------------------------------------------------
for s in write-talent-card write-work-summary write-promo-doc write-exec-update rewrite rewrite-and-validate; do
  f="skills/$s/SKILL.md"
  grep -q 'validate-writing' "$f" || { say loop "FAIL: $f never invokes validate-writing"; fail=1; }
  grep -qiE 'minimum of two passes|at least two|minimum of TWO' "$f" || { say loop "FAIL: $f has no minimum-pass rule"; fail=1; }
  grep -qiE 'maximum of five|maxRounds|cap(ped)? (the loop )?at five|five passes|at 5 total passes' "$f" || { say loop "FAIL: $f has no maximum-pass cap"; fail=1; }
  grep -q 'house-rules' "$f" || { say loop "FAIL: $f never reads house-rules"; fail=1; }
done
[ $fail -eq 0 ] && say loop "ok (6 writer skills: gate, min 2, max 5, house-rules)"

# glossary -------------------------------------------------------------------------------------
keys=$(grep -rhoE '`(principles|rating|levels|roles)\.[a-z_0-9]+`' skills --include=*.md | tr -d '`' | sort -u)
for k in $keys; do
  leaf=${k#*.}
  grep -q "^- \*\*${leaf}\*\*" skills/leadership-writing/glossary.md || { say glossary "FAIL: $k not defined in glossary.md"; fail=1; }
done
[ $fail -eq 0 ] && say glossary "ok ($(echo "$keys" | wc -l | tr -d ' ') glossary keys all defined)"

# triggers -------------------------------------------------------------------------------------
if out=$(python3 scripts/trigger-eval.py 2>&1); then say triggers "ok ($(echo "$out" | tail -1 | sed 's/trigger eval: //'))"; else say triggers "FAIL:"; echo "$out" | head -8; fail=1; fi

# rules ----------------------------------------------------------------------------------------
# every check.sh group and vstack subcommand named in docs/RULES.md exists in this repo
for ref in $(grep -oE 'check\.sh [a-z-]+' docs/RULES.md | awk '{print $2}' | sort -u); do
  grep -q "^# $ref " scripts/check.sh || { say rules "FAIL: docs/RULES.md names check.sh group '$ref' which does not exist"; fail=1; }
done
for sc in $(grep -oE '`vstack [a-z-]+' docs/RULES.md | awk '{print $2}' | sort -u); do
  grep -q "add_parser(\"$sc\")" bin/vstack || { say rules "FAIL: docs/RULES.md names vstack subcommand '$sc' which does not exist"; fail=1; }
done
[ $fail -eq 0 ] && say rules "ok ($(grep -c '^| ' docs/RULES.md) rows, every enforcer exists)"

# promo-lint -----------------------------------------------------------------------------------
# the red fixture must fail (exit 1, every lint-side class named in evals/results), the green must pass
# both run with their stage documents (round 4c): --impact-data turns on marker-propagation, --dates
# gives ordering-stamped the artifact dates. The red stage files must add failures (the three
# rules that read them), the green ones must add none, and the green must also pass without them.
stage() { echo "--impact-data evals/fixtures/promo-doc-$1.impact-data.md --dates evals/fixtures/promo-doc-$1.dates.csv"; }
if python3 scripts/promo-lint.py $(stage bad) evals/fixtures/promo-doc-bad.md >/tmp/promo-lint-bad.$$ 2>&1; then
  say promo-lint "FAIL: evals/fixtures/promo-doc-bad.md passed the lint, the red sample no longer trips it"; fail=1
fi
nbad=$(grep -c '^[a-z-]* ' /tmp/promo-lint-bad.$$ || true)
nfail=$(sed -n 's/^promo-lint: \([0-9]*\) failure.*/\1/p' /tmp/promo-lint-bad.$$)
nbare=$({ python3 scripts/promo-lint.py evals/fixtures/promo-doc-bad.md 2>&1 || true; } | sed -n 's/^promo-lint: \([0-9]*\) failure.*/\1/p')
[ "${nfail:-0}" -gt "${nbare:-0}" ] || { say promo-lint "FAIL: the red stage files (impact-data, dates) add no failure, marker-propagation or ordering-stamped stopped reading them"; fail=1; }
grep -q '^marker-propagation ' /tmp/promo-lint-bad.$$ || { say promo-lint "FAIL: marker-propagation did not fire on the red fixture with its impact-data file"; fail=1; }
grep -q '^ordering-stamped ' /tmp/promo-lint-bad.$$ || { say promo-lint "FAIL: ordering-stamped did not fire on the red fixture with its dates file"; fail=1; }
grep -q '^dates-printed-match-csv ' /tmp/promo-lint-bad.$$ || { say promo-lint "FAIL: dates-printed-match-csv did not fire on the red fixture with its dates file"; fail=1; }
grep -q '^warning dates-csv-coverage ' /tmp/promo-lint-bad.$$ || { say promo-lint "FAIL: dates-csv-coverage did not warn on the red fixture's dated link with no csv row"; fail=1; }
grep -q '^warning headline-no-identifier ' /tmp/promo-lint-bad.$$ || { say promo-lint "FAIL: headline-no-identifier did not warn on the red fixture's Headline with a review id"; fail=1; }
for args in "$(stage good)" ""; do
  if ! out=$(python3 scripts/promo-lint.py $args evals/fixtures/promo-doc-good.md 2>&1); then
    say promo-lint "FAIL: evals/fixtures/promo-doc-good.md (args: ${args:-none})"; echo "$out" | sed 's/^/    /'; fail=1
  fi
  echo "$out" | grep -q '^warning ' && { say promo-lint "FAIL: evals/fixtures/promo-doc-good.md carries a warning (args: ${args:-none})"; echo "$out" | grep '^warning ' | sed 's/^/    /'; fail=1; }
done
rm -f /tmp/promo-lint-bad.$$
# the flattened red fixture (pre-template shape) must be measured per story through the fallback
flat=$(python3 scripts/promo-lint.py evals/fixtures/promo-doc-bad.flat.md 2>&1 || true)
echo "$flat" | head -1 | grep -q '^shape: fallback$' \
  || { say promo-lint "FAIL: evals/fixtures/promo-doc-bad.flat.md did not print 'shape: fallback' first"; fail=1; }
echo "$flat" | grep -q '^story-length ' \
  || { say promo-lint "FAIL: the fallback did not measure the long story in promo-doc-bad.flat.md"; fail=1; }
# the copy check (round 3b) reports the known 8-word run the red fixture shares with the fictional
# feedback file, and nothing for the green fixture, whose provider words sit only in quote lines and
# the Feedback section the check skips by rule
fb=evals/fixtures/promo-doc-copycheck-feedback.md
if python3 scripts/promo-copycheck.py evals/fixtures/promo-doc-bad.md "$fb" >/tmp/promo-copy-bad.$$ 2>&1; then
  say promo-lint "FAIL: promo-copycheck.py found no run between promo-doc-bad.md and $fb"; fail=1
fi
nruns=$(grep -c 'word run:' /tmp/promo-copy-bad.$$ || true); rm -f /tmp/promo-copy-bad.$$
if ! out=$(python3 scripts/promo-copycheck.py evals/fixtures/promo-doc-good.md "$fb" 2>&1); then
  say promo-lint "FAIL: promo-copycheck.py found a run in promo-doc-good.md"; echo "$out" | sed 's/^/    /'; fail=1
fi
[ $fail -eq 0 ] && say promo-lint "ok (red fixture fails with $nbad lines and $nfail failures, $nbare failures without its stage files, green fixture 0 failures and 0 warnings with and without, flattened red fixture linted through the fallback, copy check $nruns run(s) on red and 0 on green)"

# instance -------------------------------------------------------------------------------------
if [ -n "${VSTACK_INSTANCE:-}" ]; then
  inst=$(cd "$VSTACK_INSTANCE" && pwd -P); here=$(pwd -P)
  case "$inst" in "$here"|"$here"/*) say instance "FAIL: instance $inst is inside this repo"; fail=1;; esac
  if git remote -v | grep -q "$inst"; then say instance "FAIL: instance is a git remote of this repo"; fail=1; fi
  if git -C "$inst" remote -v 2>/dev/null | grep -qiE 'github\.com|gitlab\.com|bitbucket'; then
    say instance "FAIL: instance has a public git remote"; fail=1
  fi
  [ $fail -eq 0 ] && say instance "ok ($inst is outside this repo and has no public remote)"
else
  say instance "skipped (VSTACK_INSTANCE not set)"
fi
exit $fail
