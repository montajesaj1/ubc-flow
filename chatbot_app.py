from re import A
import streamlit as st  # all streamlit commands will be available through the "st" alias
import chatbot_lib as glib  # reference to local lib script

courses_taken = ""

st.set_page_config(
    page_title="flow",
    page_icon="img/flow_logo.svg",
)

st.image("img/journey.svg")

st.sidebar.title("UBCFlow 🌊💬")  # page title
st.sidebar.write(
    "Welcome to UBCFlow! A generative AI student advising service for students studying tech at UBC 🤗"
)

st.sidebar.write(
    "This chatbot was made using AWS Bedrock, Anthropic's Claude LLM, and data compiled from UBC Student Service Centers."
)

with st.sidebar:
    with st.form("completed_courses_form"):
        text = st.text_area("Enter all the courses you've taken so far:")
        submitted = st.form_submit_button("Submit")
        if submitted:
            # Save the submitted text to the session state
            st.session_state["courses_taken"] = text
            st.success("Courses saved successfully!")

st.markdown(
    """<style>.css-1egvi7u {margin-top: -4rem;}</style>""", unsafe_allow_html=True
)
# Design change hyperlink href link color
st.markdown(
    """<style>.css-znku1x a {color: #9d03fc;}</style>""", unsafe_allow_html=True
)  # darkmode
st.markdown(
    """<style>.css-znku1x a {color: #9d03fc;}</style>""", unsafe_allow_html=True
)  # lightmode
# Design change height of text input fields headers
st.markdown(
    """<style>.css-qrbaxs {min-height: 0.0rem;}</style>""", unsafe_allow_html=True
)
# Design change spinner color to primary color
st.markdown(
    """<style>.stSpinner > div > div {border-top-color: #9d03fc;}</style>""",
    unsafe_allow_html=True,
)
# Design change min height of text input box
st.markdown(
    """<style>.css-15tx938{min-height: 0.0rem;}</style>""", unsafe_allow_html=True
)
# Design hide top header line
hide_decoration_bar_style = """<style>header {visibility: hidden;}</style>"""
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)
# Design hide "made with streamlit" footer menu area
hide_streamlit_footer = """<style>#MainMenu {visibility: hidden;}
                        footer {visibility: hidden;}</style>"""
st.markdown(hide_streamlit_footer, unsafe_allow_html=True)

if "memory" not in st.session_state:  # see if the memory hasn't been created yet
    st.session_state.memory = glib.get_memory()  # initialize the memory


if (
    "chat_history" not in st.session_state
):  # see if the chat history hasn't been created yet
    st.session_state.chat_history = []  # initialize the chat history


# Re-render the chat history (Streamlit re-runs this script, so need this to preserve previous chat messages)
for message in st.session_state.chat_history:  # loop through the chat history
    with st.chat_message(
        message["role"]
    ):  # renders a chat line for the given role, containing everything in the with block
        st.markdown(message["text"])  # display the chat content

input_text = st.chat_input("Chat with your advisor here")  # display a chat input box

if input_text:  # run the code in this if block after the user submits a chat message
    with st.chat_message("user"):  # display a user chat message
        st.markdown(input_text)  # renders the user's latest message

    st.session_state.chat_history.append(
        {"role": "user", "text": input_text}
    )  # append the user's latest message to the chat history

    chat_response = glib.get_chat_response(
        input_text=input_text,
        memory=st.session_state.memory,
    )  # call the model through the supporting library

    with st.chat_message("assistant"):  # display a bot chat message
        st.markdown(chat_response)  # display bot's latest response

    st.session_state.chat_history.append(
        {"role": "assistant", "text": chat_response}
    )  # append the bot's latest message to the chat history
