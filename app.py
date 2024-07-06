from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model=genai.GenerativeModel("gemini-pro-vision")

def get_gemini_response(image):
    prompt="""
    "Please analyze the uploaded image and identify any food items present. For each identified food item, provide the following information:

    1. A brief explanation of what the food is.
    2. A breakdown of the estimated calorie content in the following format:
        i. Total Calories:
        ii. Calories from Proteins:
        iii. Calories from Fats:
        iv.Calories from Carbohydrates:
        v. The nutritional value of the food, including macronutrients (proteins, fats, carbohydrates) and any significant micronutrients (vitamins, minerals).
        vi. An assessment of whether the food is considered nutritious or not.
    3. If the uploaded image does not contain any recognizable food items, respond with 'No food items detected in the image.'"
"""
    response=model.generate_content([prompt,image])
    return response.text
st.set_page_config(page_title="Meal Evaluator🥗")
st.title("Meal Evaluator")

st.subheader("Upload your meal")
img=st.file_uploader(label="Upload your image",type=["jpeg","jpg","png"])
if img is not None:
    img=Image.open(img)
    st.image(img,caption="uploaded image",use_column_width=True)
submit=st.button(label="submit")
if submit:
    with st.spinner('Please wait While the meal is being evaluated'):
        response = get_gemini_response(img)
    st.subheader("Response:")
    st.write(response)
