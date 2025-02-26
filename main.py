import streamlit as st
import pandas as pd
import os
from openai import OpenAI

st.set_page_config(page_title="Unit Converter", layout="wide")
st.title("🔄 Unit Converter")

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

with col1:
    convert = st.number_input("Insert a number")
    from_unit = st.selectbox("From:", unit_options[selected_category])
    
with col2:
    converted = st.number_input("Converted number")
    to_unit = st.selectbox("To:", unit_options[selected_category])
    
