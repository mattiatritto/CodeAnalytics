import streamlit as st
import datetime
import time
import pandas as pd
import plotly.express as px
import requests

input_data = ""
#endpoint = "https://codeanalytics-backend-image-771804227712.us-central1.run.app"
endpoint = "http://codeanalytics-backend:8080"

def display_predictive_analysis():
    st.markdown(
        "<h1 style='color:#00A3E0;'>📝 Predictive Analysis</h1>", unsafe_allow_html=True
    )

    with st.form("estimation_form"):
        EI = st.number_input(
            "📥 External Inputs",
            min_value=0,
            step=1,
            help="Input activities, such as acquiring, entering, or updating data",
        )

        EQ = st.number_input(
            "🔍 External Queries",
            min_value=0,
            step=1,
            help="Inquiry activities, like providing answers to questions or searching for information",
        )

        EO = st.number_input(
            "📊 External Outputs",
            min_value=0,
            step=1,
            help="Output activities, such as calculating, printing, or displaying data",
        )

        ILF = st.number_input(
            "📂 Internal Logical Files",
            min_value=0,
            step=1,
            help="Internal files within the application that store logical data",
        )

        EIF = st.number_input(
            "🔗 External Interface Files",
            min_value=0,
            step=1,
            help="External files that interact with data outside the application",
        )

        num_people = st.slider(
            "👥 Number of Developers",
            1,
            50,
            5,
            help="Specify how many people will be working on the project",
        )

        hourly_wage = st.number_input(
            "💵 Hourly Wage (€)",
            min_value=0.0,
            step=0.01,
            help="Enter the hourly wage for the project",
        )

        starting = st.date_input("🗓️ Project Start Date")

        influence_choices = [
            "0 Not Present/No Influence",
            "1 Minor Influence",
            "2 Moderate Influence",
            "3 Average Influence",
            "4 Significant Influence",
            "5 Strong, Generalized Influence",
        ]

        influence_mapping = {choice: int(choice[0]) for choice in influence_choices}

        data_communication = st.selectbox(
            "📶 Data Communication",
            influence_choices,
            help="Assess the requirement for data communication in the system",
        )
        distributed_processing = st.selectbox(
            "🌐 Distributed Data Processing",
            influence_choices,
            help="Evaluate if the system requires distributed processing capabilities",
        )
        performance = st.selectbox(
            "⚡ Performance",
            influence_choices,
            help="Indicate the significance of performance constraints in the project",
        )
        use_configuration = st.selectbox(
            "⚙️ Heavily Use of Configuration",
            influence_choices,
            help="Determine if extensive configuration is needed for the application",
        )
        transaction_rate = st.selectbox(
            "📅 Transaction Rate",
            influence_choices,
            help="Select the frequency of transactions expected in the system",
        )
        online_data_entry = st.selectbox(
            "🖱️ Online Data Entry",
            influence_choices,
            help="Assess whether interactive data entry is required for users",
        )
        user_efficiency = st.selectbox(
            "💡 End-User Efficiency",
            influence_choices,
            help="Indicate the importance of user efficiency in the application",
        )
        online_update = st.selectbox(
            "🔁 Online Update",
            influence_choices,
            help="Evaluate the need for interactive updates within the system",
        )
        computational_complexity = st.selectbox(
            "🧩 Computational Complexity",
            influence_choices,
            help="Assess whether the system has high computational complexity",
        )
        reusability = st.selectbox(
            "🔄 Reusability",
            influence_choices,
            help="Determine the reusability of components in the project",
        )
        installation_ease = st.selectbox(
            "📦 Installation Ease",
            influence_choices,
            help="Indicate how important ease of installation is for the system",
        )
        operation_ease = st.selectbox(
            "🛠️ Operation Ease",
            influence_choices,
            help="Evaluate how critical ease of operation is for end users",
        )
        multiple_sites = st.selectbox(
            "🌍 Multiple Sites",
            influence_choices,
            help="Assess whether the system will be deployed across multiple locations",
        )
        ease_of_modification = st.selectbox(
            "✏️ Facilitate Change",
            influence_choices,
            help="Indicate the importance of ease of modification in the project",
        )

        submitted = st.form_submit_button("🚀 Submit")

        if submitted:

            gsc_values = [
                influence_mapping[data_communication],
                influence_mapping[distributed_processing],
                influence_mapping[performance],
                influence_mapping[use_configuration],
                influence_mapping[transaction_rate],
                influence_mapping[online_data_entry],
                influence_mapping[user_efficiency],
                influence_mapping[online_update],
                influence_mapping[computational_complexity],
                influence_mapping[reusability],
                influence_mapping[installation_ease],
                influence_mapping[operation_ease],
                influence_mapping[multiple_sites],
                influence_mapping[ease_of_modification],
            ]

            input_data = {
                "ilf_count": ILF,
                "eif_count": EIF,
                "ei_count": EI,
                "eo_count": EO,
                "eq_count": EQ,
                "gsc_values": gsc_values,
                "start_date": str(starting),
                "hourly_pay": hourly_wage,
                "num_people": num_people,
            }

            st.write("Calculating your estimates...")

            response = requests.post(endpoint + "/predict", json=input_data)
            if response.status_code == 200:
                result = response.json()
                predicted_duration, predicted_cost, afp = result

                col1, col2, col3 = st.columns(3)
                col1.metric(label="Cost", value=f"€{predicted_cost:.2f}")
                col2.metric(label="Duration", value=f"{predicted_duration} hours")
                col3.metric(
                    label="AFP",
                    value=f"{afp:.2f}",
                    help="Adjusted Function Points",
                )

                st.write(f"**Start Date:** {starting}")

                # Animated progress bar for project duration
                progress = st.progress(0)
                for i in range(1, 101):
                    progress.progress(i)
                    time.sleep(0.02)
                end_date = starting + datetime.timedelta(days=predicted_duration/8)
                st.write(f"**Estimated End Date:** {end_date.strftime('%Y-%m-%d')}")

                # Create a DataFrame to represent the timeline
                timeline_data = pd.DataFrame(
                    {
                        "Date": [starting, end_date],
                        "Progress": ["Start", "End"],
                    }
                )

                # Plot
                fig = px.line(timeline_data, x="Date", y="Progress", markers=True)
                fig.update_yaxes(range=[-0.5, 1.5])
                st.plotly_chart(fig)

                st.success("✅ Analysis complete!")

                report_response = requests.post(endpoint + "/report", json=input_data)
                if report_response.status_code == 200:
                    docx_file = report_response.content
                    st.session_state.report_generated = True
                    st.session_state.docx_file = docx_file
                else:
                    st.error("Failed to generate the report.")
            else:
                st.error("Failed to fetch predictions.")

    if "report_generated" in st.session_state and st.session_state.report_generated:
        st.download_button(
            label="⬇️ Download Report",
            data=st.session_state.docx_file,
            file_name="Report CodeAnalytics.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
