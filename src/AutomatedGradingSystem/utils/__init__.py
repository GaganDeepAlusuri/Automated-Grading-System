import streamlit as st
from src.AutomatedGradingSystem.logging import logger  # Import the logger
from src.AutomatedGradingSystem.components import modal
import zipfile
import os


def create_rubric_page():
    st.header("Create New Rubric")

    total_marks_text = st.text_input(
        "Enter Total Marks", value="100", key="total_marks"
    )
    try:
        total_marks = int(total_marks_text)
    except ValueError:
        st.error("Please enter a valid integer for total marks.")
        logger.error("Invalid input for total marks.")
        return

    allocated_marks = sum(q["marks"] for q in st.session_state.questions)

    def remove_question(index_to_remove):
        st.session_state.questions.pop(index_to_remove)
        st.experimental_rerun()
        logger.info(f"Removed question {index_to_remove}")

    for i, question in enumerate(st.session_state.questions):
        st.markdown("---")
        cols = st.columns((1, 1, 1, 1, 0.1))
        with cols[0]:
            question_text = st.text_area(
                f"Question {i+1}", value=question["question"], key=f"question_{i}"
            )
        with cols[1]:
            criteria_text = st.text_area(
                f"Criteria {i+1}", value=question["criteria"], key=f"criteria_{i}"
            )
        with cols[2]:
            deductions_text = st.text_area(
                f"Deductions {i+1}", value=question["deductions"], key=f"deductions_{i}"
            )
        with cols[3]:
            remaining_marks = total_marks - allocated_marks + question["marks"]
            marks = st.slider(
                "", 0, int(remaining_marks), question["marks"], key=f"marks_{i}"
            )
            allocated_marks = sum(q["marks"] for q in st.session_state.questions)
        with cols[4]:
            if remaining_marks > 0:
                if st.button("➕", key=f"add_{i}"):
                    if allocated_marks >= total_marks:
                        modal.open()
                    else:
                        st.session_state.questions.append(
                            {
                                "question": "",
                                "criteria": "",
                                "deductions": "",
                                "marks": 0,
                            }
                        )
            else:
                st.button("➕", disabled=True)
            if st.button("➖", key=f"remove_{i}"):
                remove_question(i)

        st.session_state.questions[i] = {
            "question": question_text,
            "criteria": criteria_text,
            "deductions": deductions_text,
            "marks": marks,
        }

    if modal.is_open():
        with modal.container():
            st.error(
                "You have allocated all available marks. Remove some marks if you want to redistribute."
            )

    custom_instructions = st.text_area("Custom Instructions", key="custom_instructions")

    if st.button("Save Rubric"):
        rubric_dict = {
            "questions": st.session_state.questions,
            "custom_instructions": custom_instructions,
        }
        logger.info(f"Total allocated marks: {allocated_marks}")
        st.subheader("Rubric Data Summary:")
        for i, question in enumerate(rubric_dict["questions"]):
            st.write(f"Question {i+1}:")
            st.write(f"- question: {question['question']}")
            st.write(f"- Criteria: {question['criteria']}")
            st.write(f"- Deductions: {question['deductions']}")
            st.write(f"- Marks: {question['marks']}")
        st.write(f"Custom Instructions:\n{rubric_dict['custom_instructions']}\n")
        return rubric_dict


def remove_question(index_to_remove):
    # Remove the question at the specified index
    st.session_state.questions.pop(index_to_remove)
    # Rerun the app to refresh the state and UI
    st.experimental_rerun()
    logger.info(f"Removed question {index_to_remove}")  # Log question removal


def ensure_directories_exist():
    os.makedirs("submissions", exist_ok=True)
    os.makedirs("datasets", exist_ok=True)


def extract_and_save_submissions_and_datasets(uploaded_zip_file, uploaded_datasets):
    ensure_directories_exist()
    submissions_dir = "submissions"
    datasets_dir = "datasets"

    if uploaded_zip_file is not None:
        with zipfile.ZipFile(uploaded_zip_file, "r") as zip_ref:
            zip_ref.extractall(submissions_dir)
        submissions_extracted = True
    else:
        submissions_extracted = False

    if uploaded_datasets is not None:
        with zipfile.ZipFile(uploaded_datasets, "r") as zip_ref:
            zip_ref.extractall(datasets_dir)
        datasets_extracted = True
    else:
        datasets_extracted = False

    return submissions_extracted, datasets_extracted
