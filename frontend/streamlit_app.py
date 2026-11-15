
import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="Tamil Nadu Farmers AI Assistant",
    page_icon="🌾",
    layout="centered"
)

API_URL = "http://127.0.0.1:8000/ask"

# Application heading
st.title("Tamil Nadu Farmers AI Assistant")
st.caption(
    "Get information about agricultural schemes "
    "using official government documents."
)

st.divider()

# Question input form
with st.form("farmer_question_form"):

    language = st.selectbox(
        "Choose your language",
        ["English", "Tamil"]
    )

    question = st.text_area(
        "Enter your farming-related question",
        placeholder="Example: What is the minimum support price for green gram?",
        height=120
    )

    submitted = st.form_submit_button(
        "Ask Question",
        use_container_width=True
    )

# Process the question
if submitted:

    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Finding information in government documents..."):

            try:
                response = requests.post(
                    API_URL,
                    json={
                        "question": question,
                        "language": language
                    },
                    timeout=120
                )

                response.raise_for_status()
                result = response.json()

                st.subheader("Assistant's Answer")
                st.markdown(result["answer"])

            except requests.exceptions.ConnectionError:
                st.error(
                    "Cannot connect to the backend. "
                    "Please check whether FastAPI is running."
                )

            except requests.exceptions.Timeout:
                st.error("The request timed out. Please try again.")

            except requests.exceptions.RequestException as error:
                st.error(f"API request failed: {error}")

            except (KeyError, ValueError):
                st.error("The backend returned an unexpected response.")
