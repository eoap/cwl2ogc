import streamlit as st
from cwl2ogc import load_converter_from_string_content



st.title("CWL to OGC API Processes inputs/outputs")

# Input TextArea
input_text = st.text_area("Enter your CWL here", height=200)

# Button
if st.button("Process Text"):
    if input_text.strip() == "":
        st.warning("Please enter some text before processing.")
    else:
        converter = load_converter_from_string_content(input_text)

        inputs = converter.get_inputs()
        outputs = converter.get_outputs()

        # Display Output Areas
        st.subheader("OGC API Processes inputs")
        st.json(inputs)

        st.subheader("OGC API Processes outputs")
        st.json(outputs)