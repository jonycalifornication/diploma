from pydantic import BaseModel
from typing import List

class Part(BaseModel):
    text: str


class Content(BaseModel):
    parts: List[Part]
    role: str


class Candidate(BaseModel):
    content: Content
    finishReason: str
    avgLogprobs: float


class UsageMetadata(BaseModel):
    promptTokenCount: int
    candidatesTokenCount: int
    totalTokenCount: int


class GeminiResponse(BaseModel):
    candidates: List[Candidate]
    usageMetadata: UsageMetadata
    modelVersion: str