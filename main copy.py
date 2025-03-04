import streamlit as st
import pandas as pd
import os
import logging
from dotenv import load_dotenv
import google.generativeai as genai

# Configure logging
logging.basicConfig(filename="unit_converter.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

st.set_page_config(page_title="Unit Converter", layout="wide")
st.title("🔄 Unit Converter")

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_conversion(value, from_unit, to_unit, category):
    prompt = f"Convert {value} {from_unit} to {to_unit}. Return only the numeric value and unit, nothing else."
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    
    # Extracting only the number and unit
    result = response.text.strip().split("\n")[0]  # Taking the first line in case of multiple lines
    
    logging.info(f"Conversion Request: {value} {from_unit} to {to_unit} | Result: {result}")
    return result  # Returning only the essential part

unit_categories = [
    "Area", "Data Transfer Rate", "Digital Storage", "Energy", 
    "Frequency", "Fuel Economy", "Length", "Mass", "Plane Angle", 
    "Pressure", "Speed", "Temperature", "Time", "Volume"
]

unit_options = {
    "Area": ["Square meter", "Square kilometer", "Square centimeter", "Square millimeter", "Square micrometer", "Hectare", "Acre", "Square mile", "Square yard", "Square foot", "Square inch"],
    "Data Transfer Rate": ["Bit per second", "Kilobit per second", "Kibibit per second", "Megabit per second", "Mebibit per second", "Gigabit per second", "Gibibit per second", "Terabit per second", "Tebibit per second", "Petabit per second", "Pebibit per second", "Byte per second", "Kilobyte per second", "Kibibyte per second", "Megabyte per second", "Mebibyte per second", "Gigabyte per second", "Gibibyte per second", "Terabyte per second", "Tebibyte per second"],
    "Digital Storage": ["Bit", "Kilobit", "Kibibit", "Megabit", "Mebibit", "Gigabit", "Gibibit", "Terabit", "Tebibit", "Petabit", "Pebibit", "Byte", "Kilobyte", "Kibibyte", "Megabyte", "Mebibyte", "Gigabyte", "Gibibyte", "Terabyte", "Tebibyte"],
    "Energy": ["Joule", "Kilojoule", "Calorie", "Kilocalorie", "Watt-hour", "Kilowatt-hour", "Electronvolt", "British thermal unit", "US therm", "Foot-pound"],
    "Frequency": ["Hertz", "Kilohertz", "Megahertz", "Gigahertz"],
    "Fuel Economy": ["Miles per gallon", "Miles per gallon (Imperial)", "Kilometers per liter", "Liters per 100 kilometers"],
    "Length": ["Meter", "Kilometer", "Centimeter", "Millimeter", "Micrometer", "Nanometer", "Mile", "Yard", "Foot", "Inch", "Nautical mile"],
    "Mass": ["Kilogram", "Gram", "Milligram", "Microgram", "Ton", "Pound", "Ounce", "Carat", "Atomic mass unit"],
    "Plane Angle": ["Degree", "Radian", "Gradian", "Arcminute", "Arcsecond", "Turn"],
    "Pressure": ["Pascal", "Kilopascal", "Bar", "PSI", "Atmosphere"],
    "Speed": ["Meters per second", "Kilometers per hour", "Miles per hour", "Knot", "Mach"],
    "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
    "Time": ["Second", "Millisecond", "Microsecond", "Nanosecond", "Minute", "Hour", "Day", "Week", "Month", "Year", "Decade", "Century"],
    "Volume": ["Cubic meter", "Cubic centimeter", "Cubic millimeter", "Liter", "Milliliter", "US gallon", "US quart", "US pint", "US cup", "US fluid ounce", "US tablespoon", "US teaspoon", "Imperial gallon", "Imperial quart", "Imperial pint", "Imperial cup", "Imperial fluid ounce", "Imperial tablespoon", "Imperial teaspoon", "Cubic foot", "Cubic inch"]
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

if st.button("Convert"):
    result = get_conversion(convert, from_unit, to_unit, selected_category)
    st.session_state["converted_value"] = result  # Update session state
    st.rerun()  # Force Streamlit to refresh and update the UI
