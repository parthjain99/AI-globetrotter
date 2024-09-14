import langchain 
from dotenv import load_dotenv
import os
# from langchain.llms import Together
from langchain_core.prompts import PromptTemplate
import os
import openai




load_dotenv()
def build_itinerary(travelling_to, flight_number, hotel_name, eating_preference, departure_date, return_date, interests, comments):

    template=f"""
    You can help me plan a trip to {str(travelling_to)} with my flight number {str(flight_number)} and hotel name 
    {hotel_name}. Here are the dates you want to travel from {str(departure_date)} to {str(return_date)}.
    You want to eat {str(eating_preference)} food. You want to have {interests} in your trip.
    Here is also I am interested in {str(comments)}"""

    client = openai.OpenAI(
        api_key=os.environ.get("TOGETHER_API_KEY"),
        base_url="https://api.together.xyz/v1",
        )

    response = client.chat.completions.create(
    model="meta-llama/Llama-3-8b-chat-hf",
    messages=[
        {"role": "system", "content": "You are an expert travel advisor with 10+ years of experience. "},
        {"role": "user", "content": template},
    ]
    )
    completion  = response.choices[0].message.content

    return completion
