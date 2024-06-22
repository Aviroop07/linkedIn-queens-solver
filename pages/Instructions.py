import streamlit as st
from PIL import Image,ImageOps
import os

def add_css():
    st.markdown(
        """
        <style>
        .custom-image {
            border: 10px solid white;  /* Adjust the border size as needed */
            display: block;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


add_css()

st.write('''
## Hey there! 👋
          
### ***Rules to upload picture in the image uploader :***

    1. Image should be in .jpg, .jpeg, .png format
    2. Image should be less than 200MB
    3. Try to use image with as less noise as possible
    4. Do include black boundaries in the image as there is in the game
         
''')


col1,col2 = st.columns(2)

with col1:
    st.image(ImageOps.expand(Image.open('images/correct.jpeg'),border=30,fill='white'),width=200,caption='Valid Image')
    
with col2:
    st.image(ImageOps.expand(Image.open('images/wrong.jpeg'),border=30,fill='white'),width=200,caption='Invalid Image')

st.write('(The white border is just for visual purposes)')

st.write('''
### ***Happy Solving!***
''')