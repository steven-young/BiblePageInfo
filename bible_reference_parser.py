import csv
import warnings
from collections import defaultdict
from typing import Dict, List, Optional, Set, Tuple
import pythonbible as bible

class BibleReferenceParser:
    """
    A class to parse Bible references and convert them to page numbers using accurate CSV data.
    Uses pythonbible library for robust reference parsing and CSV data for exact page mappings.
    """
    
    def __init__(self, csv_path: str = "page_map.csv"):
        """Initialize with CSV data file."""
        # Book abbreviation map for expansion (must be defined before loading page map)
        self.book_abbrevs = {
            'Gen': 'Genesis', 'Ex': 'Exodus', 'Lev': 'Leviticus',
            'Num': 'Numbers', 'Deut': 'Deuteronomy', 'Josh': 'Joshua',
            'Judg': 'Judges', 'Ruth': 'Ruth',
            '1Sam': '1 Samuel', '2Sam': '2 Samuel', '1Kings': '1 Kings',
            '2Kings': '2 Kings', '1Chron': '1 Chronicles', '2Chron': '2 Chronicles',
            'Ezra': 'Ezra', 'Neh': 'Nehemiah', 'Esth': 'Esther',
            'Job': 'Job', 'Ps': 'Psalms', 'Prov': 'Proverbs',
            'Eccl': 'Ecclesiastes', 'Song': 'Song of Solomon',
            'Isa': 'Isaiah', 'Jer': 'Jeremiah', 'Lam': 'Lamentations',
            'Ezek': 'Ezekiel', 'Dan': 'Daniel', 'Hos': 'Hosea',
            'Joel': 'Joel', 'Amos': 'Amos', 'Obad': 'Obadiah',
            'Jonah': 'Jonah', 'Mic': 'Micah', 'Nah': 'Nahum',
            'Hab': 'Habakkuk', 'Zeph': 'Zephaniah', 'Hag': 'Haggai',
            'Zech': 'Zechariah', 'Mal': 'Malachi',
            'Matt': 'Matthew', 'Mark': 'Mark', 'Luke': 'Luke', 'John': 'John',
            'Acts': 'Acts', 'Rom': 'Romans', '1Cor': '1 Corinthians',
            '2Cor': '2 Corinthians', 'Gal': 'Galatians', 'Eph': 'Ephesians',
            'Phil': 'Philippians', 'Col': 'Colossians', '1Thess': '1 Thessalonians',
            '2Thess': '2 Thessalonians', '1Tim': '1 Timothy', '2Tim': '2 Timothy',
            'Titus': 'Titus', 'Phlm': 'Philemon', 'Heb': 'Hebrews',
            'Jas': 'James', '1Pet': '1 Peter', '2Pet': '2 Peter',
            '1John': '1 John', '2John': '2 John', '3John': '3 John',
            'Jude': 'Jude', 'Rev': 'Revelation'
        }
        
        # Load the page map after abbreviations are defined
        self.verse2pages = self._load_page_map(csv_path)
    
    def _expand_abbrev(self, ref_str: str) -> str:
        """Expand abbreviated book names to full names."""
        # Handle full book names that need conversion
        if ref_str.startswith("Song of Solomon"):
            return ref_str.replace("Song of Solomon", "Song of Songs", 1)
        
        # Handle abbreviations
        parts = ref_str.strip().split(' ', 1)
        book = parts[0]
        rest = parts[1] if len(parts) > 1 else ''
        full = self.book_abbrevs.get(book)
        return f"{full} {rest}".strip() if full else ref_str
    
    def _load_page_map(self, csv_path: str) -> Dict[int, Set[int]]:
        """
        Load CSV data and create verse ID to page number mapping.
        Returns dict: verse_id -> set(pages).
        """
        verse2pages = defaultdict(set)
        
        try:
            with open(csv_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    page = int(row['page'])
                    ref = row['ref']  # Use CSV reference as-is for parsing
                    # Detect spill flag (optional column)
                    spill = str(row.get('spill', '')).strip().lower() in ('1', 'true', 'yes', 'y')
                    
                    try:
                        nrefs = bible.get_references(ref)
                        vids = bible.convert_references_to_verse_ids(nrefs)
                    except Exception as e:
                        warnings.warn(f"Skipping invalid ref {row['ref']!r}: {e}", UserWarning)
                        continue
                    
                    # Map every verse ID to this page
                    for vid in vids:
                        verse2pages[vid].add(page)
                    
                    # If spillover, also map the last verse to page+1
                    if spill and vids:
                        last_vid = vids[-1]
                        next_pg = page + 1
                        verse2pages[last_vid].add(next_pg)
        
        except FileNotFoundError:
            raise FileNotFoundError(f"Page map CSV file not found: {csv_path}")
        except Exception as e:
            raise Exception(f"Error loading page map: {e}")
        
        return verse2pages
    
    def parse_and_convert(self, reference: str) -> Dict:
        """
        Main method to parse a Bible reference and return page information.
        
        Args:
            reference (str): The Bible reference to parse
            
        Returns:
            Dict: Contains success status, page number(s), and reference details
        """
        try:
            pages, warning = self._find_pages(reference)
            
            if pages is None:
                return {
                    'success': False,
                    'error': warning
                }
            
            if not pages:
                return {
                    'success': False,
                    'error': f"Reference not found in page map: {warning}" if warning else "Reference not found in page map."
                }
            
            # Format page information
            is_range = len(pages) > 1
            page_start = pages[0]
            page_end = pages[-1]
            
            # Format the output range
            if len(pages) == 1:
                page_display = str(pages[0])
            else:
                start, end = pages[0], pages[-1]
                if end == start + len(pages) - 1:
                    page_display = f"{start}-{end}"
                else:
                    page_display = ",".join(map(str, pages))
            
            # Get book info using pythonbible
            try:
                expanded_ref = self._expand_abbrev(reference)
                nrefs = bible.get_references(expanded_ref)
                if nrefs:
                    first_ref = nrefs[0]
                    book_name = bible.Book(first_ref.book).title
                    chapter_num = first_ref.start_chapter
                else:
                    book_name = "Unknown"
                    chapter_num = None
            except:
                expanded_ref = reference
                book_name = "Unknown"
                chapter_num = None
            
            return {
                'success': True,
                'reference': expanded_ref if 'expanded_ref' in locals() else reference,
                'page': page_display,
                'page_start': page_start,
                'page_end': page_end,
                'is_range': is_range,
                'warning': warning,
                'book_info': {
                    'name': book_name,
                    'chapter': chapter_num,
                    'verses': None  # Could extract verse info if needed
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error processing reference: {str(e)}'
            }
    
    def _find_pages(self, ref_str: str) -> Tuple[Optional[List[int]], Optional[str]]:
        """
        Find pages for a given Bible reference.
        Returns (sorted_page_list, warning_msg).
        """
        ref = self._expand_abbrev(ref_str)
        try:
            nrefs = bible.get_references(ref)
            vids = bible.convert_references_to_verse_ids(nrefs)
        except Exception as e:
            return None, f"Invalid reference format: {e}"
        
        if not vids:
            return [], "No verses parsed from reference."
        
        pages = set()
        missing = 0
        for vid in vids:
            if vid in self.verse2pages:
                pages.update(self.verse2pages[vid])
            else:
                missing += 1
        
        if not pages:
            return [], f"All {missing} verse(s) out of range. Reference: '{ref}', Verse IDs: {vids[:5] if len(vids) > 5 else vids}"
        
        return sorted(pages), (None if missing == 0 else f"{missing} verse(s) out of range.")
