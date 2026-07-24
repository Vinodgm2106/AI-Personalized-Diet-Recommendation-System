
import streamlit as st
import google.generativeai as genai

genai.configure(
    api_key=st.secrets["GEMINI_API_KEY"]
)

model = genai.GenerativeModel("gemini-2.5-flash")

def ask_gemini(prompt):

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:

        if "429" in str(e):
            return """
    ⚠️ Gemini API quota exceeded.

    You have reached the free-tier request limit.

    Options:
    • Wait a few minutes and try again
    • Use a new Gemini API key
    • Upgrade your Gemini API plan

    The Diet Recommendation System will continue working normally.
    """
        else:
            return f"Error: {str(e)}"
        

