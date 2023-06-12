from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from api.router import v3

tags_metadata = [
    {
        "name": "V3",
        "description": "V3 API Renewal",
    }
]

app = FastAPI(openapi_tags=tags_metadata)

app.include_router(v3.router)

origins = [
    "https://beaverhouse.github.io",
    "https://beta.loaprofile.com",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # price_save(None)
    pass

@app.get("/", include_in_schema=False)
def read_root():
    return RedirectResponse("/docs") 