import os
import streamlit as st
from src.AutomatedGradingSystem.logging import logger  # Import the logger
import streamlit as st
from src.AutomatedGradingSystem.components import modal
from src.AutomatedGradingSystem.utils import create_rubric_page
from src.AutomatedGradingSystem.utils import remove_question


# Initialize Session State for Questions with one empty question if not already set
if "questions" not in st.session_state or not st.session_state.questions:
    st.session_state.questions = [{"text": "", "rubric": "", "marks": 0}]


def main():
    st.title("AI-Powered Grading Tool")

    # Tabs for navigation
    tabs = st.tabs(["Home", "Upload Rubric", "Create Rubric"])
    with tabs[0]:
        st.write("Home Page Content Here")

    with tabs[1]:
        st.write("Upload Rubric Page Content Here")

    with tabs[2]:
        rubric_dict = create_rubric_page()
        if rubric_dict:
            logger.info("Rubric created successfully.")  # Log rubric creation


if __name__ == "__main__":
    main()
