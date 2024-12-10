from fastapi import FastAPI, HTTPException
from app.routers import router
from app.services import check_mongo_connection
from dotenv import load_dotenv
import os

app = FastAPI(title="My FastAPI with MongoDB")

# Load environment variables
load_dotenv()

# Include the router with API endpoints
app.include_router(router)

# Startup event to check MongoDB connection
@app.on_event("startup")
async def startup_event():
    try:
        await check_mongo_connection()  # No need to pass mongo_uri here
        print("MongoDB connection successful!")
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        raise HTTPException(status_code=500, detail=f"MongoDB connection failed: {e}")


@app.get("/")
def read_root():
    return {"message": "Welcome to the RAD OpenAI API"}
