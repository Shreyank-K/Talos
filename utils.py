import openai
import requests
from pydantic import BaseModel, ValidationError
import os

BACKEND_URL = "http://127.0.0.1:5000/upload"

class Response(BaseModel):
    allocations: dict  # Keys are categories, values are suggested amounts/details
    risks: list  # A list of risk descriptions
    recommendations: list  # A list of actionable recommendations
    total_after_suggestions: str

def get_analysis(uploaded_file):
    files = {"image": uploaded_file.getvalue()}
    response = requests.post(BACKEND_URL, files={"image": uploaded_file})
    return response