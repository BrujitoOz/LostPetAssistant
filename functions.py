import json
import requests
import os
from openai import OpenAI
from prompts import assistant_instructions

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
AIRTABLE_API_KEY = os.environ['AIRTABLE_API_KEY']

# Init OpenAI Client
client = OpenAI(api_key=OPENAI_API_KEY)


# Add lead to Airtable
def create_lead(ownerName, phone, petName, email, petInfo):
  url = "https://api.airtable.com/v0/appGb93GAfGkUGLG5/Table%201"
  headers = {
      "Authorization": AIRTABLE_API_KEY,
      "Content-Type": "application/json"
  }
  data = {
      "records": [{
          "fields": {
              "ownerName": ownerName,
              "phone": phone,
              "petName": petName,
              "email": email,
              "petInfo": petInfo
          }
      }]
  }
  response = requests.post(url, headers=headers, json=data)
  if response.status_code == 200:
    print("Lead created successfully.")
    return response.json()
  else:
    print(f"Failed to create lead: {response.text}")


# Use GPT completion
def simplify_financial_data(data):
  try:
    data_str = json.dumps(data, indent=2)
    system_prompt = assistant_instructions

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[{
            "role": "system",
            "content": system_prompt
        }, {
            "role":
            "user",
            "content":
            f"Here is some data, parse and format it exactly as shown in the example: {data_str}"
        }],
        temperature=0)

    simplified_data = json.loads(completion.choices[0].message.content)
    print("Simplified Data:", simplified_data)
    return simplified_data

  except Exception as e:
    print("Error simplifying data:", e)
    return None


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
    file = client.files.create(file=open("knowledge.docx", "rb"),
                               purpose='assistants')

    assistant = client.beta.assistants.create(
        instructions=assistant_instructions,
        model="gpt-3.5-turbo-1106",
        tools=[{
            "type": "retrieval"
        }, {
            "type": "function",
            "function": {
                "name": "create_lead",
                "description": "Capture lead details and save to Airtable.",
                "parameters": {
                    "type":
                    "object",
                    "properties": {
                        "ownerName": {
                            "type": "string",
                            "description": "Name of the pet's owner."
                        },
                        "phone": {
                            "type": "string",
                            "description": "contact phone of the pet's owner."
                        },
                        "petName": {
                            "type": "string",
                            "description": "Name of the pet."
                        },
                        "email": {
                            "type": "string",
                            "description": "Owner's email for contact."
                        },
                        "petInfo": {
                            "type":
                            "string",
                            "description":
                            "Information about the pet like last time he was saw, breed, age, color, aditional description like clothes etc."
                        },
                    },
                    "required":
                    ["ownerName", "phone", "petName", "email", "petInfo"]
                }
            }
        }],
        file_ids=[file.id])

    # Create a new assistant.json file to load on future runs
    with open(assistant_file_path, 'w') as file:
      json.dump({'assistant_id': assistant.id}, file)
      print("Created a new assistant and saved the ID.")
    assistant_id = assistant.id

  return assistant_id
