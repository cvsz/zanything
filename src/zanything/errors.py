"""RFC 7807 Problem Details error contract and enterprise exception handlers."""

import time
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from starlette.exceptions import HTTPException as StarletteHTTPException

from zanything.logging import get_logger, request_id_ctx

logger = get_logger("zanything.errors")


class ProblemDetails(BaseModel):
    """RFC 7807 compliant problem details model."""

    type: str = Field(
        default="about:blank", description="URI reference identifying problem type"
    )
    title: str = Field(description="Short, human-readable summary of the problem")
    status: int = Field(description="HTTP status code")
    detail: str = Field(
        description="Human-readable explanation specific to this occurrence"
    )
    instance: str | None = Field(
        default=None, description="URI identifying the specific occurrence"
    )
    request_id: str = Field(default_factory=lambda: request_id_ctx.get())
    timestamp: str = Field(
        default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    )
    invalid_params: list[dict[str, Any]] | None = Field(
        default=None, description="Validation error details if applicable"
    )


class AppException(Exception):
    """Base application exception."""

    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        title: str = "Internal Server Error",
        detail: str = "An unexpected error occurred while processing the request.",
        error_type: str = "about:blank",
        invalid_params: list[dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(detail)
        self.status_code = status_code
        self.title = title
        self.detail = detail
        self.error_type = error_type
        self.invalid_params = invalid_params


class NotFoundException(AppException):
    def __init__(self, resource: str, identifier: str) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            title="Resource Not Found",
            detail=f"{resource} with identifier '{identifier}' was not found.",
            error_type="https://zany.zeaz.dev/errors/not-found",
        )


class ValidationException(AppException):
    def __init__(
        self, detail: str, invalid_params: list[dict[str, Any]] | None = None
    ) -> None:
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            title="Validation Error",
            detail=detail,
            error_type="https://zany.zeaz.dev/errors/validation-error",
            invalid_params=invalid_params,
        )


def register_exception_handlers(app: FastAPI) -> None:
    """Register RFC 7807 exception handlers on the FastAPI application."""

    @app.exception_handler(AppException)
    async def app_exception_handler(
        request: Request, exc: AppException
    ) -> JSONResponse:
        req_id = request_id_ctx.get()
        logger.warning(
            f"Handled application exception: [{exc.status_code}] "
            f"{exc.title}: {exc.detail}"
        )
        problem = ProblemDetails(
            type=exc.error_type,
            title=exc.title,
            status=exc.status_code,
            detail=exc.detail,
            instance=str(request.url.path),
            request_id=req_id,
            invalid_params=exc.invalid_params,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=problem.model_dump(exclude_none=True),
            media_type="application/problem+json",
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        req_id = request_id_ctx.get()
        errors = [
            {
                "name": ".".join(str(loc) for loc in err["loc"] if loc != "body"),
                "reason": err["msg"],
            }
            for err in exc.errors()
        ]
        logger.info(
            f"Request validation failed on {request.url.path}: {len(errors)} error(s)"
        )
        problem = ProblemDetails(
            type="https://zany.zeaz.dev/errors/validation-error",
            title="Validation Failed",
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="The request body or parameters failed schema validation.",
            instance=str(request.url.path),
            request_id=req_id,
            invalid_params=errors,
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=problem.model_dump(exclude_none=True),
            media_type="application/problem+json",
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        req_id = request_id_ctx.get()
        problem = ProblemDetails(
            type="about:blank",
            title="HTTP Error",
            status=exc.status_code,
            detail=str(exc.detail),
            instance=str(request.url.path),
            request_id=req_id,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=problem.model_dump(exclude_none=True),
            media_type="application/problem+json",
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        req_id = request_id_ctx.get()
        logger.error(f"Unhandled exception on {request.url.path}: {exc}", exc_info=True)
        problem = ProblemDetails(
            type="https://zany.zeaz.dev/errors/internal-server-error",
            title="Internal Server Error",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal error occurred. Please refer to request_id.",
            instance=str(request.url.path),
            request_id=req_id,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=problem.model_dump(exclude_none=True),
            media_type="application/problem+json",
        )
