import langchain
from dotenv import load_dotenv
import os
# from langchain.llms import Together
from langchain_core.prompts import PromptTemplate
import os
import openai
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAI
# from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from datetime import datetime
import requests
from parse import calculate_total_travel_time
from config import Tavily_description_prompt
from tavily import TavilyClient


load_dotenv()


@tool
def update_itenerary(res):
    
    """
    Tool to update the current itenerary. 
    If itenary changes please update the itenary.
    You have to make changes and pass in the whole itenerary.
    It does not take a prompt , you have pass in the whole itenerary.
    Stricltly call the itenary is ready.

    Args:
        res (str):  Whole Itenerary
    
    Returns:
        (str): Confirmation message
    """
    
    with open("itenerary.txt", "w") as f:
        f.write(res)
    return "The itenerary has been updated"

def read_itenerary():
    with open("itenerary.txt", "r") as f:
        file = f.read()
    return file

@tool
def direction_api(source, destination):
    """
    Tool to get the time taken to travel from one location to another by transit, walking, and driving.
    Stricltly call if times are to be calculated from point A to point B.
    You can also use this to verify the time taken to travel from one location to another.

    Args:
        source (str): Source location
        destination (str): Destination location

    Returns:
        str: A string containing the time taken to travel from the source to the destination by transit, walking, and driving
    """
    request_url_transit = f"""https://maps.googleapis.com/maps/api/directions/json?&destination={destination}&mode=transit&origin={source}&key={os.getenv("GOOGLE_API_KEY")}"""
    request_url_walking = f"""https://maps.googleapis.com/maps/api/directions/json?&destination={destination}&mode=walking&origin={source}&key={os.getenv("GOOGLE_API_KEY")}"""
    request_url_driving = f"""https://maps.googleapis.com/maps/api/directions/json?&destination={destination}&&origin={source}&key={os.getenv("GOOGLE_API_KEY")}"""

    response_transit = f"Time to travel by transit: {calculate_total_travel_time(requests.get(request_url_transit).json())}"
    response_walking = f"Time to travel by walking: {calculate_total_travel_time(requests.get(request_url_walking).json())}"
    response_driving = f"Time to travel by driving: {calculate_total_travel_time(requests.get(request_url_driving).json())}"

    return response_transit +" " + response_walking+ " "+ response_driving

def build_itinerary(travelling_to, flight_number, hotel_name, eating_preference, departure_date, return_date, interests, comments):
    tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

    # Step 2. Executing a simple search query
    response = tavily_client.get_search_context(f"Itenerary for {travelling_to}")
    print(response)
    input=f"""
    Help me plan a trip to {str(travelling_to)}. With my flight number {str(flight_number)} and hotel name
    {hotel_name}. Here are the dates you want to travel from {str(departure_date)} to {str(return_date)}.
    I want to eat {str(eating_preference)} food. I want to have {interests} in your trip.
    Here is also more things to consider {str(comments)}. Here are some iteneraries that I found:{response}"""
    
    client = openai.OpenAI(
        api_key=os.environ.get("TOGETHER_API_KEY"),
        base_url="https://api.together.xyz/v1",
        )
 
    response = client.chat.completions.create(
    model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
    messages=[
        {"role": "system", "content": "You are an expert travel advisor with 10+ years of experience. "},
        {"role": "user", "content": input},
    ]
    )

    completion  = response.choices[0].message.content
    update_itenerary(completion)
    build_itinerary_agent(completion)

    itenary = read_itenerary()

    return itenary

def build_itinerary_agent(itenenary):
    
    llm = ChatGroq(
        api_key=os.environ.get("GROQ_API_KEY"),
        model="llama3-groq-70b-8192-tool-use-preview"
    )
    tools = [TavilySearchResults(max_results=5, api_key=os.environ.get("TAVILY_API_KEY"), 
                                 description=Tavily_description_prompt), update_itenerary]


    prompt = ChatPromptTemplate.from_messages(
        [
        ("system","""
            You are a travel itenary verifier with 10+ years of experience. 
            Verify the itenerary using various web searches verify only information that sounds inaccurate , yoi only havr 5 websearches. rovide the correct itenerary. 
            If the itenerary is incorrect, update the itenerary with the correct itenerary.
            Check if a location exists and is open or not during a certain time. and food preferences match with the itenerary.
        """),
        ("human", "Here is the itenerary: {iterenary}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
    )
 
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=10)
    res = agent_executor.invoke({"iterenary": itenenary})

    return res["output"]


def call_everytime():
    time = datetime.now()
    time, date = time.strftime("%H:%M"), time.strftime("%Y-%m-%d")
    location = "Leonardo da Vinci–Fiumicino Airport, Rome, Italy"
    return date, time, location


def agent(input):
    llm = ChatGroq(
        api_key=os.environ.get("GROQ_API_KEY"),
        model="llama3-groq-70b-8192-tool-use-preview"
    )
    tools = [TavilySearchResults(max_results=1, api_key=os.environ.get("TAVILY_API_KEY")), direction_api, update_itenerary]
        
    itenary = read_itenerary()
    date, time, location = call_everytime()

    prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a helpful travel advisor and you provide on road assitance to the user. That the user could ask you any information. Also, you also have access to the following information.
            Current Location: {location} , Current Time: {time} , Current Date: {date}.
            The current itenary is as follows: {itenary}.
            Use the itenary to help the user. 
            Strictly only answer the questions asked and use the tools when you need it.""",
        ),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
    )
    # Construct the Tools agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=3)
    res = agent_executor.invoke({"input": input, "location": location, "time": time, "date": date, "itenary": itenary})

    return res["output"]

if __name__ == "__main__":

    destination = "Hyatt Regency, Salt Lake City, UT, USA"
    origin = "SLC Airport, Salt Lake City, UT, USA"

    directions = direction_api(origin, destination)
    print(directions)