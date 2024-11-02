import streamlit as st


def display_home():
    image_path = "./frontend/images/CodeAnalytics.png"
    st.image(image_path, use_column_width=True)

    st.markdown(
        """
        <hr class="gradient-line">
        <h1 class="main-header">Welcome to CodeAnalytics!</h1>
        <p class="main-description">
            CodeAnalytics helps you accurately predict costs and time of your software projects based on your inputs.
            Whether you're planning a small application or a large-scale system, our tool analyzes project parameters and 
            provides reliable predictions for project duration, estimated costs, and adjusted functional points. 
            From the sidebar, you can choose to conduct predictive analysis or visualize historical data, empowering you to 
            make informed decisions and effectively plan your software development projects.
            <br><br>
            Let's get started on your project today!
        </p>
    """,
        unsafe_allow_html=True,
    )