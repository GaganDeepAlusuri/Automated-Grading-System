import os
import streamlit as st
from src.AutomatedGradingSystem.logging import logger
from src.AutomatedGradingSystem.components import modal
from src.AutomatedGradingSystem.utils import (
    create_rubric_page,
    remove_question,
    extract_and_save_submissions_and_datasets,
)
import json

# Initialize Session State for Questions with one empty question if not already set
if "questions" not in st.session_state or not st.session_state.questions:
    st.session_state.questions = [
        {"question": "", "rubric": "", "criteria": "", "deductions": "", "marks": 0}
    ]


def main():
    st.title("AI-Powered Grading Tool")

    if "form_submitted" not in st.session_state:
        st.session_state.form_submitted = False

    tabs = st.tabs(["Home", "Upload Rubric", "Create Rubric"])

    with tabs[0]:
        st.write("Home Page Content Here")

    with tabs[1]:
        st.write("Upload Rubric Page Content Here")

    with tabs[2]:
        rubric_dict = create_rubric_page()
        if rubric_dict:
            logger.info("Rubric created successfully.")
            with open("rubric.json", "w") as outfile:
                json.dump(rubric_dict, outfile, indent=4)
            st.success("Rubric saved successfully.")

        with st.form("upload_form"):
            uploaded_zip_file = st.file_uploader(
                "Upload Student Submissions (ZIP)", type=["zip"]
            )
            uploaded_datasets = st.file_uploader("Upload Datasets (ZIP)", type=["zip"])
            submitted = st.form_submit_button("Upload ZIP and Datasets")

        if submitted or st.session_state.form_submitted:
            st.session_state.form_submitted = True
            (
                submissions_extracted,
                datasets_extracted,
            ) = extract_and_save_submissions_and_datasets(
                uploaded_zip_file, uploaded_datasets
            )

            if submissions_extracted:
                st.success("Submission ZIP file uploaded and extracted successfully.")
            else:
                st.error("Failed to upload or extract submissions.")

            if datasets_extracted:
                st.success("Datasets ZIP file uploaded and extracted successfully.")
            else:
                st.error("Failed to upload or extract datasets.")


if __name__ == "__main__":
    main()
