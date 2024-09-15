import streamlit as st
import datetime
import requests
from app_utils import *
 

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
    st.title("Pierie")
 
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
 
def get_current_location():
    pass




def chatbot_ui():
    st.title("AI Chatbot")
 
    chat_container = st.container()
 
    if 'messages' not in st.session_state:
        st.session_state.messages = []
 
    def update_chat(user_message, bot_response):
        st.session_state.messages.append({"user": user_message, "bot": bot_response})
 
    def generate_response(user_message):
        user_message = user_message.lower()
        if "time" in user_message:
            response = f"The current time is: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        elif "date" in user_message:
            response = f"Today's date is: {datetime.datetime.now().strftime('%Y-%m-%d')}"
        elif "location" in user_message:
            response = get_current_location()
        else:
            response = f"Echoing: {user_message}"
        return response
 
    with st.form(key="chat_form"):
        user_message = st.text_area("You:", height=150, placeholder="Type your message here...")
        submit_button = st.form_submit_button("Send")
 
    if submit_button and user_message:
        bot_response = generate_response(user_message)
        update_chat(user_message, bot_response)
 
    with chat_container:
        for message in st.session_state.messages:
            st.write(f"You: {message['user']}")
            st.write(f"Bot: {message['bot']}")
 
# Sidebar navigation
# st.sidebar.title("Navigation")

if "page" not in st.session_state:
    st.session_state.page = "Travel Form"
 
if st.session_state.page == "Travel Form":
    travel_form()
elif st.session_state.page == "Chatbot":
    chatbot_ui()