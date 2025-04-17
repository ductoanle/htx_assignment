from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from htx_transcriber.api.router import router as api_router


def get_application() -> FastAPI:
    application = FastAPI(title="HTX Transcriber")
    application.include_router(api_router)
    return application


app = get_application()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
