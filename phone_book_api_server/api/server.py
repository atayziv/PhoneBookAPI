import logging
import os
import time
import uuid
from typing import Awaitable, Callable

from fastapi import FastAPI, Request, Response, status
from fastapi.concurrency import iterate_in_threadpool
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from fastapi_server import SETTINGS
from fastapi_server.api.routers import examples_router, health_router, index_router
from fastapi_server.constants import get_from_env
from fastapi_server.containers import Container


def create_container() -> Container:
    container = Container()
    container.config.from_yaml(SETTINGS.CONFIG, required=True, envs_required=True)
    container.init_resources()
    container.wire(modules=[examples_router, health_router, index_router])
    return container


def create_app() -> FastAPI:
    container = create_container()

    logger = logging.getLogger(__name__)
    logger.info(f"Starting FastAPI server {SETTINGS.NAME} v{SETTINGS.VERSION}...")

    _app = FastAPI(
        title=SETTINGS.NAME,
        version=SETTINGS.VERSION,
        root_path=get_from_env("FASTAPI_SERVER_ROOT_PATH", ""),
        docs_url=None,
        redoc_url=None,
    )
    _app.extra = {"container": container}
    _app.include_router(examples_router.router)
    _app.include_router(health_router.router)
    _app.include_router(index_router.router)

    logger.info(f"FastAPI server {SETTINGS.NAME} v{SETTINGS.VERSION} is up and running!")

    return _app


app = create_app()


@app.exception_handler(Exception)
async def exception_handler(_: Request, error: Exception) -> None:
    logger = logging.getLogger(__name__)
    logger.exception(error)
    raise error


static_folder = os.path.join(SETTINGS.ROOT_DIR, "api/static")
app.mount("/static", StaticFiles(directory=static_folder), name="static")


@app.get("/docs", include_in_schema=False)
def custom_swagger_ui_html() -> HTMLResponse:
    return get_swagger_ui_html(
        openapi_url=f"{app.root_path}{app.openapi_url}",
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url=f"{app.root_path}/static/swagger-ui-bundle.js",
        swagger_css_url=f"{app.root_path}/static/swagger-ui.css",
        swagger_favicon_url=f"{app.root_path}/static/favicon.png",
    )


@app.get("/redoc", include_in_schema=False)
def redoc_html() -> HTMLResponse:
    return get_redoc_html(
        openapi_url=f"{app.root_path}{app.openapi_url}",
        title=app.title + " - ReDoc",
        redoc_js_url=f"{app.root_path}/static/redoc.standalone.js",
        redoc_favicon_url=f"{app.root_path}/static/favicon.png",
    )


@app.middleware("http")
async def add_process_time_header(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    logger = logging.getLogger(__name__)
    start_time = time.time()
    idem = str(uuid.uuid1())[:8]
    logger.info("rid=%s start request [%s] path=%s", idem, request.method.upper(), request.url.path)
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    msg = f"rid={idem} completed_in={process_time} seconds status_code={response.status_code}"
    if response.status_code < status.HTTP_400_BAD_REQUEST:
        logger.info(msg)
    else:
        resp_body = [section async for section in response.__dict__["body_iterator"]]
        response.__dict__["body_iterator"] = iterate_in_threadpool(iter(resp_body))
        logger.info(f"{msg}, {resp_body}")
    return response
