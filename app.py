import streamlit as st
import datetime
import requests
from app_utils import *

st.set_page_config(layout="wide")

@st.dialog(title="Chatbot",width=1200)
def show_diaog(itenary):

    st.write(itenary)

    submit = st.button("Sounds good! Let's go!")    
    if submit:
        update_itenerary(itenary)
        st.session_state.page = "Chatbot"
        st.rerun()
 
def travel_form():
    st.title("Welcome to AI Globertrotter,")
    st.title("Pierre")
 
    col1, col2 = st.columns(2)
 
    form = st.form(key="my_form", border=False)
 
    with form:
        with col1:
            travelling_to = st.text_input("What is your Destination?")
            flight_number = st.text_input("What is your flight number?")
            hotel_name = st.text_input("What is your hotel location?")
            eating_preference = st.selectbox("What is your food preference?", ("Veg", "Non-Veg", "Vegan", "Halal"), placeholder="Select food preference...")
        with col2:
            departure_date = st.date_input("When do you want to depart?")
            return_date = st.date_input("When do you want to return?")
            interests = st.multiselect("What are your interests?", ["Historical", "Nature", "Monuments", "Cultural"])
            comments = st.text_area("Do you have any comments?")
        submit = st.form_submit_button("Lets GO!")
 
        if submit:
            res = build_itinerary(travelling_to, flight_number, hotel_name, eating_preference, departure_date, return_date, interests, comments)
            show_diaog(res)
 
def chatbot_ui():
    st.title("AI Globertrotter")
    new_trip = st.button("New Trip")
    if new_trip:
        st.session_state.page = "Travel Form"
        st.rerun()
    
    # chat_container = st.container()
    # Left column: Display the itinerary loaded from the file
    itinerary = read_itenerary()  # Fetch the itinerary from the file
    st.text_area("Your Itinerary", itinerary, height=200, disabled=True)
 
    messages = st.container(height = 300, border=True)
    if prompt := st.chat_input("Say something"):
        # Clear previous messages
        messages.empty()
        bot_response = agent(prompt)
        # Display user message and bot response
        messages.chat_message("user").write(prompt)
        bot_response = f"Echo: {bot_response}"  # Replace with actual bot response logic
        messages.chat_message("assistant").write(bot_response)
        

 

if "page" not in st.session_state:
    st.session_state.page = "Travel Form"

if st.session_state.page == "Travel Form":
    travel_form()
elif st.session_state.page == "Chatbot":
    chatbot_ui()