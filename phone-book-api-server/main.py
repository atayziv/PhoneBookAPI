import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from phone_book_api_server.api.server import app

if __name__ == "__main__":
    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    uvicorn.run(app, host="0.0.0.0", port=8000)