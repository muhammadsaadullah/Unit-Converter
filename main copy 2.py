import streamlit as st
import os
import logging
from dotenv import load_dotenv
import google.generativeai as genai
from pint import UnitRegistry

# Configure logging
logging.basicConfig(filename="unit_converter.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

st.set_page_config(page_title="Unit Converter", layout="wide")
st.title("🔄 Unit Converter")

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Pint Unit Registry
ureg = UnitRegistry()

def get_pint_conversion(value, from_unit, to_unit):
    try:
        result = (value * ureg(from_unit)).to(to_unit)
        return str(result)
    except Exception as e:
        logging.error(f"Pint conversion error: {e}")
        return "Conversion Error"

def get_gemini_conversion(value, from_unit, to_unit):
    prompt = f"Convert {value} {from_unit} to {to_unit}. Return only the numeric value and unit, nothing else."
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    
    # Extracting only the number and unit
    result = response.text.strip().split("\n")[0]  # Taking the first line in case of multiple lines
    
    logging.info(f"Gemini Conversion: {value} {from_unit} to {to_unit} | Result: {result}")
    return result

unit_categories = [
    "Length", "Mass", "Time", "Temperature", "Speed", "Area", "Volume", "Energy", "Pressure"
]

unit_options = {
    "Length": ["meter", "kilometer", "centimeter", "millimeter", "mile", "yard", "foot", "inch"],
    "Mass": ["kilogram", "gram", "milligram", "pound", "ounce"],
    "Time": ["second", "minute", "hour", "day", "week", "year"],
    "Temperature": ["celsius", "fahrenheit", "kelvin"],
    "Speed": ["meter/second", "kilometer/hour", "mile/hour", "knot"],
    "Area": ["square meter", "square kilometer", "hectare", "acre", "square foot"],
    "Volume": ["liter", "milliliter", "cubic meter", "gallon", "pint"],
    "Energy": ["joule", "calorie", "kilojoule", "watt hour"],
    "Pressure": ["pascal", "bar", "psi", "atmosphere"]
}

selected_category = st.selectbox("Select a unit category:", unit_categories)

col1, col2 = st.columns(2)

if "converted_value" not in st.session_state:
    st.session_state["converted_value"] = ""

with col1:
    convert = st.number_input("Insert a number", key="input_number")
    from_unit = st.selectbox("From:", unit_options[selected_category])

with col2:
    converted_box = st.text_input("Converted number", value=st.session_state["converted_value"], key="converted_box")
    to_unit = st.selectbox("To:", unit_options[selected_category])

# Advanced conversion option
# advanced_conversion = st.checkbox("Enable Advanced Conversion (Uses Gemini AI)")

if st.button("Convert"):
    # if advanced_conversion:
    #     result = get_gemini_conversion(convert, from_unit, to_unit)
    # else:
    #     result = get_pint_conversion(convert, from_unit, to_unit)
    
    st.session_state["converted_value"] = result  # Update session state
    st.rerun()  # Force Streamlit to refresh and update the UI
