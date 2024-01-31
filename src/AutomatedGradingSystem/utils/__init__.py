import streamlit as st
from src.AutomatedGradingSystem.logging import logger  # Import the logge
from src.AutomatedGradingSystem.components import modal


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
        cols = st.columns((2, 2, 1, 0.1))
        with cols[0]:
            question_text = st.text_area(
                f"Question {i+1}", value=question["text"], key=f"question_{i}"
            )
        with cols[1]:
            rubric_text = st.text_area(
                f"Rubric {i+1}", value=question["rubric"], key=f"rubric_{i}"
            )
        with cols[2]:
            remaining_marks = total_marks - allocated_marks + question["marks"]
            marks = st.slider(
                "", 0, int(remaining_marks), question["marks"], key=f"marks_{i}"
            )
            allocated_marks = sum(q["marks"] for q in st.session_state.questions)
        with cols[3]:
            if remaining_marks > 0:
                if st.button("➕", key=f"add_{i}"):
                    if allocated_marks >= total_marks:
                        modal.open()
                    else:
                        st.session_state.questions.append(
                            {"text": "", "rubric": "", "marks": 0}
                        )
            else:
                st.button("➕", disabled=True)
            if st.button("➖", key=f"remove_{i}"):
                remove_question(i)

        st.session_state.questions[i] = {
            "text": question_text,
            "rubric": rubric_text,
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
            st.write(f"- Text: {question['text']}")
            st.write(f"- Rubric: {question['rubric']}")
            st.write(f"- Marks: {question['marks']}")
        st.write(f"Custom Instructions:\n{rubric_dict['custom_instructions']}\n")

        st.subheader("Upload Student Submissions")
        uploaded_files = st.file_uploader(
            "Upload Student Submissions", type=["pdf", "zip"]
        )
        if uploaded_files:
            st.write("Submissions Uploaded:", uploaded_files)
            logger.info(f"Uploaded student submissions: {uploaded_files}")
        return rubric_dict


def remove_question(index_to_remove):
    # Remove the question at the specified index
    st.session_state.questions.pop(index_to_remove)
    # Rerun the app to refresh the state and UI
    st.experimental_rerun()
    logger.info(f"Removed question {index_to_remove}")  # Log question removal
