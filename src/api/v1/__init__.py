from fastapi import APIRouter


api_router = APIRouter(prefix="/v1")

# Такой формат является не PEP-friendly, 
# но мне он кажется достаточно удобным
from .courses import *
