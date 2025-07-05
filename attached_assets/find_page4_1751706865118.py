#!/usr/bin/env python3
import csv
import sys
import warnings
import logging
import bisect
import argparse
from collections import defaultdict

import pythonbible as bible

# ─── Configure Logging ───────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ─── Abbreviation Map ────────────────────────────────────────────────────────
BOOK_ABBREVS = {
    'Gen': 'Genesis',  'Ex': 'Exodus',     'Lev': 'Leviticus',
    'Num': 'Numbers',  'Deut': 'Deuteronomy','Josh': 'Joshua',
    'Judg': 'Judges',  'Ruth': 'Ruth',
    '1Sam': '1 Samuel','2Sam': '2 Samuel', '1Kings': '1 Kings',
    '2Kings': '2 Kings',
    # …add others as needed…
}

def expand_abbrev(ref_str):
    parts = ref_str.strip().split(' ', 1)
    book = parts[0]
    rest = parts[1] if len(parts) > 1 else ''
    full = BOOK_ABBREVS.get(book)
    return f"{full} {rest}".strip() if full else ref_str

# ─── Load Page Map with Spillover ───────────────────────────────────────────
def load_page_map(csv_path):
    """
    Reads CSV with columns: page,ref[,spill]
    Returns dict: verse_id -> set(pages).
    If 'spill' is truthy, the last verse also maps to page+1.
    """
    verse2pages = defaultdict(set)

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            page = int(row['page'])
            ref  = expand_abbrev(row['ref'])
            # detect spill flag (optional column)
            spill = str(row.get('spill','')).strip().lower() in ('1','true','yes','y')

            try:
                nrefs = bible.get_references(ref)
                vids  = bible.convert_references_to_verse_ids(nrefs)
            except Exception as e:
                warnings.warn(f"Skipping invalid ref {row['ref']!r}: {e}", UserWarning)
                logger.warning(f"Invalid ref skipped: {row['ref']} ({e})")
                continue

            # map every vid → this page (warn if it's a genuine overlap)
            for vid in vids:
                if page not in verse2pages[vid] and verse2pages[vid]:
                    warnings.warn(
                        f"Verse ID {vid} on page {page} also appears on pages "
                        f"{sorted(verse2pages[vid])}",
                        UserWarning
                    )
                    logger.warning(f"Overlap: vid {vid} on pages {sorted(verse2pages[vid])} & {page}")
                verse2pages[vid].add(page)

            # if spillover, also map the *last* vid to page+1
            if spill and vids:
                last_vid = vids[-1]
                next_pg  = page + 1
                verse2pages[last_vid].add(next_pg)
                #logger.info(f"Spillover: vid {last_vid} also mapped to page {next_pg}")

    return verse2pages

# ─── Lookup & Page‐Range Computation ─────────────────────────────────────────
def find_pages(verse2pages, ref_str):
    """
    Returns (sorted_page_list, warning_msg).
    If ref_str is invalid, sorted_page_list is None and warning_msg is the error.
    """
    ref = expand_abbrev(ref_str)
    try:
        nrefs = bible.get_references(ref)
        vids  = bible.convert_references_to_verse_ids(nrefs)
    except Exception as e:
        return None, f"Invalid reference format: {e}"

    if not vids:
        return [], "No verses parsed from reference."

    pages = set()
    missing = 0
    for vid in vids:
        if vid in verse2pages:
            pages.update(verse2pages[vid])
        else:
            missing += 1

    if not pages:
        return [], f"All {missing} verse(s) out of range."

    return sorted(pages), (None if missing==0 else f"{missing} verse(s) out of range.")

# ─── Command‐Line Interface ─────────────────────────────────────────────────
def process_input(arg,versemap):
    verse2pages = load_page_map(versemap)
    pages, warn = find_pages(verse2pages, arg)

    if pages is None:
        print(warn, file=sys.stderr)
        sys.exit(1)

    # Format the output range
    if len(pages) == 1:
        out = f"page {pages[0]}"
    else:
        start, end = pages[0], pages[-1]
        if end == start + len(pages) - 1:
            out = f"pages {start}-{end}"
        else:
            out = "pages " + ",".join(map(str, pages))

    if warn:
        print(f"Warning: {warn}", file=sys.stderr)
    return(f"{arg} → {out}")

def main():
    parser = argparse.ArgumentParser(
        description="Lookup Bible verse → page(s), with optional spillover support."
    )
    parser.add_argument('reference',
                        help='Scripture reference, e.g. "John 3:16-18"')
    parser.add_argument('-m','--map',
                        default='page_map.csv',
                        help='CSV file with columns page,ref[,spill]')
    args = parser.parse_args()

    print(process_input(args.reference,args.map))

if __name__ == '__main__':
    main()
