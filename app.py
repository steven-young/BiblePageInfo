import streamlit as st
from bible_reference_parser import BibleReferenceParser

def main():
    st.title("Bible Reference to Page Number Converter")
    st.write("Enter a Bible reference to find the corresponding page number.")
    
    # Initialize the parser
    parser = BibleReferenceParser()
    
    # Use a form to enable Enter key functionality
    with st.form(key="reference_form", clear_on_submit=False):
        # Create input field
        reference_input = st.text_input(
            "Bible Reference",
            placeholder="e.g., John 3:16, Genesis 1-3, Matthew 5:1-7:10",
            help="Enter Bible references in standard format. Press Enter or click the button to search.",
            key="reference_input"
        )
        
        # Create submit button
        search_clicked = st.form_submit_button("Find Page Number", type="primary")
    
    # Process the reference when form is submitted (button clicked OR Enter pressed)
    if search_clicked:
        if reference_input.strip():
            try:
                # Process the reference
                result = parser.parse_and_convert(reference_input.strip())
                
                if result['success']:
                    # Display page information with appropriate formatting for ranges
                    if result.get('is_range', False):
                        st.success(f"📖 **{result['reference']}** can be found on pages **{result['page']}**")
                    else:
                        st.success(f"📖 **{result['reference']}** can be found on page **{result['page']}**")
                    
                    # Display additional information if available
                    if result.get('book_info'):
                        with st.expander("Reference Details"):
                            st.write(f"**Book:** {result['book_info']['name']}")
                            st.write(f"**Chapter:** {result['book_info']['chapter']}")
                            if result['book_info'].get('verses'):
                                st.write(f"**Verses:** {result['book_info']['verses']}")
                            if result.get('is_range', False):
                                st.write(f"**Page Range:** {result['page_start']} - {result['page_end']}")
                            else:
                                st.write(f"**Page:** {result['page']}")
                else:
                    st.error(f"❌ {result['error']}")
                    
            except Exception as e:
                st.error(f"❌ An error occurred while processing the reference: {str(e)}")
        else:
            st.warning("⚠️ Please enter a Bible reference.")
    
    # Add some helpful information
    with st.expander("Supported Reference Formats"):
        st.write("""
        **Supported formats:**
        - Single verse: `John 3:16`, `Genesis 1:1`
        - Verse range: `Matthew 5:3-12`, `Genesis 1:1-10`
        - Whole chapter: `Psalm 23`, `Romans 8`
        - Multiple chapters: `Genesis 1-3`, `Matthew 5-7`
        - Cross-chapter verses: `Matthew 5:1-7:10`
        
        **Supported books:** All 66 books of the Bible (Old and New Testament)
        
        **Note:** This converter uses page numbers from a standard Bible edition. 
        Page numbers may vary between different Bible translations and publishers.
        """)

if __name__ == "__main__":
    main()
