from pydantic import BaseModel


class Part(BaseModel):
    text: str


class Content(BaseModel):
    parts: list[Part]
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
    candidates: list[Candidate]
    usageMetadata: UsageMetadata
    modelVersion: str
