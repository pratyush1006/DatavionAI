"""
Enterprise HTTP client.

Provides a reusable HTTP client for the DatavionAI platform.
"""

from __future__ import annotations

from typing import Literal, Self

import httpx

from apps.common.http.auth import (
    NoAuthentication,
)
from apps.common.http.config import (
    DEFAULT_CLIENT_CONFIGURATION,
    ClientConfiguration,
    RequestOptions,
)
from apps.common.http.exceptions import (
    HTTPConnectionError,
    HTTPRequestError,
    HTTPResponseError,
    HTTPServerError,
    HTTPTimeoutError,
)
from apps.common.http.response import (
    HTTPResponse,
)
from apps.common.http.timeout import (
    TimeoutConfiguration,
)
from apps.common.http.types import (
    Headers,
    ResponseData,
)

HTTPMethod = Literal[
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "HEAD",
    "OPTIONS",
]


class HTTPClient:
    """
    Enterprise HTTP client.

    Wraps ``httpx.Client`` and exposes a stable API for
    DatavionAI.
    """

    def __init__(
        self,
        configuration: ClientConfiguration | None = None,
    ) -> None:
        """
        Initialize the HTTP client.
        """

        self._configuration = configuration or DEFAULT_CLIENT_CONFIGURATION

        self._client = self._create_client()

    @property
    def configuration(
        self,
    ) -> ClientConfiguration:
        """
        Return the client configuration.
        """

        return self._configuration

    @property
    def client(
        self,
    ) -> httpx.Client:
        """
        Return the underlying HTTP client.
        """

        return self._client

    def __enter__(
        self,
    ) -> Self:
        """
        Enter the runtime context.
        """

        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: object | None,
    ) -> None:
        """
        Exit the runtime context.
        """

        self.close()

    def close(
        self,
    ) -> None:
        """
        Close the underlying HTTP client.
        """

        self._client.close()

    def _create_client(
        self,
    ) -> httpx.Client:
        """
        Create the underlying HTTP client.
        """

        configuration = self._configuration

        return httpx.Client(
            base_url=configuration.base_url,
            headers=configuration.default_headers,
            follow_redirects=configuration.follow_redirects,
            verify=configuration.verify_ssl,
            http2=configuration.http2,
        )

    def _build_headers(
        self,
        options: RequestOptions,
    ) -> Headers:
        """
        Build request headers.
        """

        headers: Headers = {}

        if self._configuration.default_headers:
            headers.update(
                self._configuration.default_headers,
            )

        if options.headers:
            headers.update(
                options.headers,
            )

        authentication = (
            options.authentication
            if not isinstance(
                options.authentication,
                NoAuthentication,
            )
            else self._configuration.authentication
        )

        return authentication.apply(
            headers,
        )

    def _build_timeout(
        self,
        options: RequestOptions,
    ) -> httpx.Timeout:
        """
        Build the transport timeout configuration.
        """

        timeout: TimeoutConfiguration = options.timeout or self._configuration.timeout

        return httpx.Timeout(
            timeout=timeout.timeout,
            connect=timeout.connect,
            read=timeout.read,
            write=timeout.write,
            pool=timeout.pool,
        )

    def _convert_response(
        self,
        response: httpx.Response,
    ) -> HTTPResponse:
        """
        Convert an ``httpx.Response`` into an immutable
        ``HTTPResponse``.
        """

        data = None

        content_type = response.headers.get(
            "Content-Type",
            "",
        ).lower()

        if "application/json" in content_type:
            try:
                data = response.json()
            except ValueError:
                data = None

        return HTTPResponse(
            status_code=response.status_code,
            headers=dict(response.headers),
            data=data,
            content=response.content,
            encoding=response.encoding or "utf-8",
        )

    def _handle_exception(
        self,
        exception: Exception,
    ) -> None:
        """
        Translate transport exceptions into the common
        HTTP exception hierarchy.
        """

        if isinstance(
            exception,
            httpx.ConnectError,
        ):
            raise HTTPConnectionError(
                str(exception),
            ) from exception

        if isinstance(
            exception,
            httpx.TimeoutException,
        ):
            raise HTTPTimeoutError(
                str(exception),
            ) from exception

        if isinstance(
            exception,
            httpx.HTTPStatusError,
        ):
            response = exception.response

            raise HTTPResponseError(
                status_code=response.status_code,
                message=str(exception),
            ) from exception

        if isinstance(
            exception,
            httpx.RequestError,
        ):
            raise HTTPRequestError(
                str(exception),
            ) from exception

        raise HTTPServerError(
            str(exception),
        ) from exception

    def request(
        self,
        *,
        method: HTTPMethod,
        url: str,
        options: RequestOptions | None = None,
        json: ResponseData | None = None,
        content: bytes | None = None,
    ) -> HTTPResponse:
        """
        Execute an HTTP request.
        """

        request_options = options or RequestOptions()

        headers = self._build_headers(
            request_options,
        )

        timeout = self._build_timeout(
            request_options,
        )

        try:
            response = self._client.request(
                method=method,
                url=url,
                headers=headers,
                params=request_options.query_params,
                json=json,
                content=content,
                timeout=timeout,
                follow_redirects=request_options.follow_redirects,
            )

            return self._convert_response(
                response,
            )

        except Exception as exception:
            self._handle_exception(
                exception,
            )

            raise

    def get(
        self,
        url: str,
        *,
        options: RequestOptions | None = None,
    ) -> HTTPResponse:
        """
        Execute a GET request.
        """

        return self.request(
            method="GET",
            url=url,
            options=options,
        )

    def post(
        self,
        url: str,
        *,
        json: object | None = None,
        content: bytes | None = None,
        options: RequestOptions | None = None,
    ) -> HTTPResponse:
        """
        Execute a POST request.
        """

        return self.request(
            method="POST",
            url=url,
            json=json,
            content=content,
            options=options,
        )

    def put(
        self,
        url: str,
        *,
        json: object | None = None,
        content: bytes | None = None,
        options: RequestOptions | None = None,
    ) -> HTTPResponse:
        """
        Execute a PUT request.
        """

        return self.request(
            method="PUT",
            url=url,
            json=json,
            content=content,
            options=options,
        )

    def patch(
        self,
        url: str,
        *,
        json: object | None = None,
        content: bytes | None = None,
        options: RequestOptions | None = None,
    ) -> HTTPResponse:
        """
        Execute a PATCH request.
        """

        return self.request(
            method="PATCH",
            url=url,
            json=json,
            content=content,
            options=options,
        )

    def delete(
        self,
        url: str,
        *,
        options: RequestOptions | None = None,
    ) -> HTTPResponse:
        """
        Execute a DELETE request.
        """

        return self.request(
            method="DELETE",
            url=url,
            options=options,
        )

    def head(
        self,
        url: str,
        *,
        options: RequestOptions | None = None,
    ) -> HTTPResponse:
        """
        Execute a HEAD request.
        """

        return self.request(
            method="HEAD",
            url=url,
            options=options,
        )

    def options(
        self,
        url: str,
        *,
        options: RequestOptions | None = None,
    ) -> HTTPResponse:
        """
        Execute an OPTIONS request.
        """

        return self.request(
            method="OPTIONS",
            url=url,
            options=options,
        )


__all__: tuple[str, ...] = ("HTTPClient",)
