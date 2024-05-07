import sys

import uvicorn

from phone_book_api_server.api.server import app


def init() -> None:
    uvicorn.run(
        "fastapi_server.api.server:app",
        host="127.0.0.1",
        port=8000,
        log_level="trace",
        reload=True,
    )


# To make sure the service will run with uvicorn only when running this service directly
# on the localhost for developing purposes
if __name__ == "__main__":
    app.extra["container"].wire(modules=[sys.modules[__name__]])
    init()
