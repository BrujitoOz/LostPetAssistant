import os
import json
import requests
from openai import OpenAI
from dotenv import load_dotenv
from prompts import assistant_instructions

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")

# Init OpenAI Client
client = OpenAI(api_key=OPENAI_API_KEY)

# Add lead to Airtable
def create_lead(owner_name, phone, pet_name, email, pet_info):
    url = "https://api.airtable.com/v0/appGb93GAfGkUGLG5/LostPet"
    headers = {
        "Authorization": AIRTABLE_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "records": [{
            "fields": {
                "owner_name": owner_name,
                "phone": phone,
                "pet_name": pet_name,
                "email": email,
                "pet_info": pet_info
            }
        }]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Lead created successfully.")
        return response.json()
    else:
        print(f"Failed to create lead: {response.text}")

# Create or load assistant
def create_assistant(client):
    assistant_file_path = 'assistant.json'
    # If there is an assistant.json file already, then load that assistant
    if os.path.exists(assistant_file_path):
        with open(assistant_file_path, 'r') as file:
            assistant_data = json.load(file)
            assistant_id = assistant_data['assistant_id']
            print("Loaded existing assistant ID.")
    else:
        # If no assistant.json is present, create a new assistant
        file = client.files.create(file=open("knowledge.docx", "rb"), purpose='assistants')

        assistant = client.beta.assistants.create(
            instructions=assistant_instructions,
            model="gpt-4o",
            tools=[
                {
                    "type": "retrieval"
                },
                {
                    "type": "function",
                    "function": {
                        "name": "create_lead",
                        "description": "Capture lead details and save to Airtable.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "owner_name": {
                                    "type": "string",
                                    "description": "Name of the pet's owner."
                                },
                                "phone": {
                                    "type": "string",
                                    "description": "contact phone of the pet's owner."
                                },
                                "pet_name": {
                                    "type": "string",
                                    "description": "Name of the pet."
                                },
                                "email": {
                                    "type": "string",
                                    "description": "Owner's email for contact."
                                },
                                "pet_info": {
                                    "type":
                                    "string",
                                    "description":
                                    "Information about the pet like last time he was saw, breed, age, color, aditional description like clothes etc."
                                },
                            },
                            "required": ["owner_name", "phone", "pet_name", "email", "pet_info"]
                        }
                    }
                }
            ],
            file_ids=[file.id]
        )
        # Create a new assistant.json file to load on future runs
        with open(assistant_file_path, 'w') as file:
            json.dump({'assistant_id': assistant.id}, file)
            print("Created a new assistant and saved the ID.")
        assistant_id = assistant.id
    return assistant_id