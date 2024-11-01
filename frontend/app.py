import streamlit as st
import pathlib
from home import display_home
from predict import display_predictive_analysis
from past_data import display_past_data



def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
css_path = pathlib.Path("assets/styles.css")
load_css(css_path)



if 'page' not in st.session_state:
    st.session_state.page = "home"



st.sidebar.image("assets/images/logo.png", use_column_width=True)
if st.sidebar.button("🏠︎ Home", key="home"):
    st.session_state.page = "home"

st.sidebar.header("PREDICTIVE ANALYSIS")
st.sidebar.write("""Enter the parameters for your project, our predictive algorithms will analyze the inputs and 
                    provide estimated costs and timelines.""")
if st.sidebar.button("Predictive Analysis", key="navbutton"):
    st.session_state.page = "predictive"
st.sidebar.markdown('<div class="gradient-line"></div>', unsafe_allow_html=True)

st.sidebar.header("PROJECT HISTORY")
st.sidebar.write("""Explore metrics and interactive graphs that illustrate the data of previous projects.""")
if st.sidebar.button("Project History"):
    st.session_state.page = "past_data"
st.sidebar.markdown('<div class="gradient-line"></div>', unsafe_allow_html=True)



if st.session_state.page == "home":
    display_home()
elif st.session_state.page == "predictive":
    display_predictive_analysis()
elif st.session_state.page == "past_data":
    display_past_data()