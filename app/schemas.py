# Content from D:\fastapi_sentiment_analysis\app\schemas.py
from pydantic import BaseModel
from typing import Dict, Optional

class User(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class SentimentAnalysisRequest(BaseModel):
    file: str  # File content as a string (binary representation of the uploaded CSV)
    scopes: Optional[Dict[str, str]] = None  # Optional dictionary for additional properties

class SentimentAnalysisResult(BaseModel):
    sentiment_counts: Dict[str, int]
    positive_count: int
    neutral_count: int
    negative_count: int
    bar_chart_url: str
    pie_chart_url: str

class Scopes(BaseModel):
    additionalProp1: str
    additionalProp2: str
    additionalProp3: str
