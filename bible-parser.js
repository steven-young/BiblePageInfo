class BibleReferenceParser {
    constructor() {
        this.verse2pages = new Map();
        this.loadPageMap();
    }

    loadPageMap() {
        // Convert CSV data to verse ID mappings
        for (const entry of BIBLE_PAGE_DATA) {
            const { page, ref, spill } = entry;
            
            try {
                const verseIds = this.parseReferenceToVerseIds(ref);
                
                // Map every verse ID to this page
                for (const vid of verseIds) {
                    if (!this.verse2pages.has(vid)) {
                        this.verse2pages.set(vid, new Set());
                    }
                    this.verse2pages.get(vid).add(page);
                }
                
                // If spillover, also map the last verse to page+1
                if (spill && verseIds.length > 0) {
                    const lastVid = verseIds[verseIds.length - 1];
                    const nextPage = page + 1;
                    if (!this.verse2pages.has(lastVid)) {
                        this.verse2pages.set(lastVid, new Set());
                    }
                    this.verse2pages.get(lastVid).add(nextPage);
                }
            } catch (error) {
                console.warn(`Skipping invalid reference ${ref}: ${error.message}`);
            }
        }
    }

    expandAbbreviation(refStr) {
        // Handle Song of Solomon -> Song of Songs conversion
        if (refStr.startsWith("Song of Solomon")) {
            return refStr.replace("Song of Solomon", "Song of Songs");
        }
        
        // Handle abbreviations
        const parts = refStr.trim().split(' ');
        const book = parts[0];
        const rest = parts.slice(1).join(' ');
        const fullName = BOOK_ABBREVIATIONS[book];
        
        return fullName ? `${fullName} ${rest}`.trim() : refStr;
    }

    parseReferenceToVerseIds(reference) {
        // This is a simplified parser that converts Bible references to verse IDs
        // In a real implementation, you'd use a more sophisticated parsing library
        
        const expanded = this.expandAbbreviation(reference);
        const verseIds = [];
        
        // Parse the reference format: "Book Chapter:Verse-Verse" or "Book Chapter-Chapter"
        const match = expanded.match(/^(.+?)\s+(\d+)(?::(\d+))?(?:-(\d+)(?::(\d+))?)?$/);
        
        if (!match) {
            throw new Error(`Invalid reference format: ${reference}`);
        }
        
        const [, bookName, startChapter, startVerse, endChapterOrVerse, endVerse] = match;
        const bookId = this.getBookId(bookName);
        
        if (!bookId) {
            throw new Error(`Unknown book: ${bookName}`);
        }
        
        const startCh = parseInt(startChapter);
        const startV = startVerse ? parseInt(startVerse) : 1;
        
        let endCh, endV;
        
        if (endVerse) {
            // Cross-chapter range like "Matthew 5:1-7:10"
            endCh = parseInt(endChapterOrVerse);
            endV = parseInt(endVerse);
        } else if (endChapterOrVerse) {
            if (startVerse) {
                // Verse range within chapter like "John 3:16-18"
                endCh = startCh;
                endV = parseInt(endChapterOrVerse);
            } else {
                // Chapter range like "Genesis 1-3"
                endCh = parseInt(endChapterOrVerse);
                endV = this.getMaxVerseInChapter(bookId, endCh);
            }
        } else {
            // Single chapter or verse
            endCh = startCh;
            endV = startVerse ? startV : this.getMaxVerseInChapter(bookId, startCh);
        }
        
        // Generate verse IDs for the range
        for (let ch = startCh; ch <= endCh; ch++) {
            const chStartV = (ch === startCh) ? startV : 1;
            const chEndV = (ch === endCh) ? endV : this.getMaxVerseInChapter(bookId, ch);
            
            for (let v = chStartV; v <= chEndV; v++) {
                verseIds.push(this.createVerseId(bookId, ch, v));
            }
        }
        
        return verseIds;
    }

    getBookId(bookName) {
        // Map book names to IDs (simplified)
        const books = {
            'Genesis': 1, 'Exodus': 2, 'Leviticus': 3, 'Numbers': 4, 'Deuteronomy': 5,
            'Joshua': 6, 'Judges': 7, 'Ruth': 8, '1 Samuel': 9, '2 Samuel': 10,
            '1 Kings': 11, '2 Kings': 12, '1 Chronicles': 13, '2 Chronicles': 14,
            'Ezra': 15, 'Nehemiah': 16, 'Esther': 17, 'Job': 18, 'Psalms': 19,
            'Proverbs': 20, 'Ecclesiastes': 21, 'Song of Songs': 22, 'Isaiah': 23,
            'Jeremiah': 24, 'Lamentations': 25, 'Ezekiel': 26, 'Daniel': 27,
            'Hosea': 28, 'Joel': 29, 'Amos': 30, 'Obadiah': 31, 'Jonah': 32,
            'Micah': 33, 'Nahum': 34, 'Habakkuk': 35, 'Zephaniah': 36,
            'Haggai': 37, 'Zechariah': 38, 'Malachi': 39, 'Matthew': 40,
            'Mark': 41, 'Luke': 42, 'John': 43, 'Acts': 44, 'Romans': 45,
            '1 Corinthians': 46, '2 Corinthians': 47, 'Galatians': 48,
            'Ephesians': 49, 'Philippians': 50, 'Colossians': 51,
            '1 Thessalonians': 52, '2 Thessalonians': 53, '1 Timothy': 54,
            '2 Timothy': 55, 'Titus': 56, 'Philemon': 57, 'Hebrews': 58,
            'James': 59, '1 Peter': 60, '2 Peter': 61, '1 John': 62,
            '2 John': 63, '3 John': 64, 'Jude': 65, 'Revelation': 66
        };
        return books[bookName];
    }

    getMaxVerseInChapter(bookId, chapter) {
        // Simplified - in reality you'd need a complete verse count database
        // For now, return a reasonable default
        return 50;
    }

    createVerseId(bookId, chapter, verse) {
        // Create a unique verse ID (simplified format)
        return (bookId * 1000000) + (chapter * 1000) + verse;
    }

    findPages(reference) {
        const expanded = this.expandAbbreviation(reference);
        
        try {
            const verseIds = this.parseReferenceToVerseIds(expanded);
            
            if (verseIds.length === 0) {
                return { pages: [], warning: "No verses parsed from reference." };
            }
            
            const pages = new Set();
            let missing = 0;
            
            for (const vid of verseIds) {
                if (this.verse2pages.has(vid)) {
                    const vidPages = this.verse2pages.get(vid);
                    for (const page of vidPages) {
                        pages.add(page);
                    }
                } else {
                    missing++;
                }
            }
            
            if (pages.size === 0) {
                return { 
                    pages: [], 
                    warning: `All ${missing} verse(s) out of range.` 
                };
            }
            
            const sortedPages = Array.from(pages).sort((a, b) => a - b);
            const warning = missing === 0 ? null : `${missing} verse(s) out of range.`;
            
            return { pages: sortedPages, warning };
            
        } catch (error) {
            return { pages: null, warning: `Invalid reference format: ${error.message}` };
        }
    }

    parseAndConvert(reference) {
        try {
            const { pages, warning } = this.findPages(reference);
            
            if (pages === null) {
                return {
                    success: false,
                    error: warning
                };
            }
            
            if (pages.length === 0) {
                return {
                    success: false,
                    error: warning || "Reference not found in page map."
                };
            }
            
            // Format page information
            const isRange = pages.length > 1;
            const pageStart = pages[0];
            const pageEnd = pages[pages.length - 1];
            
            // Format the output range
            let pageDisplay;
            if (pages.length === 1) {
                pageDisplay = pages[0].toString();
            } else {
                const start = pages[0];
                const end = pages[pages.length - 1];
                if (end === start + pages.length - 1) {
                    pageDisplay = `${start}-${end}`;
                } else {
                    pageDisplay = pages.join(',');
                }
            }
            
            // Get book info
            const expanded = this.expandAbbreviation(reference);
            const bookMatch = expanded.match(/^(.+?)\s+(\d+)/);
            const bookName = bookMatch ? bookMatch[1] : "Unknown";
            const chapterNum = bookMatch ? parseInt(bookMatch[2]) : null;
            
            return {
                success: true,
                reference: expanded,
                page: pageDisplay,
                pageStart: pageStart,
                pageEnd: pageEnd,
                isRange: isRange,
                warning: warning,
                bookInfo: {
                    name: bookName,
                    chapter: chapterNum,
                    verses: null
                }
            };
            
        } catch (error) {
            return {
                success: false,
                error: `Error processing reference: ${error.message}`
            };
        }
    }
}