import re
from typing import Dict, List, Optional, Tuple

class BibleReferenceParser:
    """
    A class to parse Bible references and convert them to page numbers.
    Handles various reference formats and provides page number lookup.
    """
    
    def __init__(self):
        # Bible books mapping with abbreviations and full names
        self.books = {
            # Old Testament
            'genesis': {'name': 'Genesis', 'abbrev': ['gen', 'ge'], 'page_start': 1},
            'exodus': {'name': 'Exodus', 'abbrev': ['exod', 'ex'], 'page_start': 78},
            'leviticus': {'name': 'Leviticus', 'abbrev': ['lev', 'le'], 'page_start': 142},
            'numbers': {'name': 'Numbers', 'abbrev': ['num', 'nu'], 'page_start': 185},
            'deuteronomy': {'name': 'Deuteronomy', 'abbrev': ['deut', 'dt'], 'page_start': 239},
            'joshua': {'name': 'Joshua', 'abbrev': ['josh', 'jos'], 'page_start': 289},
            'judges': {'name': 'Judges', 'abbrev': ['judg', 'jdg'], 'page_start': 322},
            'ruth': {'name': 'Ruth', 'abbrev': ['ru'], 'page_start': 354},
            '1 samuel': {'name': '1 Samuel', 'abbrev': ['1sam', '1sa'], 'page_start': 359},
            '2 samuel': {'name': '2 Samuel', 'abbrev': ['2sam', '2sa'], 'page_start': 403},
            '1 kings': {'name': '1 Kings', 'abbrev': ['1king', '1ki'], 'page_start': 442},
            '2 kings': {'name': '2 Kings', 'abbrev': ['2king', '2ki'], 'page_start': 484},
            '1 chronicles': {'name': '1 Chronicles', 'abbrev': ['1chron', '1ch'], 'page_start': 525},
            '2 chronicles': {'name': '2 Chronicles', 'abbrev': ['2chron', '2ch'], 'page_start': 567},
            'ezra': {'name': 'Ezra', 'abbrev': ['ezr'], 'page_start': 610},
            'nehemiah': {'name': 'Nehemiah', 'abbrev': ['neh', 'ne'], 'page_start': 625},
            'esther': {'name': 'Esther', 'abbrev': ['esth', 'es'], 'page_start': 642},
            'job': {'name': 'Job', 'abbrev': ['jo'], 'page_start': 653},
            'psalms': {'name': 'Psalms', 'abbrev': ['psalm', 'ps'], 'page_start': 695},
            'proverbs': {'name': 'Proverbs', 'abbrev': ['prov', 'pr'], 'page_start': 789},
            'ecclesiastes': {'name': 'Ecclesiastes', 'abbrev': ['eccl', 'ec'], 'page_start': 825},
            'song of solomon': {'name': 'Song of Solomon', 'abbrev': ['song', 'ss'], 'page_start': 837},
            'isaiah': {'name': 'Isaiah', 'abbrev': ['isa', 'is'], 'page_start': 844},
            'jeremiah': {'name': 'Jeremiah', 'abbrev': ['jer', 'je'], 'page_start': 921},
            'lamentations': {'name': 'Lamentations', 'abbrev': ['lam', 'la'], 'page_start': 997},
            'ezekiel': {'name': 'Ezekiel', 'abbrev': ['ezek', 'eze'], 'page_start': 1007},
            'daniel': {'name': 'Daniel', 'abbrev': ['dan', 'da'], 'page_start': 1067},
            'hosea': {'name': 'Hosea', 'abbrev': ['hos', 'ho'], 'page_start': 1084},
            'joel': {'name': 'Joel', 'abbrev': ['joe'], 'page_start': 1094},
            'amos': {'name': 'Amos', 'abbrev': ['am'], 'page_start': 1099},
            'obadiah': {'name': 'Obadiah', 'abbrev': ['obad', 'ob'], 'page_start': 1108},
            'jonah': {'name': 'Jonah', 'abbrev': ['jon'], 'page_start': 1110},
            'micah': {'name': 'Micah', 'abbrev': ['mic'], 'page_start': 1114},
            'nahum': {'name': 'Nahum', 'abbrev': ['nah', 'na'], 'page_start': 1122},
            'habakkuk': {'name': 'Habakkuk', 'abbrev': ['hab'], 'page_start': 1126},
            'zephaniah': {'name': 'Zephaniah', 'abbrev': ['zeph', 'zep'], 'page_start': 1130},
            'haggai': {'name': 'Haggai', 'abbrev': ['hag'], 'page_start': 1134},
            'zechariah': {'name': 'Zechariah', 'abbrev': ['zech', 'zec'], 'page_start': 1137},
            'malachi': {'name': 'Malachi', 'abbrev': ['mal'], 'page_start': 1150},
            
            # New Testament
            'matthew': {'name': 'Matthew', 'abbrev': ['matt', 'mt'], 'page_start': 1155},
            'mark': {'name': 'Mark', 'abbrev': ['mk'], 'page_start': 1202},
            'luke': {'name': 'Luke', 'abbrev': ['lk'], 'page_start': 1234},
            'john': {'name': 'John', 'abbrev': ['jn'], 'page_start': 1287},
            'acts': {'name': 'Acts', 'abbrev': ['ac'], 'page_start': 1324},
            'romans': {'name': 'Romans', 'abbrev': ['rom', 'ro'], 'page_start': 1370},
            '1 corinthians': {'name': '1 Corinthians', 'abbrev': ['1cor', '1co'], 'page_start': 1394},
            '2 corinthians': {'name': '2 Corinthians', 'abbrev': ['2cor', '2co'], 'page_start': 1418},
            'galatians': {'name': 'Galatians', 'abbrev': ['gal', 'ga'], 'page_start': 1433},
            'ephesians': {'name': 'Ephesians', 'abbrev': ['eph', 'ep'], 'page_start': 1442},
            'philippians': {'name': 'Philippians', 'abbrev': ['phil', 'php'], 'page_start': 1451},
            'colossians': {'name': 'Colossians', 'abbrev': ['col'], 'page_start': 1458},
            '1 thessalonians': {'name': '1 Thessalonians', 'abbrev': ['1thess', '1th'], 'page_start': 1465},
            '2 thessalonians': {'name': '2 Thessalonians', 'abbrev': ['2thess', '2th'], 'page_start': 1471},
            '1 timothy': {'name': '1 Timothy', 'abbrev': ['1tim', '1ti'], 'page_start': 1475},
            '2 timothy': {'name': '2 Timothy', 'abbrev': ['2tim', '2ti'], 'page_start': 1482},
            'titus': {'name': 'Titus', 'abbrev': ['tit', 'ti'], 'page_start': 1488},
            'philemon': {'name': 'Philemon', 'abbrev': ['phlm', 'phm'], 'page_start': 1491},
            'hebrews': {'name': 'Hebrews', 'abbrev': ['heb'], 'page_start': 1493},
            'james': {'name': 'James', 'abbrev': ['jas'], 'page_start': 1512},
            '1 peter': {'name': '1 Peter', 'abbrev': ['1pet', '1pe'], 'page_start': 1520},
            '2 peter': {'name': '2 Peter', 'abbrev': ['2pet', '2pe'], 'page_start': 1528},
            '1 john': {'name': '1 John', 'abbrev': ['1jn'], 'page_start': 1533},
            '2 john': {'name': '2 John', 'abbrev': ['2jn'], 'page_start': 1540},
            '3 john': {'name': '3 John', 'abbrev': ['3jn'], 'page_start': 1542},
            'jude': {'name': 'Jude', 'abbrev': ['jud'], 'page_start': 1544},
            'revelation': {'name': 'Revelation', 'abbrev': ['rev', 're'], 'page_start': 1547}
        }
        
        # Create reverse lookup for abbreviations
        self.book_lookup = {}
        for book_key, book_info in self.books.items():
            # Add full name
            self.book_lookup[book_key.lower()] = book_key
            self.book_lookup[book_info['name'].lower()] = book_key
            # Add abbreviations
            for abbrev in book_info['abbrev']:
                self.book_lookup[abbrev.lower()] = book_key
    
    def parse_and_convert(self, reference: str) -> Dict:
        """
        Main method to parse a Bible reference and return page information.
        
        Args:
            reference (str): The Bible reference to parse
            
        Returns:
            Dict: Contains success status, page number(s), and reference details
        """
        try:
            parsed = self._parse_reference(reference)
            if not parsed:
                return {
                    'success': False,
                    'error': 'Could not parse the Bible reference. Please check the format.'
                }
            
            book_key, chapter, verses = parsed
            page_info = self._calculate_page_range(book_key, chapter, verses)
            
            return {
                'success': True,
                'reference': self._format_reference(book_key, chapter, verses),
                'page': page_info['page_display'],
                'page_start': page_info['page_start'],
                'page_end': page_info['page_end'],
                'is_range': page_info['is_range'],
                'book_info': {
                    'name': self.books[book_key]['name'],
                    'chapter': chapter,
                    'verses': verses
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error processing reference: {str(e)}'
            }
    
    def _parse_reference(self, reference: str) -> Optional[Tuple[str, int, Optional[str]]]:
        """
        Parse a Bible reference string into components.
        
        Returns:
            Tuple of (book_key, chapter, verses) or None if parsing fails
        """
        # Clean up the reference
        reference = reference.strip()
        
        # Pattern to match various reference formats including multi-chapter ranges
        # Examples: "John 3:16", "Genesis 1:1-10", "Psalm 23", "Genesis 1-3", "Matthew 5-7:10"
        patterns = [
            # Multi-chapter ranges: "Genesis 1-3", "Matthew 5-7"
            r'^([1-3]?\s*[a-zA-Z]+(?:\s+of\s+[a-zA-Z]+)?)\s+(\d+)-(\d+)$',
            # Chapter with verse range across chapters: "Matthew 5:1-7:10" 
            r'^([1-3]?\s*[a-zA-Z]+(?:\s+of\s+[a-zA-Z]+)?)\s+(\d+):(\d+)-(\d+):(\d+)$',
            # Single chapter with verse range: "John 3:16-20", "Genesis 1:1-10"
            r'^([1-3]?\s*[a-zA-Z]+(?:\s+of\s+[a-zA-Z]+)?)\s+(\d+):(\d+(?:-\d+)?)$',
            # Single chapter only: "Psalm 23", "Romans 8"
            r'^([1-3]?\s*[a-zA-Z]+(?:\s+of\s+[a-zA-Z]+)?)\s+(\d+)$'
        ]
        
        for i, pattern in enumerate(patterns):
            match = re.match(pattern, reference, re.IGNORECASE)
            if match:
                book_name = match.group(1).strip().lower()
                
                # Find the book key
                book_key = self.book_lookup.get(book_name)
                if not book_key:
                    return None
                
                if i == 0:  # Multi-chapter range
                    start_chapter = int(match.group(2))
                    end_chapter = int(match.group(3))
                    return book_key, start_chapter, f"chapters {start_chapter}-{end_chapter}"
                elif i == 1:  # Cross-chapter verse range
                    start_chapter = int(match.group(2))
                    start_verse = match.group(3)
                    end_chapter = int(match.group(4))
                    end_verse = match.group(5)
                    return book_key, start_chapter, f"{start_chapter}:{start_verse}-{end_chapter}:{end_verse}"
                elif i == 2:  # Single chapter with verse range
                    chapter = int(match.group(2))
                    verses = match.group(3)
                    return book_key, chapter, verses
                else:  # Single chapter only
                    chapter = int(match.group(2))
                    return book_key, chapter, None
        
        return None
    
    def _calculate_page_range(self, book_key: str, chapter: int, verses: Optional[str]) -> Dict:
        """
        Calculate the page range for a given reference.
        Returns both start and end pages for multi-page references.
        """
        base_page = self.books[book_key]['page_start']
        
        # Simple estimation: approximately 1-2 pages per chapter for most books
        # This would need to be replaced with actual page mapping data
        chapter_offset = max(0, (chapter - 1) * 1.5)
        
        # Default to single page
        start_page = int(base_page + chapter_offset)
        end_page = start_page
        is_range = False
        
        if verses:
            # Handle different verse formats
            if verses.startswith('chapters '):
                # Multi-chapter range: "chapters 1-3"
                chapter_range = verses.replace('chapters ', '')
                if '-' in chapter_range:
                    start_ch, end_ch = map(int, chapter_range.split('-'))
                    # Calculate start and end pages for chapter range
                    start_offset = max(0, (start_ch - 1) * 1.5)
                    end_offset = max(0, (end_ch - 1) * 1.5) + 1.5  # Add full chapter length
                    start_page = int(base_page + start_offset)
                    end_page = int(base_page + end_offset)
                    is_range = True
            elif ':' in verses and '-' in verses:
                # Check if it's a cross-chapter reference like "5:1-7:10"
                if verses.count(':') == 2:  # Cross-chapter verse range
                    parts = verses.split('-')
                    start_part = parts[0]
                    end_part = parts[1]
                    
                    start_ch, start_verse = map(int, start_part.split(':'))
                    end_ch, end_verse = map(int, end_part.split(':'))
                    
                    # Calculate start page
                    start_chapter_offset = max(0, (start_ch - 1) * 1.5)
                    start_verse_offset = (start_verse - 1) / 25
                    start_page = int(base_page + start_chapter_offset + start_verse_offset)
                    
                    # Calculate end page
                    end_chapter_offset = max(0, (end_ch - 1) * 1.5)
                    end_verse_offset = (end_verse - 1) / 25
                    end_page = int(base_page + end_chapter_offset + end_verse_offset)
                    
                    if start_page != end_page:
                        is_range = True
                else:
                    # Single chapter verse range like "16-20"
                    if '-' in verses:
                        start_verse, end_verse = map(int, verses.split('-'))
                        start_verse_offset = (start_verse - 1) / 25
                        end_verse_offset = (end_verse - 1) / 25
                        start_page = int(base_page + chapter_offset + start_verse_offset)
                        end_page = int(base_page + chapter_offset + end_verse_offset)
                        
                        if start_page != end_page:
                            is_range = True
                    else:
                        # Single verse
                        start_verse = int(verses)
                        verse_offset = (start_verse - 1) / 25
                        start_page = int(base_page + chapter_offset + verse_offset)
                        end_page = start_page
            elif '-' in verses:
                # Simple verse range within same chapter
                start_verse, end_verse = map(int, verses.split('-'))
                start_verse_offset = (start_verse - 1) / 25
                end_verse_offset = (end_verse - 1) / 25
                start_page = int(base_page + chapter_offset + start_verse_offset)
                end_page = int(base_page + chapter_offset + end_verse_offset)
                
                if start_page != end_page:
                    is_range = True
            else:
                # Single verse
                start_verse = int(verses)
                verse_offset = (start_verse - 1) / 25
                start_page = int(base_page + chapter_offset + verse_offset)
                end_page = start_page
        
        # Format page display
        if is_range:
            page_display = f"{start_page}-{end_page}"
        else:
            page_display = str(start_page)
        
        return {
            'page_start': start_page,
            'page_end': end_page,
            'page_display': page_display,
            'is_range': is_range
        }
    
    def _format_reference(self, book_key: str, chapter: int, verses: Optional[str]) -> str:
        """Format the reference for display."""
        book_name = self.books[book_key]['name']
        if verses:
            return f"{book_name} {chapter}:{verses}"
        else:
            return f"{book_name} {chapter}"
    
    def get_supported_books(self) -> List[str]:
        """Get a list of all supported book names."""
        return [book_info['name'] for book_info in self.books.values()]
