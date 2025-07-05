# Bible Reference to Page Number Converter

## Overview

This is a Streamlit web application that converts Bible references (e.g., "John 3:16", "Genesis 1:1-10") into specific page numbers. The application provides a simple user interface where users can input Bible references in various formats and receive the corresponding page number from what appears to be a specific Bible edition or translation.

## System Architecture

The application follows a simple two-layer architecture:

1. **Frontend Layer**: Streamlit web interface (`app.py`)
2. **Processing Layer**: Bible reference parsing and conversion logic (`bible_reference_parser.py`)

### Design Rationale
- **Streamlit Choice**: Selected for rapid prototyping and deployment of data applications with minimal frontend development
- **Modular Design**: Separation of UI logic from business logic allows for easier testing and potential reuse of the parser in other contexts
- **Single-Page Application**: Simple, focused functionality doesn't require complex navigation or state management

## Key Components

### Frontend (app.py)
- **Streamlit Interface**: Provides text input, button interaction, and result display
- **User Input Validation**: Handles empty inputs and provides helpful error messages
- **Results Display**: Shows success/error states with formatted output
- **Help Documentation**: Expandable section showing supported reference formats

### Backend (bible_reference_parser.py)
- **BibleReferenceParser Class**: Core parsing and conversion logic
- **Book Mapping**: Comprehensive dictionary of Bible books with:
  - Full names and abbreviations
  - Starting page numbers for each book
  - Support for both Old and New Testament books (though New Testament data appears incomplete in the provided code)

## Data Flow

1. User enters Bible reference in text input field
2. Streamlit captures input on button click
3. Reference passed to `BibleReferenceParser.parse_and_convert()`
4. Parser processes reference using regex patterns and book mappings
5. Page number calculated based on book starting page and chapter/verse information
6. Result returned to Streamlit for display

## External Dependencies

- **Streamlit**: Web application framework for the user interface
- **Python Standard Library**: 
  - `re` module for regex pattern matching
  - `typing` module for type hints

### Dependency Rationale
- Minimal external dependencies reduce deployment complexity
- Streamlit provides sufficient functionality for the application's requirements
- Standard library usage ensures compatibility across Python environments

## Deployment Strategy

The application is designed for deployment on Replit or similar platforms:

- **Single-file execution**: Main application runs via `streamlit run app.py`
- **No database requirements**: All data stored in-memory as Python dictionaries
- **Platform agnostic**: Can run on any platform supporting Python and Streamlit

### Deployment Considerations
- Page number mappings are hardcoded, suggesting they're specific to a particular Bible edition
- No external configuration files required
- Stateless design enables easy horizontal scaling if needed

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes

- July 05, 2025: Enhanced Bible reference parser to support multi-chapter references (Genesis 1-3, Matthew 5:1-7:10)
- July 05, 2025: Added Enter key functionality using Streamlit forms for automatic submission
- July 05, 2025: Implemented page range calculation and display for references spanning multiple pages
- July 05, 2025: Updated UI to show "page" vs "pages" appropriately based on single page or page range

## Changelog

Changelog:
- July 05, 2025. Initial setup