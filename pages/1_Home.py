import streamlit as st

st.title(" Welcome to your bot!")
st.markdown(
    '''
Welcome to your chatbot built with LLM models! You can chat with me and ask me anything. 
Besides, you can also upload documents!
'''
)


# Select a LLM model(optional)
model_choice = st.selectbox(
    "Choose a model you would like to use",
    # need to update this list with the actual models available
    ["GPT-3.5", "GPT-4", "Claude 3"],
    index=0,
    help="The default model is GPT-3.5. You can choose any model from the dropdown list."
)

# Upload multiple files(optional)
''' uploaded_files = st.file_uploader(
    accept_multiple_files=True,
    type=["jpg", "jpeg", "pdf", "txt", "docx", "csv"],
    help="You can upload multiple files. The files will be used to answer your questions. "
         "The files will be stored in the session state and will be used for the chat."
    "Choose your files to be uploaded"
)

for file in uploaded_files:
    bytes_data = file.read()
    st.write(
        "File name: ", file.name, "File type: ", file.type, "File length: ", len(bytes_data))
    st.write(bytes_data)  '''


# redirect to the chat page
if st.button("Start chatting!"):
    st.session_state.modelchoice = model_choice
    st.switch_page("2_Chat.py")
