
import streamlit as st
import requests
import html
import re

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Tamil Nadu Farmers AI Assistant",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

API_URL = "http://127.0.0.1:8000/ask"

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.stApp {
    background-color: #F5F8F1;
}

.main .block-container {
    max-width: 1050px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero {
    background: linear-gradient(120deg, #174D32, #347B4D);
    padding: 36px;
    border-radius: 18px;
    color: white;
    margin-bottom: 28px;
}

.hero h1 {
    color: white !important;
    font-size: 34px;
    font-weight: 750;
    margin-bottom: 10px;
}

.hero p {
    color: #E5F1E8 !important;
    font-size: 16px;
    margin-bottom: 0;
}

.section-heading {
    color: #174D32;
    font-size: 23px;
    font-weight: 700;
    margin-top: 22px;
    margin-bottom: 12px;
}

.stSelectbox label,
.stTextArea label {
    color: #174D32 !important;
    font-weight: 700 !important;
    font-size: 16px !important;
}

.stSelectbox div[data-baseweb="select"] {
    background-color: white;
    border-radius: 9px;
}

.stTextArea textarea {
    background-color: white !important;
    color: #26382C !important;
    border-radius: 10px !important;
    font-size: 16px !important;
}

.stTextArea textarea::placeholder {
    color: #68766B !important;
}

div.stButton > button,
div.stFormSubmitButton > button {
    background-color: #24623E;
    color: white;
    border-radius: 9px;
    border: none;
    font-weight: 600;
    min-height: 45px;
}

div.stButton > button:hover,
div.stFormSubmitButton > button:hover {
    background-color: #174D32;
    color: white;
    border: none;
}

.answer-card {
    background-color: white;
    padding: 24px;
    border-radius: 14px;
    border-left: 5px solid #347B4D;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    color: #26382C;
    line-height: 1.8;
    font-size: 16px;
}

.source-card {
    background-color: #E8F1E8;
    padding: 16px 20px;
    border-radius: 10px;
    color: #174D32;
    margin-top: 12px;
    font-size: 14px;
}

.info-card {
    background-color: #E8F1E8;
    padding: 22px;
    border-radius: 12px;
    color: #174D32;
    line-height: 1.9;
}

div[data-testid="stForm"] {
    background-color: #FFFFFF;
    padding: 20px;
    border: 1px solid #DCE6D9;
    border-radius: 14px;
}

div[data-testid="stCaptionContainer"] {
    color: #526257;
}

hr {
    border-color: #DCE6D9;
}


/* Improve source text readability */
.source-card,
.source-card p,
.source-card strong,
.stMarkdown p,
.stMarkdown strong {
    color: #174D32 !important;
}

.stLinkButton a {
    background-color: #24623E !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

.stLinkButton a:hover {
    background-color: #174D32 !important;
    color: #FFFFFF !important;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="hero">
    <h1>Tamil Nadu Farmers AI Assistant</h1>
    <p>
        Agricultural scheme information made easier.
        Ask questions in English or Tamil and explore
        information from government documents.
    </p>
</div>
""", unsafe_allow_html=True)


# =====================================================
# SUGGESTED QUESTIONS
# =====================================================

st.markdown(
    '<div class="section-heading">Suggested Questions</div>',
    unsafe_allow_html=True
)

suggestions = [
    "What is the minimum support price for green gram?",
    "Who is eligible for agricultural government schemes?",
    "What documents are required to apply for a scheme?"
]

if "farmer_question" not in st.session_state:
    st.session_state.farmer_question = ""

suggestion_columns = st.columns(3)

for index, suggestion in enumerate(suggestions):
    with suggestion_columns[index]:
        if st.button(
            suggestion,
            key=f"suggestion_{index}",
            use_container_width=True
        ):
            st.session_state.farmer_question = suggestion


# =====================================================
# QUESTION INPUT
# =====================================================

st.markdown(
    '<div class="section-heading">Ask Your Question</div>',
    unsafe_allow_html=True
)

language = st.selectbox(
    "Language / மொழி",
    ["English", "Tamil"]
)

if language == "Tamil":
    question_label = "உங்கள் விவசாயக் கேள்வியை உள்ளிடவும்"
    placeholder = "உதாரணம்: பச்சைப்பயறுக்கான குறைந்தபட்ச ஆதரவு விலை என்ன?"
    button_label = "கேள்வியைக் கேளுங்கள்"
else:
    question_label = "Enter your farming-related question"
    placeholder = "Example: What is the minimum support price for green gram?"
    button_label = "Ask Question"


with st.form("farmer_question_form"):

    question = st.text_area(
        question_label,
        value=st.session_state.farmer_question,
        placeholder=placeholder,
        height=130
    )

    submitted = st.form_submit_button(
        button_label,
        use_container_width=True
    )


# =====================================================
# PROCESS QUESTION
# =====================================================

if submitted:

    if not question.strip():
        st.warning("Please enter a question before submitting.")

    else:
        with st.spinner(
            "Searching government documents and preparing your answer..."
        ):
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

                answer = result.get("answer", "")
                sources = result.get("sources", [])

                st.markdown(
                    '<div class="section-heading">Assistant Response</div>',
                    unsafe_allow_html=True
                )

                safe_answer = html.escape(str(answer))
                safe_answer = safe_answer.replace("\\n", "<br>")

                st.markdown(
                    f'<div class="answer-card">{safe_answer}</div>',
                    unsafe_allow_html=True
                )

                # Display source references returned separately by FastAPI.
                st.markdown(
                    '<div class="section-heading">Government Sources</div>',
                    unsafe_allow_html=True
                )

                if sources:
                    for index, source in enumerate(sources):

                        source_name = source.get(
                            "name", "Government document"
                        )
                        source_url = source.get("url", "")
                        source_file = source.get("file", "")
                        source_page = source.get("page")

                        with st.container():
                            st.markdown(
                                f"**{source_name}**"
                            )

                            if source_page is not None:
                                st.caption(f"Page: {source_page}")

                            if (
                                isinstance(source_url, str)
                                and source_url.startswith(("https://", "http://"))
                            ):
                                st.link_button(
                                    "Open official source",
                                    source_url,
                                    key=f"government_source_{index}"
                                )
                            elif source_file:
                                st.caption(f"Document: {source_file}")

                            st.divider()

                else:
                    st.info(
                        "No source references were returned for this answer. "
                        "Please verify important information with the "
                        "relevant government department."
                    )

            except requests.exceptions.ConnectionError:
                st.error(
                    "Cannot connect to the backend. "
                    "Please check whether FastAPI is running."
                )

            except requests.exceptions.Timeout:
                st.error(
                    "The request timed out. Please try again."
                )

            except requests.exceptions.RequestException as error:
                st.error(f"API request failed: {error}")

            except (KeyError, ValueError):
                st.error(
                    "The backend returned an unexpected response."
                )


# ABOUT THE ASSISTANT
# =====================================================

st.divider()

st.markdown(
    '<div class="section-heading">About This Assistant</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="info-card">

<b>How does it work?</b><br><br>

1. Ask your question in English or Tamil.<br>
2. The assistant searches its indexed government documents.<br>
3. AI prepares an answer using the retrieved information.<br>
4. Source document and page references are displayed when available.

</div>
""", unsafe_allow_html=True)


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Tamil Nadu Farmers AI Assistant | Buildathon Prototype"
)

st.caption(
    "Please verify important agricultural and scheme-related "
    "information with the relevant government department."
)
