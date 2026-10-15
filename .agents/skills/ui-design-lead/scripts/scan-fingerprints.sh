#!/usr/bin/env bash
# scan-fingerprints.sh — fast read on AI-slop tells in a frontend codebase.
# Read-only. No writes, no network. Usage: scan-fingerprints.sh [path ...]  (default: .)
#
# It counts the design fingerprints that ui-design-lead's diagnosis.md glossary explains,
# prints up to 3 sample hits per category, and ends with a BREADTH (how many of the 15
# categories fired) and VOLUME read. Feed the output into the DIAGNOSIS "Findings" line —
# cite the specific categories that spiked, not just the totals.

set -u
paths=("$@"); [ ${#paths[@]} -eq 0 ] && paths=(".")

for p in "${paths[@]}"; do
  if [ ! -e "$p" ]; then echo "scan-fingerprints: no such path: $p" >&2; exit 2; fi
done

inc=(--include='*.tsx' --include='*.jsx' --include='*.ts' --include='*.js'
     --include='*.css' --include='*.scss' --include='*.less' --include='*.html'
     --include='*.vue' --include='*.svelte' --include='*.astro' --include='*.mdx')
exc=(--exclude-dir=node_modules --exclude-dir=.next --exclude-dir=dist --exclude-dir=build
     --exclude-dir=.git --exclude-dir=.svelte-kit --exclude-dir=.nuxt --exclude-dir=out
     --exclude-dir=coverage --exclude-dir=.turbo --exclude-dir=vendor)

total=0      # volume: capped sum of hit counts
cats=0       # breadth: how many distinct categories fired
bold() { printf '\033[1m%s\033[0m\n' "$1"; }

probe() { # label  pattern
  local label="$1" pat="$2" out n
  out=$(grep -rInE "${inc[@]}" "${exc[@]}" -e "$pat" "${paths[@]}" 2>/dev/null)
  report "$label" "$out"
}

report() { # label  newline-separated "file:line:text" hits
  local label="$1" out="$2" n
  n=$(printf '%s' "$out" | grep -c . 2>/dev/null || true)
  [ -z "$n" ] && n=0
  # Cap each category's contribution so one noisy tell (e.g. ✓ in every pricing row)
  # can't swamp the score. The displayed count is still the true one.
  local capped=$n; [ "$capped" -gt 20 ] && capped=20
  total=$((total + capped))
  [ "$n" -gt 0 ] && cats=$((cats + 1))
  if [ "$n" -gt 0 ]; then
    printf '  %-32s %4d\n' "$label" "$n"
    printf '%s\n' "$out" | head -3 | sed 's/^/       /'
  else
    printf '  %-32s %4d\n' "$label" 0
  fi
}

emoji_probe() { # emoji needs real Unicode handling — byte-oriented grep over-matches any
  # multibyte script (Coptic, CJK, etc.). Use perl with explicit pictographic ranges.
  if ! command -v perl >/dev/null 2>&1; then
    printf '  %-32s %s\n' "emoji in source" "(perl not found — check manually)"
    return
  fi
  local out
  out=$(find "${paths[@]}" \
          \( -type d \( -name node_modules -o -name .git -o -name dist -o -name build \
             -o -name .next -o -name .svelte-kit -o -name .nuxt -o -name out -o -name coverage \) -prune \) -o \
          \( -type f \( -name '*.tsx' -o -name '*.jsx' -o -name '*.ts' -o -name '*.js' \
             -o -name '*.css' -o -name '*.scss' -o -name '*.html' -o -name '*.vue' \
             -o -name '*.svelte' -o -name '*.astro' -o -name '*.mdx' \) -print0 \) 2>/dev/null \
        | xargs -0 perl -CSD -ne '
            print "$ARGV:$.:$_" if /[\x{1F000}-\x{1FAFF}\x{2600}-\x{27BF}\x{2B00}-\x{2BFF}\x{1F1E6}-\x{1F1FF}]/;
            close ARGV if eof;' 2>/dev/null)
  report "emoji in source" "$out"
}

bold "AI-slop fingerprint scan — ${paths[*]}"
echo

bold "Typography"
probe "Inter as a font"            "(font-?family[^;{}]*\bInter\b|fontFamily[^;{}]*\bInter\b|['\"]Inter['\",]|\bInter\b['\"]|\bfont-inter\b|--font-inter|\binter\.(className|variable|style)|Inter:wght|\{ ?Inter ?\})"
emoji_probe
probe "cliche marketing copy"      "\b(Elevate|Seamless(ly)?|Unleash|Supercharge|Game[- ]?changer|Next[- ]?[Gg]en|Delve|Effortless(ly)?|Revolutioniz|Empower your|Take (it|your) .* to the next level)\b"
probe "placeholder junk"           "(Lorem ipsum|John Doe|Jane Doe|Acme (Corp|Inc|Co\b)|example@example|Your Company Name)"

echo
bold "Color & surfaces"
probe "purple/indigo AI gradient"  "(from|via|to)-(purple|violet|fuchsia|indigo)-[0-9]|bg-gradient-to-[a-z]+ +from-(indigo|purple|violet|fuchsia)"
probe "pure black"                 "(#000000|#000\b|bg-black\b|text-black\b|rgb\(0, ?0, ?0\)|background:? *#000\b)"
probe "default gray hairline"      "border-(gray|slate|zinc|neutral|stone)-(200|300)\b"
probe "heavy generic shadow"       "\bshadow-(md|lg|xl|2xl)\b|box-shadow:[^;]*rgba\(0, ?0, ?0, ?0?\.[1-9]"

echo
bold "Layout"
probe "three equal cards"          "grid-cols-3\b|grid-template-columns:[^;]*repeat\(3,"
probe "h-screen / 100vh"           "\b(h-screen|min-h-screen)\b|height: ?100vh|min-height: ?100vh"
probe "centered blocks"            "\btext-center\b"
probe "flex percentage math"       "(w-\[[0-9]+%\]|width: ?calc\([0-9]|flex-basis: ?[0-9]+%)"

echo
bold "Motion & state"
probe "backdrop-blur usage"        "backdrop-blur|backdrop-filter: ?blur"
probe "outline-none (focus risk)"  "outline-none|outline: ?none"
probe "scroll-listener animation"  "addEventListener\(['\"]scroll['\"]"

echo
printf '\033[1mBREADTH: %d/15 categories fired   VOLUME: %d\033[0m  (per-category count capped at 20)\n' "$cats" "$total"
echo
if   [ "$cats" -ge 8 ] || [ "$total" -ge 90 ]; then
  echo "Read: heavy — slop across many categories. This is a whole-surface redesign, not one"
  echo "      targeted fix. Pick the redesign route in SKILL.md by artifacts + surface type."
elif [ "$cats" -ge 4 ] || [ "$total" -ge 35 ]; then
  echo "Read: moderate — note which categories fired; a few targeted refinements probably cover"
  echo "      it (spacing, type, color, copy). Confirm against the screenshot before deciding."
elif [ "$cats" -ge 1 ]; then
  echo "Read: light — likely one targeted refinement, or fold the fixes into whatever pass is planned."
else
  echo "Read: clean on these tells. Diagnose from the brief and the screenshots instead."
fi
echo
echo "(A category at 0 is not proof of quality, and a spike is not proof of a problem — dingbats"
echo " and centered text can be deliberate. The screenshot and the brief still decide.)"
