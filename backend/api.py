import asyncio
from datetime import datetime, timezone
import http
import os
from logging import Logger
from langchain_core.messages import HumanMessage, AIMessageChunk
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from dotenv import load_dotenv
from misc import format_datetime
from errs import BaseError
from log import get_logger
from graph import super_graph

load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))


class LoggingMiddleware(BaseHTTPMiddleware):
    logger: Logger = get_logger("api")

    async def dispatch(self, request, call_next):
        self.logger.info("Request body: %s", await request.body())
        resp = await call_next(request)
        return resp
    

fastapi_app = FastAPI(validate_responses=False)
fastapi_app.add_middleware(LoggingMiddleware)
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

@fastapi_app.exception_handler(BaseError)
async def custom_exception_handler(request: Request, exc: BaseError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "path": request.url.path,
            "timestamp": format_datetime(datetime.now(timezone.utc)),
            "status": exc.status_code,
            "error": http.HTTPStatus(exc.status_code).phrase,
            "code": exc.code,
            "message": exc.detail,
            "params": [],
        },
    )


@fastapi_app.exception_handler(500)
async def internal_exception_handler(request: Request, exc):
    if isinstance(exc, BaseError):
        return await custom_exception_handler(request, exc)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

 


####################################################################
async def answer_generator(question: str):
    try:
        question = question.strip()

        async for messages in super_graph.astream(
            {
                "messages": [
                    ("user", question)
                ],
            },
            {"recursion_limit": 150},
            stream_mode="messages"
        ):
            
            checkpoint_ns:str = messages[1]["checkpoint_ns"]
            is_cared_checkpoints = checkpoint_ns.startswith("search:") or checkpoint_ns.startswith("note_taker:")
            if True or is_cared_checkpoints:
                for msg in messages:
                    if isinstance(msg, AIMessageChunk):
                        content = msg.content
                        if content:
                            #print(content, end="", flush=True)
                            yield f"data: {content}\n"
                #await asyncio.sleep(0)
    except Exception as e:
        yield f"data: [Error] {str(e)}\n\n"
    yield "data: [DONE]\n\n"



@fastapi_app.get("/rest/v1/question")
async def submit_question(request: Request, question: str):
    async def event_stream():
        try:
            async for data in answer_generator(question):
                if await request.is_disconnected():
                    break
                yield data
        except Exception as e:
            yield f"data: [Error] {str(e)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
