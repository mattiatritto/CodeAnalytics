import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from io import StringIO

endpoint = "http://codeanalytics-backend:8000"


def display_past_data():
    st.markdown(
        "<h1 style='color:#00A3E0;'>Project History</h1>", unsafe_allow_html=True
    )

    # Fetch data from the endpoint

    data_url = endpoint + "/data"

    try:
        response = requests.get(data_url)
        df = pd.read_csv(StringIO(response.text))
    except requests.RequestException as e:
        st.error(f"An error occurred while fetching the dataset: {e}")
        return

    st.markdown(
        '<div class="main-section">Data Highlights</div>', unsafe_allow_html=True
    )
    st.markdown(
        '<div class="sub-section">Functional Components</div>', unsafe_allow_html=True
    )

    functional_components = ["Input", "Output", "Enquiry", "File", "Interface"]

    # Compute mean and std of each functional component

    mean_values = df[functional_components].mean()
    std_values = df[functional_components].std()
    stats = pd.DataFrame({"Mean": mean_values, "Standard Deviation": std_values})
    stats = stats.round(2)

    html_table = stats.to_html(classes="custom-table", border=0, escape=False)
    st.markdown(html_table, unsafe_allow_html=True)

    # Compute low, average and high effort
    low_value = df["Effort"].min()
    average_value = df["Effort"].mean()
    high_value = df["Effort"].max()
    st.markdown(
        '<div class="sub-section">Effort Overview</div>', unsafe_allow_html=True
    )
    st.markdown('<div class="highlight-section">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f'<div class="low">Low: €{low_value:.2f}</div>', unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f'<div class="average">Average: €{average_value:.2f}</div>',
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f'<div class="high">High: €{high_value:.2f}</div>', unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="main-section">Graphs</div>', unsafe_allow_html=True)

    # Pair Plot of AFP, Effor and Duration

    fig = px.scatter_matrix(
        df,
        dimensions=["AFP", "Effort", "Duration"],
        color_discrete_sequence=["#00A3E0"],
        title="Pairplot of AFP, Effort, and Duration",
    )
    fig.update_traces(diagonal_visible=True)
    fig.update_layout(
        title_font=dict(size=16, color="#00A3E0", family="Arial, sans-serif"),
        height=600,
        plot_bgcolor="rgba(0, 0, 0, 0)",
    )
    st.plotly_chart(fig)

    # Histogram of Effort

    st.markdown('<div class="sub-section">Effort</div>', unsafe_allow_html=True)
    fig = px.histogram(
        df,
        x="Effort",
        nbins=10,
        title="Distribution of Effort",
        color_discrete_sequence=["#00A3E0"],
        template="plotly_white",
    )
    fig.update_layout(
        title_font=dict(size=16, color="#00A3E0", family="Arial, sans-serif"),
        xaxis_title="Effort (hours)",
        yaxis_title="Frequency",
        xaxis=dict(titlefont=dict(size=12, color="#00A3E0")),
        yaxis=dict(titlefont=dict(size=12, color="#00A3E0")),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        showlegend=False,
    )
    st.plotly_chart(fig)

    # Histogram of Duration

    st.markdown('<div class="sub-section">Duration</div>', unsafe_allow_html=True)
    fig = px.histogram(
        df,
        x="Duration",
        nbins=10,
        title="Distribution of Duration",
        color_discrete_sequence=["#00A3E0"],
        template="plotly_white",
    )
    fig.update_layout(
        title_font=dict(size=16, color="#00A3E0", family="Arial, sans-serif"),
        xaxis_title="Effort (hours)",
        yaxis_title="Frequency",
        xaxis=dict(titlefont=dict(size=12, color="#00A3E0")),
        yaxis=dict(titlefont=dict(size=12, color="#00A3E0")),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        showlegend=False,
    )
    st.plotly_chart(fig)
    st.markdown("<hr class='gradient-line'>", unsafe_allow_html=True)
