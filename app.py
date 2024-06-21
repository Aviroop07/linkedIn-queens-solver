import streamlit as st
from PIL import Image
from functions import queen_solver

# Placeholder for the queen_solver function


st.title("LinkedIn Queens Solver")

# File uploader allows the user to upload an image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read the image file into a PIL Image
    image = Image.open(uploaded_file)
    
    # Display the original image
    # st.image(image, caption='Uploaded Image', use_column_width=True)
    st.write("")
    status = st.empty()
    try:
        status.success("Solution : ")

        # Process the image using the queen_solver function
        processed_image = queen_solver(image)

        # Display the processed image
        st.image(processed_image,  use_column_width=True)

    except ValueError as e:
        status.error(e)
