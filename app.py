import streamlit as st 
import langchain
import dotenv
from app_utils import build_itinerary

st.title("Welcome to AI Globertrotter,")
st.title("Pierie")

col1, col2 = st.columns(2)


form = st.form(key="my_form", border=False,  clear_on_submit=True)

with form: 
    with col1: 
        travelling_to = st.text_input("What is your Destination?")
        flight_number = st.text_input("What is your flight number?")
        hotel_name = st.text_input("What is your hotel location?")
        eating_preference = st.selectbox("What is your food preference?", ("Veg", "Non-Veg", "Vegan", "Halal"), placeholder="Select food preference...")
    with col2:
        departure_date = st.date_input("When do you want to depart?")
        return_date = st.date_input("When do you want to return?")
        interests = st.multiselect("What are your interests?", ["Historical", "Nature", "Monumnets", "Cultural"])
        comments = st.text_area("Do you have any comments?")
    submit = st.form_submit_button(" Lets GO!")
    
    if submit :
        res = build_itinerary(travelling_to, flight_number, hotel_name, eating_preference, departure_date, return_date, interests, comments)
        st.write(res)