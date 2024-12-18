from datetime import datetime, timezone
import http
import os
from logging import Logger
from pprint import pprint
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel

from dotenv import load_dotenv
from misc import format_datetime
from errs import BaseError
from log import get_logger
from workflow import workflow

load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))

# Compile
compiled_workflow = workflow.compile()


class LoggingMiddleware(BaseHTTPMiddleware):
    logger: Logger = get_logger("api")

    async def dispatch(self, request, call_next):
        self.logger.info("Request body: %s", await request.body())
        resp = await call_next(request)
        return resp
    

fastapi_app = FastAPI(validate_responses=False)
fastapi_app.add_middleware(LoggingMiddleware)

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
class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    question: str
    answer: str

@fastapi_app.post("/rest/v1/question", response_model=AnswerResponse)
async def submit_question(request: QuestionRequest):
    question = request.question.strip()
    inputs = {
        "question": question
    }

    for output in compiled_workflow.stream(inputs):
        for key, value in output.items():
            # Node
            pprint(f"Node '{key}':")
            # Optional: print full state at each node
            # pprint.pprint(value["keys"], indent=2, width=80, depth=None)
        pprint("\n---\n")
    
    answer = value["generation"]#"Sorry, I don't know the answer to that question."
    return {"question": question, "answer": answer}
