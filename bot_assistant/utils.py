from tenacity import retry, wait_random_exponential, stop_after_attempt

import json
from dotenv import load_dotenv
load_dotenv()
import os

import openai
openai.api_key=os.environ.get('OPENAI_API_KEY')
GPT_MODEL = "gpt-4-1106-preview"
MAX_MESSAGE_LENGTH = 10

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            tools=tools,
            temperature=0.0,
            tool_choice=tool_choice,
            messages=messages
        )

        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e



def run_conversation(messages):
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"],
                                 "description": "calculates the name of the unit of the temperature (example: “celsius”) when provided a unit of temperature."},


                        "day": {"type": "string", 
                                "description": "Calculates the day of the week (example: “Wednesday”) when provided."},
                    },
                    "required": ["location"],
                },
            },
        }
        ,
         {
            "type": "function",
            "function": {
                "name": "get_answer_to_question",
                "description": "Get the answer to the query. This is petroleum or drilling information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "The complete user query",
                        }
                    }
                },
            },
        },
         {
            "type": "function",
            "function": {
                "name": "plot_the_wells_on_map_based_on_proximity",
                "description": "plot specific wells on map based on proximity. Proximity could be based on latitude, longitude, radies, and could be only a specific well or a group of wells",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "well_names": {
                            "type": "string",#"array",
                            "items": {"type": "string"},
                            "description": "Taken from the user query. The well names of interest example:['1/2-1', '15/9-F11 A'].",
                        },
                        "latitude": {
                            "type": "number",
                            "description": "Taken from the user query. The latitude of the well.",
                        },
                        "longitude": {
                            "type": "number",
                            "description": "Taken from the user query. The longitude of the well.",
                        },
                        "radius": {
                            "type": "number",
                            "description": "Taken from the user query. The radius of the well.",
                        },
                    }
                },
            },
        },
        
        {"type": "function",
         "function": {
             "name": "plot_the_overview_of_the_norwegian_sea",
             "description": "plot the overview of the norwegian sea",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "Field_Name": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Taken from the user query. The name of the field. Must be all in capital letters. example:['GRANE', 'GULLFAKS'].",
                            
                        },

                        "Well_type": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Taken from the user query. Must be all in capital letters. example: The type of the well example:['EXPLORATION', 'DEVELOPMENT'].",
                        },
                        "Operator": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Taken from the user query. The company operator of the well.",
                        },
                        "Purpose": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Taken from the user query. The purpose of the well example:['OBSERVATION', 'APPRAISAL'].",
                        },
                        "Status": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Taken from the user query. The status of the well. example:['PLUGGED', 'DRILLING'].",
                        },
                        "Content": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Taken from the user query. The content of the well. example:['OIL', 'GAS', 'OIL SHOWS'].",
                        },
                
                        "latitude": {
                            "type": "number",
                            "description": "Taken from the user query. The latitude of the well.",
                        },
                        "longitude": {
                            "type": "number",
                            "description": "Taken from the user query. The longitude of the well.",
                        },
                        "radius": {
                            "type": "number",
                            "description": "Taken from the user query. The radius of the well.",
                        },
                        "well_names": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Taken from the user query. The well names of interest example:['1/2-1', '15/9-F11 A'].",
                        },

                    }
                },

         }
        }
    ]

    response = chat_completion_request(messages, tools=tools, tool_choice="auto", model=GPT_MODEL)
    response_message = response.choices[0]["message"]
    
    #check if response_message dict has tool_calls as key
    if 'tool_calls' in response_message:

        function_name =response['choices'][0]['message'].tool_calls[0].function.name
        json_response =json.loads(response['choices'][0]['message'].tool_calls[0].function.arguments)
       
        return {'json_response': json_response,'function_name':function_name }
    
    else:
        return {'json_response':response_message}


def message_appender(messages:list, current_single_message:dict):
    if len(messages) > MAX_MESSAGE_LENGTH:
       #remove the second and third elements
        messages.pop(1)
        messages.pop(1)

    messages.append(current_single_message)
    return messages