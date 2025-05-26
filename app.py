import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

# Streamlit UI
st.set_page_config(page_title="Government Scheme Explainer", layout="centered")
st.title("🛂 Government Scheme Explainer")

st.markdown("Enter your details to see which Indian government schemes may apply to you.")

income = st.number_input("Your Annual Income (INR)", min_value=0)
category = st.selectbox("Category", ["Student", "Farmer", "Unemployed", "Senior Citizen", "Entrepreneur", "Other"])
location = st.text_input("Your State or Region (optional)", "")

if st.button("🔍 Find Schemes"):
    with st.spinner("Thinking..."):
        prompt = (
            f"Suggest Indian government schemes for a person with these details:\n"
            f"- Annual Income: ₹{income}\n"
            f"- Category: {category}\n"
        )
        if location:
            prompt += f"- Location: {location}\n"
        prompt += "Explain each scheme briefly and how it helps the person."

        try:
            response = model.generate_content(prompt)
            st.success("Here are some matching government schemes:")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Failed to fetch schemes: {e}")
