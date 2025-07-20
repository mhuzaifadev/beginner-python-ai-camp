# 📖 LESSON 3: Reading Files!
# Today we learn how to make our computer read PDF files like a super-fast reader!

import streamlit as st
from PyPDF2 import PdfReader

# 🎯 What we're learning today:
# - How to read PDF files
# - How to extract text from documents
# - How to process information step by step

# 📝 Step 1: Let's create our file reading function
def read_pdf_file(pdf_file):
    """
    📖 This function reads PDF files like a super-fast reader!
    """
    pdf_reader = PdfReader(pdf_file)
    text = ""
    
    # Read each page one by one
    for page_number, page in enumerate(pdf_reader.pages):
        st.write(f"📄 Reading page {page_number + 1}")
        text += page.extract_text()
        text += "\n"  # Add a new line between pages
    
    return text

# 🎬 Step 2: Let's make our website
st.title("📖 PDF Reader Robot!")
st.write("I can read your PDF files and show you what's inside!")

# 📁 Step 3: Add file uploader
uploaded_file = st.file_uploader("📁 Drop your PDF file here!", type=['pdf'])

# 🔍 Step 4: Read the file when uploaded
if uploaded_file:
    st.write(f"📄 You uploaded: {uploaded_file.name}")
    
    # Show a spinner while reading (like a loading animation)
    with st.spinner("🔄 Reading your file... This might take a moment!"):
        try:
            # Read the PDF
            all_text = read_pdf_file(uploaded_file)
            
            # Show what we read
            st.success("✅ File read successfully!")
            
            # Show the first part of the text
            st.header("📚 Here's what I read:")
            st.write("(Showing first 500 characters...)")
            st.text_area("📖 File Content:", all_text[:500] + "...", height=200)
            
            # Show some statistics
            st.header("📊 File Statistics:")
            st.write(f"📄 Total pages: {len(PdfReader(uploaded_file).pages)}")
            st.write(f"📝 Total characters: {len(all_text)}")
            st.write(f"📊 File size: {uploaded_file.size} bytes")
            
        except Exception as error:
            st.error(f"😞 Something went wrong: {error}")
            st.write("Try uploading a different PDF file!")

# 🎯 Challenge for you:
# 1. Try uploading different PDF files
# 2. See how the statistics change
# 3. Notice how some files work better than others

# 💡 What you learned:
# - PyPDF2 can read PDF files
# - We can extract text from each page
# - Different files have different amounts of text
# - Error handling helps when things go wrong

# 🚀 Next time: We'll learn how to talk to AI!

# 🎮 Try this:
# 1. Upload a simple PDF (like a short story)
# 2. Upload a complex PDF (like a textbook)
# 3. Compare how much text each one has
# 4. Notice how the reading process works

# 💭 Think about:
# - What kinds of files work best?
# - What happens with files that have lots of pictures?
# - How could we make this work with other file types? 