# 🎉 KID-FRIENDLY CHAT WITH PDF! 🎉
# This is like having a super smart friend who can read your books and answer questions!

import streamlit as st  # Makes our website look pretty
import os  # Helps us work with files
from PyPDF2 import PdfReader  # Reads PDF files (like digital books)
from langchain_openai import ChatOpenAI  # Our smart AI friend
from langchain.text_splitter import CharacterTextSplitter  # Cuts big text into small pieces
from langchain_huggingface import HuggingFaceEmbeddings  # Helps understand words
from langchain_community.vectorstores import FAISS  # Super-fast library
from langchain.chains import ConversationalRetrievalChain  # Helps have conversations
from langchain.memory import ConversationBufferMemory  # Remembers our chat

def main():
    """
    🎬 THE MAIN SHOW! Everything starts here!
    """
    
    # Make our website look nice and friendly
    st.set_page_config(
        page_title="🤖 My Smart Reading Buddy",
        page_icon="🤖",
        layout="wide"
    )
    
    # Show a big, friendly title
    st.title("🤖 My Smart Reading Buddy! 📚")
    st.markdown("**Upload your PDF and ask me anything! I'm like having a super smart friend who read your book!** ✨")
    
    # Add some fun emojis and colors
    st.markdown("---")
    st.markdown("🎯 **How it works:**")
    st.markdown("1. 📁 Upload your PDF file")
    st.markdown("2. 🔑 Add your secret key (ask a grown-up!)")
    st.markdown("3. 🚀 Click 'Start Reading!'")
    st.markdown("4. 💬 Ask me questions about your file!")
    st.markdown("---")
    
    # Create memory boxes for our robot
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "files_processed" not in st.session_state:
        st.session_state.files_processed = False

    # Create a friendly sidebar
    with st.sidebar:
        st.header("🛠️ My Toolbox")
        
        # File uploader with friendly messages
        uploaded_file = st.file_uploader(
            "📁 Drop your PDF file here!",
            type=['pdf'],
            help="Only PDF files work right now!"
        )
        
        # API key input with kid-friendly language
        openai_api_key = st.text_input(
            "🔑 Secret Key (Ask a grown-up for this!)",
            type="password",
            help="This is like a special password to talk to the smart robot!"
        )
        
        # Process button with fun emoji
        process_button = st.button("🚀 Start Reading!", type="primary")
    
    # When someone clicks the start button
    if process_button:
        if not openai_api_key:
            st.error("🚨 Oops! We need the secret key to make the magic work!")
            st.stop()
        
        if not uploaded_file:
            st.error("🚨 Don't forget to upload your PDF file first!")
            st.stop()
        
        # Show a fun loading message
        with st.spinner("🔄 Reading your file... This is like magic!"):
            try:
                # Step 1: Read the PDF
                st.write("📖 Reading your PDF file...")
                all_text = read_pdf_file(uploaded_file)
                
                # Step 2: Cut text into pieces
                st.write("✂️ Cutting your text into small pieces...")
                text_pieces = cut_text_into_pieces(all_text)
                
                # Step 3: Create smart library
                st.write("🏛️ Creating my smart library...")
                smart_library = create_smart_library(text_pieces)
                
                # Step 4: Set up our chat robot
                st.write("🤖 Setting up your reading buddy...")
                st.session_state.conversation = create_chat_robot(smart_library, openai_api_key)
                
                st.session_state.files_processed = True
                
                st.success("🎉 Yay! Your reading buddy is ready! Now you can ask me questions!")
                
            except Exception as error:
                st.error(f"😞 Something went wrong: {error}")
                st.error("Try uploading your file again or ask a grown-up for help!")

    # Show the chat interface if files are processed
    if st.session_state.files_processed:
        st.header("💬 Chat with Your Reading Buddy!")
        
        # Chat input with friendly message
        user_question = st.chat_input("Ask me anything about your file! 🤔")
        
        if user_question:
            handle_question(user_question)


def read_pdf_file(pdf_file):
    """
    📖 PDF READER
    This reads your PDF file like a super-fast reader!
    """
    pdf_reader = PdfReader(pdf_file)
    text = ""
    
    # Read each page
    for page_number, page in enumerate(pdf_reader.pages):
        st.write(f"  📄 Reading page {page_number + 1}")
        text += page.extract_text()
        text += "\n"
    
    return text


def cut_text_into_pieces(big_text):
    """
    ✂️ TEXT CUTTER
    Cuts big text into small, easy pieces!
    """
    text_cutter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    
    text_pieces = text_cutter.split_text(big_text)
    st.write(f"✂️ I cut your text into {len(text_pieces)} pieces!")
    return text_pieces


def create_smart_library(text_pieces):
    """
    🏛️ SMART LIBRARY
    Creates a super-fast library to find information!
    """
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    smart_library = FAISS.from_texts(text_pieces, embeddings)
    st.write("🏛️ Smart library created! Now I can find answers super fast!")
    return smart_library


def create_chat_robot(smart_library, api_key):
    """
    🤖 CHAT ROBOT
    Creates our friendly robot that can chat with us!
    """
    # Create our AI friend
    ai_friend = ChatOpenAI(
        api_key=api_key,
        model="gpt-4o-mini",
        temperature=0.1,
        max_tokens=1000
    )
    
    # Give the robot memory
    robot_memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True,
        output_key='answer'
    )
    
    # Connect everything together
    chat_robot = ConversationalRetrievalChain.from_llm(
        llm=ai_friend,
        retriever=smart_library.as_retriever(search_kwargs={"k": 3}),
        memory=robot_memory,
        return_source_documents=True
    )
    
    st.write("🤖 Your reading buddy is ready to chat!")
    return chat_robot


def handle_question(user_question):
    """
    💬 QUESTION HANDLER
    Takes care of answering your questions!
    """
    # Get answer from our robot
    response = st.session_state.conversation({
        'question': user_question
    })
    
    # Save our conversation
    st.session_state.chat_history.append(('user', user_question))
    st.session_state.chat_history.append(('bot', response['answer']))
    
    # Show our chat
    show_chat()


def show_chat():
    """
    💬 SHOW CHAT
    Shows our conversation in a nice way!
    """
    # Show each message
    for sender, message_text in st.session_state.chat_history:
        if sender == 'user':
            # Your messages (blue)
            st.markdown(f"""
            <div style="text-align: right; margin: 10px 0;">
                <div style="background-color: #007bff; color: white; padding: 10px; border-radius: 10px; display: inline-block; max-width: 70%;">
                    🧒 You: {message_text}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Robot messages (gray)
            st.markdown(f"""
            <div style="text-align: left; margin: 10px 0;">
                <div style="background-color: #f1f1f1; color: black; padding: 10px; border-radius: 10px; display: inline-block; max-width: 70%;">
                    🤖 Reading Buddy: {message_text}
                </div>
            </div>
            """, unsafe_allow_html=True)


# 🎬 START THE SHOW!
if __name__ == '__main__':
    main() 