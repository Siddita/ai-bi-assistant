from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models import Product
import pandas as pd
import logging
from utils import generate_sql_query, generate_visualization, generate_forecast

# Create router without prefix
router = APIRouter()
logger = logging.getLogger(__name__)

class QueryRequest(BaseModel):
    question: str

@router.get("/")
async def root():
    return {"message": "AI Business Intelligence Assistant API is running"}

@router.get("/test-db")
async def test_db(db: Session = Depends(get_db)):
    try:
        # Try to query the database
        count = db.query(Product).count()
        logger.info(f"Database connection successful. Found {count} products.")
        return {"status": "success", "message": f"Database connection successful. Found {count} products."}
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ask")
async def ask_question(payload: QueryRequest, db: Session = Depends(get_db)):
    try:
        logger.info(f"Processing question: {payload.question}")
        
        # Generate SQL query based on the question
        sql_query = generate_sql_query(payload.question)
        logger.info(f"Generated SQL query: {sql_query}")
        
        # Execute query and get results
        results = db.execute(sql_query).fetchall()
        
        # Convert results to DataFrame
        df = pd.DataFrame(results)
        
        # Generate visualization or forecast based on the question
        if "forecast" in payload.question.lower():
            return await generate_forecast(df)
        else:
            return await generate_visualization(df)
            
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        raise HTTPException(status_code=500, detail=str(e))
