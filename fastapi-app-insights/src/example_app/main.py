from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from opentelemetry.exporter.richconsole import RichConsoleExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.jinja2 import Jinja2Instrumentor
from opentelemetry.instrumentation.tortoiseorm import TortoiseORMInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import get_current_span
from starlette.exceptions import HTTPException as StarletteHTTPException
from tortoise.contrib.fastapi import register_tortoise

from example_app.models import Settings

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
settings = Settings(_env_file=".env")
templates = Jinja2Templates(directory="templates")
tracer = TracerProvider(resource=Resource({SERVICE_NAME: "FastAPI"}))


import example_app.routes  # NOQA


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    span_context = get_current_span().get_span_context()
    return JSONResponse(
        {
            "message": str(exc.detail),
            "trace_id": span_context.trace_id,
            "span_id": span_context.span_id,
        },
        status_code=exc.status_code,
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    span = get_current_span()
    assert span.is_recording
    span_context = span.get_span_context()
    return JSONResponse(
        {
            "message": "Server Error",
            "trace_id": span_context.trace_id,
            "span_id": span_context.span_id,
        },
        status_code=500,
    )


@app.on_event("startup")
def startup_event():
    if settings.verbose_tracing:
        tracer.add_span_processor(BatchSpanProcessor(RichConsoleExporter()))

    from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

    exporter = AzureMonitorTraceExporter.from_connection_string(
        settings.app_insights_connection_string
    )
    tracer.add_span_processor(BatchSpanProcessor(exporter))

    FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer)
    TortoiseORMInstrumentor().instrument(tracer_provider=tracer)
    Jinja2Instrumentor().instrument(tracer_provider=tracer)
    register_tortoise(
        app,
        db_url=settings.db_url,
        modules={"models": ["example_app.db_models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
