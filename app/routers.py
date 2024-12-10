from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services import query_ibm_assistant

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/assistant/query")
async def assistant_query(request: QueryRequest):
    try:
        response = query_ibm_assistant(request.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
