from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import httpx
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "phi3"


class TravelQuery(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)


class TravelResponse(BaseModel):
    query: str
    response: str


@app.get("/health")
async def health():
    logger.info("Health check requested")
    return {"status": "running"}


@app.post("/ask", response_model=TravelResponse)
async def ask_travel_question(travel_query: TravelQuery):
    logger.info(f"Received travel query: {travel_query.query}")
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            payload = {
                "model": OLLAMA_MODEL,
                "prompt": travel_query.query,
                "stream": False
            }
            
            logger.debug(f"Sending request to Ollama: {payload}")
            response = await client.post(OLLAMA_API_URL, json=payload)
            
            if response.status_code != 200:
                logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                raise HTTPException(
                    status_code=503,
                    detail="Ollama service is unavailable or returned an error"
                )
            
            result = response.json()
            answer = result.get("response", "No response from model")
            
            logger.info("Successfully received response from Ollama")
            return TravelResponse(query=travel_query.query, response=answer)
            
    except httpx.ConnectError:
        logger.error("Failed to connect to Ollama service")
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to Ollama service. Make sure Ollama is running on localhost:11434"
        )
    except httpx.TimeoutException:
        logger.error("Ollama request timed out")
        raise HTTPException(
            status_code=504,
            detail="Request to Ollama timed out"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
