import streamlit as st
import requests

st.title('PDF Knowledge Base Chatbot')

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    response = requests.post('http://localhost:5000/upload', files={'file': uploaded_file})
    if response.status_code == 200:
        context = response.json()['text']
        st.session_state['context'] = context
        st.success("PDF uploaded successfully!")

    question = st.text_input("Ask a question about the PDF:")
    if st.button("Submit"):
        if 'context' in st.session_state:
            answer_response = requests.post('http://localhost:5000/ask', json={
                'question': question,
                'context': st.session_state['context']
            })
            if answer_response.status_code == 200:
                answer = answer_response.json().get('answer', 'No answer found.')
                st.write(f"Answer: {answer}")
            else:
                st.error("Error getting answer.")
        else:
            st.error("No PDF uploaded yet.")
