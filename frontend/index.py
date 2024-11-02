import streamlit as st
import pathlib
from home import display_home
from predict import display_predictive_analysis
from past_data import display_past_data

# Set page title and layout
st.set_page_config(page_title="Light Mode App", page_icon="🌞", layout="centered")

# Inject CSS and JavaScript to enforce light mode and hide theme toggle
st.markdown(
    """
    <style>
    /* Enforce light theme colors */
    :root {
        --primary-color: #1f77b4;
        --background-color: #ffffff;
        --secondary-background-color: #f0f2f6;
        --text-color: #000000;
        --font: "sans-serif";
    }

    /* Set the main background and text colors */
    body {
        background-color: var(--background-color);
        color: var(--text-color);
    }

    /* Set the sidebar background */
    .css-1d391kg {
        background-color: var(--secondary-background-color);
    }
    </style>

    <script>
    // JavaScript to enforce light mode and remove theme toggle button
    const setLightMode = () => {
        // Remove the theme toggle button
        const themeToggle = window.parent.document.querySelector('[data-testid="stThemeToggle"]');
        if (themeToggle) {
            themeToggle.style.display = 'none';
        }
        // Force light mode by setting the class
        const bodyClassList = window.parent.document.body.classList;
        if (!bodyClassList.contains("light")) {
            bodyClassList.remove("dark");
            bodyClassList.add("light");
        }
    };
    // Run the setLightMode function when the page loads
    window.addEventListener("load", setLightMode);
    </script>
    """,
    unsafe_allow_html=True,
)


def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


css_path = pathlib.Path("./frontend/style/styles.css")
load_css(css_path)


if "page" not in st.session_state:
    st.session_state.page = "home"


st.sidebar.image("./frontend/images/logo.png", use_column_width=True)
if st.sidebar.button("🏠︎ Home", key="home"):
    st.session_state.page = "home"

st.sidebar.header("PREDICTIVE ANALYSIS")
st.sidebar.write(
    """Enter parameters for your project, our predictive algorithms will analyze the inputs and 
                    provide estimated costs and timelines."""
)
if st.sidebar.button("Predictive Analysis", key="navbutton"):
    st.session_state.page = "predictive"
st.sidebar.markdown('<div class="gradient-line"></div>', unsafe_allow_html=True)

st.sidebar.header("PROJECT HISTORY")
st.sidebar.write(
    """Explore metrics and interactive graphs that illustrate data of previous projects."""
)
if st.sidebar.button("Project History"):
    st.session_state.page = "past_data"
st.sidebar.markdown('<div class="gradient-line"></div>', unsafe_allow_html=True)


if st.session_state.page == "home":
    display_home()
elif st.session_state.page == "predictive":
    display_predictive_analysis()
elif st.session_state.page == "past_data":
    display_past_data()
