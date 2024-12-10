from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from pymongo import MongoClient
import os
import logging
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

# Load environment variables
IBM_API_KEY = os.getenv("IBM_API_KEY")
IBM_SERVICE_URL = os.getenv("IBM_SERVICE_URL")
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DATABASE_NAME", "langchain_chatbot")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "data")

if not IBM_API_KEY or not IBM_SERVICE_URL:
    logging.error("IBM_API_KEY or IBM_SERVICE_URL is not set")

# MongoDB setup
client = MongoClient(MONGODB_URI)
collection = client[DB_NAME][COLLECTION_NAME]

# IBM Watson Assistant setup
authenticator = IAMAuthenticator(IBM_API_KEY)
assistant = AssistantV2(version='2021-06-14', authenticator=authenticator)
assistant.set_service_url(IBM_SERVICE_URL)

def query_ibm_assistant(query: str):
    try:
        # With this updated line, adding the 'environment_id' parameter
        response = assistant.message_stateless(
            assistant_id="e703007f-3124-4aef-9628-5927263f9583",  # Replace with your real Assistant ID
            environment_id="11fb57aa-d586-4661-ad33-43401cb4e5c2",  # Replace with your real Environment ID
            input={"message_type": "text", "text": query}
        ).get_result()


        return response.get("output", {}).get("generic", [])
    except Exception as e:
        logging.error(f"Error querying IBM Assistant: {e}")
        raise HTTPException(status_code=500, detail=f"IBM Assistant error: {str(e)}")

async def check_mongo_connection():
    try:
        mongo_uri = os.getenv("MONGODB_URI")  # Get the MongoDB URI from environment variables
        client = MongoClient(mongo_uri)
        client.admin.command('ping')  # Ping MongoDB server
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"MongoDB connection failed: {e}")
