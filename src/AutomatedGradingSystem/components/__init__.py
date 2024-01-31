from streamlit_modal import Modal  # Import the Modal

# Initialize the Modal
modal = Modal(
    "Allocation Limit Reached",
    key="allocation-limit-modal",
    padding=20,  # Optional: default value
    max_width=744,  # Optional: default value
)
