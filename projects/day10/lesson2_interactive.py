# 🎨 LESSON 2: Making Things Interactive!
# Today we learn how to add buttons and make our website respond to clicks!

import streamlit as st

# 🎯 What we're learning today:
# - How to add buttons and inputs
# - How to organize information in sidebars
# - How to make things respond to user actions

# 📝 Step 1: Let's make our website look better
st.title("🤖 My Smart Reading Buddy!")
st.write("This is going to be our reading robot!")

# 🛠️ Step 2: Let's add a sidebar (like a toolbox)
with st.sidebar:
    st.header("🛠️ My Toolbox")
    st.write("This is where we'll put our tools!")

# 🎮 Step 3: Let's add some buttons!
st.header("🎮 Let's Play with Buttons!")

# This button shows a message when you click it
if st.button("🚀 Click Me!"):
    st.write("🎉 You clicked the button! Great job!")

# This button counts how many times you click it
if "click_count" not in st.session_state:
    st.session_state.click_count = 0

if st.button("🔢 Count My Clicks!"):
    st.session_state.click_count += 1
    st.write(f"You clicked {st.session_state.click_count} times!")

# 📁 Step 4: Let's add a file uploader
st.header("📁 File Uploader")
uploaded_file = st.file_uploader("📁 Drop your file here!", type=['txt', 'pdf'])

if uploaded_file:
    st.write(f"📄 You uploaded: {uploaded_file.name}")
    st.write("📏 File size:", uploaded_file.size, "bytes")

# 🔑 Step 5: Let's add a text input
st.header("🔑 Secret Input")
secret_text = st.text_input("🔑 Type your secret message here:", type="password")

if secret_text:
    st.write("🤫 Your secret message is:", secret_text)

# 🎯 Challenge for you:
# 1. Add a new button that shows your favorite color
# 2. Change the sidebar header to something fun
# 3. Add a text input for your name and display it

# 💡 What you learned:
# - st.button() creates clickable buttons
# - st.sidebar creates a sidebar
# - st.file_uploader() lets people upload files
# - st.text_input() creates text input boxes
# - st.session_state remembers things between clicks

# 🚀 Next time: We'll learn how to read PDF files!

# 🎮 Try this:
# 1. Click the buttons and see what happens
# 2. Upload a file and see the information
# 3. Type in the secret input and see your message 