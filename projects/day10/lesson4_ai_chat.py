# 🧠 LESSON 4: Talking to AI!
# Today we learn how to make our computer understand questions and give smart answers!

import streamlit as st
from PyPDF2 import PdfReader
from langchain_openai import ChatOpenAI

# 🎯 What we're learning today:
# - What AI is and how it works
# - How to ask questions and get answers
# - How to connect AI to our PDF reader

# 📝 Step 1: Let's create our AI friend
def create_ai_friend(api_key):
    """
    🤖 This creates our smart AI friend!
    """
    ai_friend = ChatOpenAI(
        api_key=api_key,
        model="gpt-4o-mini",
        temperature=0.1  # Makes answers more focused
    )
    return ai_friend

# 💬 Step 2: Let's create a function to ask AI questions
def ask_ai_question(ai_friend, question, context):
    """
    💬 This asks our AI friend a question about the text!
    """
    # Create a prompt that tells AI what to do
    prompt = f"""
    Based on this text: {context}
    
    Question: {question}
    
    Please answer the question based only on the information in the text above.
    """
    
    # Ask the AI and get the answer (using newer syntax)
    response = ai_friend.invoke(prompt)
    return response.content

# 📖 Step 3: Let's create our PDF reader (same as before)
def read_pdf_file(pdf_file):
    """
    📖 This function reads PDF files like a super-fast reader!
    """
    pdf_reader = PdfReader(pdf_file)
    text = ""
    
    for page_number, page in enumerate(pdf_reader.pages):
        st.write(f"📄 Reading page {page_number + 1}")
        text += page.extract_text()
        text += "\n"
    
    return text

# 🎬 Step 4: Let's make our website
st.title("🧠 AI Reading Buddy!")
st.write("I can read your PDF and answer questions about it!")

# 📁 Step 5: Add file uploader and API key input
with st.sidebar:
    st.header("🛠️ Setup")
    uploaded_file = st.file_uploader("📁 Drop your PDF here!", type=['pdf'])
    api_key = st.text_input("🔑 OpenAI API Key (ask a grown-up!)", type="password")

# 🔍 Step 6: Process the file and create AI friend
if uploaded_file and api_key:
    st.write(f"📄 You uploaded: {uploaded_file.name}")
    
    with st.spinner("🔄 Reading your file and setting up AI..."):
        try:
            # Read the PDF
            all_text = read_pdf_file(uploaded_file)
            
            # Create our AI friend
            ai_friend = create_ai_friend(api_key)
            
            st.success("✅ Ready to answer questions!")
            
            # Show the text we read
            with st.expander("📖 Click to see what I read"):
                st.text_area("File Content:", all_text[:1000] + "...", height=200)
            
            # 💬 Step 7: Let's chat with AI!
            st.header("💬 Ask me anything about your file!")
            
            # Add a chat input
            user_question = st.text_input("🤔 Your question:")
            
            if user_question:
                with st.spinner("🤖 Thinking..."):
                    try:
                        # Ask AI the question
                        answer = ask_ai_question(ai_friend, user_question, all_text)
                        
                        # Show the answer in a nice way
                        st.markdown("### 🤖 AI Answer:")
                        st.write(answer)
                        
                        # Show some example questions
                        st.markdown("### 💡 Try asking:")
                        st.write("- What is this document about?")
                        st.write("- Who are the main characters?")
                        st.write("- What are the important points?")
                        st.write("- Can you summarize this?")
                        
                    except Exception as error:
                        st.error(f"😞 AI had trouble answering: {error}")
            
        except Exception as error:
            st.error(f"😞 Something went wrong: {error}")

# 🎯 Challenge for you:
# 1. Ask different types of questions
# 2. See how the AI responds to specific vs. general questions
# 3. Try uploading different types of PDFs

# 💡 What you learned:
# - AI can understand and answer questions about text
# - We need to give AI context (the PDF text) to answer questions
# - Different questions get different types of answers
# - AI is like a very smart friend who read your book

# 🚀 Next time: We'll put everything together into one complete chatbot!

# 🎮 Try this:
# 1. Upload a story and ask "What is this about?"
# 2. Upload a science article and ask "What are the main points?"
# 3. Ask specific questions like "What happens in chapter 2?"
# 4. Compare how AI answers different types of questions

# 💭 Think about:
# - What makes a good question for AI?
# - How is AI different from human thinking?
# - What are the limitations of AI? 