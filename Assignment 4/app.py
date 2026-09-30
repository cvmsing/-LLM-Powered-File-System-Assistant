import streamlit as st

from llm_file_assistant import ask_assistant


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Resume AI Assistant",
    page_icon="📄",
    layout="centered"
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("📄 Resume AI Assistant")

st.write(
    "Ask questions about the resumes in your "
    "`resumes` folder."
)


# --------------------------------------------------
# Example Queries
# --------------------------------------------------

with st.expander("💡 Example queries"):

    st.write("• Read all resumes in the resumes folder")

    st.write("• Find resumes mentioning Python experience")

    st.write("• Find candidates with Java experience")

    st.write("• Get me the youngest candidate")

    st.write("• Create a summary file for Resume1.pdf")


# --------------------------------------------------
# Chat History
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --------------------------------------------------
# Chat Input
# --------------------------------------------------

user_query = st.chat_input(
    "Ask something about your resumes..."
)


if user_query:

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_query)

    # Get AI response
    with st.chat_message("assistant"):

        with st.spinner("Analyzing resumes..."):

            try:

                response = ask_assistant(user_query)

                st.markdown(response)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response
                    }
                )

            except Exception as e:

                error_message = f"Error: {str(e)}"

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message
                    }
                )
