import streamlit as st

st.markdown(
    '<div class="flex flex-col items-center justify-center min-h-screen">'
    '<div class="w-full max-w-md p-4 bg-white rounded shadow">'
    '<h2 class="text-xl mb-4">Chat Bot</h2>',
    unsafe_allow_html=True
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.write(msg)

user_input = st.text_input("Ask le Chat")
if st.button("Send"):
    st.session_state.messages.append(f"You: {user_input}")
    st.session_state.messages.append(f"Bot: You said {user_input}")

uploaded_file = st.file_uploader("Upload a file")
if uploaded_file:
    st.write(f"Uploaded: {uploaded_file.name}")

st.markdown('</div></div>', unsafe_allow_html=True) 