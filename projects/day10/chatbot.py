
# First, let's import all the tools we need 
import streamlit as st  # This makes our web page look pretty
import os  # This helps us work with files on the computer
from PyPDF2 import PdfReader  # This reads PDF files (like digital books)
import docx  # This reads Word documents
from langchain_openai import ChatOpenAI  # This is our smart AI friend
from dotenv import load_dotenv  # This keeps our secret keys safe
from langchain.text_splitter import CharacterTextSplitter  # This cuts big text into small pieces
from langchain_huggingface import HuggingFaceEmbeddings  # This helps understand what words mean
from langchain_community.vectorstores import FAISS  # This is like a super-fast library for our text
from langchain.chains import ConversationalRetrievalChain  # This helps have conversations
from langchain.memory import ConversationBufferMemory  # This remembers what we talked about
from streamlit_chat import message  # This makes chat bubbles look nice
from langchain.callbacks import get_openai_callback  # This counts how much we use the AI


def main():
    """
    🎪 MAIN FUNCTION - This is like the ringmaster of our circus!
    Everything starts here and this function controls the whole show!
    """
    
    # Load our secret keys (like opening a treasure chest with passwords)
    load_dotenv()
    
    # Set up our web page to look nice
    st.set_page_config(
        page_title="🤖 Chat with PDF",  # The title at the top of the browser
        page_icon="🤖",  # A cute robot icon
        layout="wide"  # Make the page use all the screen space
    )
    
    # Make a big friendly title
    st.title("🤖 Chat with Your Files - Like Magic! ✨")
    st.markdown("Upload your files and ask me anything about them! I'm like a super smart reading buddy!")
    
    # These are like the robot's memory boxes - they remember things between questions
    if "conversation" not in st.session_state:
        st.session_state.conversation = None  # No conversation yet
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []  # Empty list to store our chats
    if "files_processed" not in st.session_state:
        st.session_state.files_processed = False  # Haven't processed files yet

    # Create a sidebar (like a toolbox on the side of the screen)
    with st.sidebar:
        st.header("🛠️ My Toolbox")
        
        # File uploader - like a mail slot for your files
        uploaded_files = st.file_uploader(
            "📁 Drop your files here! (PDF or Word docs)",
            type=['pdf', 'docx'],
            accept_multiple_files=True,
            help="You can upload multiple files at once!"
        )
        
        # API key input - this is like a special password to use the smart AI
        openai_api_key = st.text_input(
            "🔑 OpenAI API Key (Ask a grown-up for this!)",
            type="password",
            help="This is a secret key that lets us talk to the AI"
        )
        
        # Process button - like pressing "GO!" to start the magic
        process_button = st.button("🎯 Process My Files!", type="primary")
    
    # When someone clicks the process button
    if process_button:
        if not openai_api_key:
            st.error("🚨 Oops! We need the secret API key to make the magic work!")
            st.stop()  # Stop everything until we get the key
        
        if not uploaded_files:
            st.error("🚨 Don't forget to upload some files first!")
            st.stop()
        
        # Show a spinner while we work (like a loading animation)
        with st.spinner("🔄 Reading your files... This might take a moment!"):
            try:
                # Step 1: Read all the text from the files
                all_text = read_all_files(uploaded_files)
                
                # Step 2: Cut the big text into smaller pieces (like cutting a pizza)
                text_pieces = cut_text_into_pieces(all_text)
                
                # Step 3: Create a smart library to store our text pieces
                smart_library = create_smart_library(text_pieces)
                
                # Step 4: Set up our conversation robot
                st.session_state.conversation = create_conversation_robot(smart_library, openai_api_key)
                
                # Remember that we've processed the files
                st.session_state.files_processed = True
                
                st.success("🎉 Hooray! Your files are ready! Now you can ask me questions!")
                
            except Exception as error:
                st.error(f"😞 Something went wrong: {error}")
                st.error("Try uploading your files again or ask a grown-up for help!")

    # If files are processed, show the chat interface
    if st.session_state.files_processed:
        st.header("💬 Chat with Your Files")
        
        # Chat input box
        user_question = st.chat_input("Ask me anything about your files! 🤔")
        
        if user_question:
            handle_user_question(user_question)


def read_all_files(uploaded_files):
    """
    📚 FILE READER FUNCTION
    This function is like a super reader who can read different types of files!
    It takes a list of files and reads all the text from them.
    """
    all_text = ""  # Start with an empty string (like an empty notebook)
    
    # Look at each file one by one
    for file in uploaded_files:
        st.write(f"📖 Reading: {file.name}")
        
        # Figure out what type of file it is by looking at its name
        file_name, file_extension = os.path.splitext(file.name)
        
        # Choose the right reading method based on file type
        if file_extension.lower() == ".pdf":
            all_text += read_pdf_file(file)
        elif file_extension.lower() == ".docx":
            all_text += read_word_file(file)
        else:
            st.warning(f"🤷 I don't know how to read {file_extension} files yet!")
    
    return all_text


def read_pdf_file(pdf_file):
    """
    📄 PDF READER FUNCTION
    This function reads PDF files page by page, like flipping through a book!
    """
    pdf_reader = PdfReader(pdf_file)  # Create a PDF reader tool
    text = ""  # Empty string to store all the text
    
    # Read each page one by one
    for page_number, page in enumerate(pdf_reader.pages):
        st.write(f"  📄 Reading page {page_number + 1}")
        text += page.extract_text()  # Get all the text from this page
        text += "\n"  # Add a new line between pages
    
    return text


def read_word_file(word_file):
    """
    📝 WORD DOCUMENT READER FUNCTION
    This function reads Word documents paragraph by paragraph!
    """
    document = docx.Document(word_file)  # Open the Word document
    all_paragraphs = []  # Empty list to store paragraphs
    
    # Read each paragraph
    for paragraph in document.paragraphs:
        if paragraph.text.strip():  # Only add paragraphs that have text
            all_paragraphs.append(paragraph.text)
    
    # Join all paragraphs with spaces
    text = ' '.join(all_paragraphs)
    return text


def cut_text_into_pieces(big_text):
    """
    ✂️ TEXT CUTTER FUNCTION
    This function takes really long text and cuts it into smaller, easier pieces!
    It's like cutting a really long sandwich into bite-sized pieces.
    """
    # Create our text cutter tool
    text_cutter = CharacterTextSplitter(
        separator="\n",  # Cut at new lines (like paragraph breaks)
        chunk_size=1000,  # Each piece should be about 1000 characters (updated from 900)
        chunk_overlap=200,  # Let pieces overlap by 200 characters so we don't lose meaning (updated from 100)
        length_function=len  # Use the built-in length function to count characters
    )
    
    # Cut the text into pieces
    text_pieces = text_cutter.split_text(big_text)
    
    st.write(f"✂️ I cut your text into {len(text_pieces)} pieces!")
    return text_pieces


def create_smart_library(text_pieces):
    """
    🏛️ SMART LIBRARY CREATOR FUNCTION
    This function creates a magical library that can find information super fast!
    It's like having a librarian who knows exactly where everything is.
    """
    # Create embeddings (these help the computer understand what words mean)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"  # A good, fast model
    )
    
    # Create our smart library using FAISS (it's like a super-fast card catalog)
    smart_library = FAISS.from_texts(text_pieces, embeddings)
    
    st.write("🏛️ Smart library created! Now I can find answers super fast!")
    return smart_library


def create_conversation_robot(smart_library, api_key):
    """
    🤖 CONVERSATION ROBOT CREATOR FUNCTION
    This function creates our smart robot friend who can have conversations with us!
    """
    # Create our AI friend (updated to use gpt-4o-mini which is newer and better)
    ai_friend = ChatOpenAI(
        api_key=api_key,
        model="gpt-4.1-nano",  # Updated from gpt-3.5-turbo to newer model
        temperature=0.1,  # Keep answers focused and consistent
        max_tokens=1000  # Limit response length
    )
    
    # Create memory so the robot remembers our conversation
    robot_memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True,
        output_key='answer'  # Added for better memory handling
    )
    
    # Create the conversation chain (this connects everything together)
    conversation_robot = ConversationalRetrievalChain.from_llm(
        llm=ai_friend,
        retriever=smart_library.as_retriever(search_kwargs={"k": 3}),  # Get 3 relevant pieces
        memory=robot_memory,
        return_source_documents=True  # Show where answers come from
    )
    
    st.write("🤖 Your conversation robot is ready to chat!")
    return conversation_robot


def handle_user_question(user_question):
    """
    💬 QUESTION HANDLER FUNCTION
    This function takes care of answering user questions!
    It's like the robot's ears and mouth working together.
    """
    # Use the OpenAI callback to track usage
    with get_openai_callback() as usage_tracker:
        # Get response from our conversation robot
        response = st.session_state.conversation({
            'question': user_question
        })
    
    # Add the new conversation to our history
    st.session_state.chat_history.append(('user', user_question))
    st.session_state.chat_history.append(('bot', response['answer']))
    
    # Display the conversation
    display_chat_history()
    
    # Show usage information (how much we used the AI)
    with st.expander("📊 Usage Information"):
        st.write(f"🔢 Total tokens used: {usage_tracker.total_tokens}")
        st.write(f"💰 Cost: ${usage_tracker.total_cost:.4f}")
        
        # Show source documents if available
        if 'source_documents' in response:
            st.write("📚 I found this information in your files:")
            for i, doc in enumerate(response['source_documents'][:2]):  # Show first 2 sources
                st.write(f"Source {i+1}: {doc.page_content[:200]}...")


def display_chat_history():
    """
    💬 CHAT DISPLAY FUNCTION
    This function shows all our conversation in a nice, easy-to-read way!
    """
    # Create a container for our chat
    chat_container = st.container()
    
    with chat_container:
        # Show each message in our chat history
        for i, (sender, message_text) in enumerate(st.session_state.chat_history):
            if sender == 'user':
                # Show user messages on the right with a different color
                st.markdown(f"""
                <div style="text-align: right; margin: 10px 0;">
                    <div style="background-color: #007bff; color: white; padding: 10px; border-radius: 10px; display: inline-block; max-width: 70%;">
                        🧒 You: {message_text}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Show bot messages on the left with a different color
                st.markdown(f"""
                <div style="text-align: left; margin: 10px 0;">
                    <div style="background-color: #f1f1f1; color: black; padding: 10px; border-radius: 10px; display: inline-block; max-width: 70%;">
                        🤖 Bot: {message_text}
                    </div>
                </div>
                """, unsafe_allow_html=True)


# 🎬 THE MAIN SHOW STARTS HERE!
# This is like the "Once upon a time..." of our program
if __name__ == '__main__':
    main()  # Start the main function and let the magic begin!