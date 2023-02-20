# Third party package imports
from fastapi import FastAPI, Request,status
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# custom module imports
from main import get_content

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Reference - https://stackoverflow.com/questions/58642528/displaying-of-fastapi-validation-errors-to-end-users
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "Error": "user_input url parameter is missing in the url eg: {base_url}/api/embed?user_input="}),
    )


@app.get("/api/embed")
async def embed_api(user_input):
    return {'answer': get_content(user_input)}
