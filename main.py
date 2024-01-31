import os
import streamlit as st
from src.AutomatedGradingSystem.logging import logger  # Import the logger

# Initialize Session State for Questions with one empty question if not already set
if "questions" not in st.session_state or not st.session_state.questions:
    st.session_state.questions = [{"text": "", "rubric": "", "marks": 0}]


def create_rubric_page():
    st.header("Create New Rubric")

    # Total Marks Input as a text field
    total_marks_text = st.text_input(
        "Enter Total Marks", value="100", key="total_marks"
    )
    # Validate and convert total marks to an integer
    try:
        total_marks = int(total_marks_text)
    except ValueError:
        st.error("Please enter a valid integer for total marks.")
        logger.error("Invalid input for total marks.")
        return

    # Calculate the total allocated marks
    allocated_marks = sum(q["marks"] for q in st.session_state.questions)

    # Display each question with a remove button
    for i, question in enumerate(st.session_state.questions):
        st.markdown("---")  # Draw a line separator
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
            if remaining_marks > 0:
                marks = st.slider(
                    "", 0, int(remaining_marks), question["marks"], key=f"marks_{i}"
                )
            else:
                st.warning(
                    "You have allocated all available marks. Remove some marks if you want to redistribute."
                )
                marks = question["marks"]  # Keep the current value
        with cols[3]:
            if remaining_marks > 0:
                if st.button("➕", key=f"add_{i}") and remaining_marks > 0:
                    st.session_state.questions.append(
                        {"text": "", "rubric": "", "marks": 0}
                    )
            else:
                st.button(
                    "➕", disabled=True
                )  # Gray out the button when the limit is reached
            if st.button("➖", key=f"remove_{i}"):
                remove_question(i)
                logger.info(f"Removed question {i}")  # Log question removal

        # Update the question dictionary with the latest input
        st.session_state.questions[i] = {
            "text": question_text,
            "rubric": rubric_text,
            "marks": marks,
        }
    # Custom Instructions at the bottom
    custom_instructions = st.text_area("Custom Instructions", key="custom_instructions")

    # Save Rubric Button
    if st.button("Save Rubric"):
        rubric_dict = {
            "questions": st.session_state.questions,
            "custom_instructions": custom_instructions,
        }
        logger.info(f"Total allocated marks: {allocated_marks}")  # Log allocated marks

        # Display rubric data in a formatted way
        st.subheader("Rubric Data Summary:")
        for i, question in enumerate(rubric_dict["questions"]):
            st.write(f"Question {i+1}:")
            st.write(f"- Text: {question['text']}")
            st.write(f"- Rubric: {question['rubric']}")
            st.write(f"- Marks: {question['marks']}")
        st.write(f"Custom Instructions:\n{rubric_dict['custom_instructions']}\n")

        # Ask the user to upload student submissions
        st.subheader("Upload Student Submissions")
        uploaded_files = st.file_uploader(
            "Upload Student Submissions", type=["pdf", "zip"]
        )
        if uploaded_files:
            st.write("Submissions Uploaded:", uploaded_files)
            logger.info(
                f"Uploaded student submissions: {uploaded_files}"
            )  # Log file upload

        # Return the rubric_dict dictionary
        return rubric_dict


def remove_question(index_to_remove):
    # Remove the question at the specified index
    st.session_state.questions.pop(index_to_remove)
    # Rerun the app to refresh the state and UI
    st.experimental_rerun()
    logger.info(f"Removed question {index_to_remove}")  # Log question removal


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
