"""Send GET/POST requests to the KCDB server.

We could use a third-party package like "requests" or "httpx" but since the
KCDB API is so basic (e.g., no authentication is required, trivial GET parameters),
the builtin urllib module is sufficient.
"""

from __future__ import annotations

import json as _json
from http.client import HTTPException
from typing import TYPE_CHECKING
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from ._version import __version__

if TYPE_CHECKING:
    from http.client import HTTPResponse
    from typing import Any

HEADERS: dict[str, str] = {
    "User-Agent": f"msl-kcdb/{__version__}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}


class _Response:
    def __init__(self, response: HTTPResponse | HTTPError) -> None:
        self._url = response.url
        self._code = 0 if response.status is None else response.status
        self._reason = response.reason
        self._data = response.read()

    @property
    def ok(self) -> bool:
        return self._code == 200  # noqa: PLR2004

    def raise_for_status(self) -> None:
        """Raise an exception, if one occurred."""
        typ: str = ""
        if 400 <= self._code < 500:  # noqa: PLR2004
            typ = "Client"
        elif 500 <= self._code < 600:  # noqa: PLR2004
            typ = "Server"

        if typ:
            msg = f"{typ} Error {self._code}: reason={self._reason!r}, url={self._url!r}"
            raise HTTPException(msg)

    def json(self) -> Any:  # noqa: ANN401
        return _json.loads(self._data)


def get(
    url: str,
    *,
    json: dict[str, bool | int | str | list[str]] | None = None,
    params: dict[str, int | str] | None = None,
    timeout: float | None = 30,
) -> _Response:
    """Send a GET request.

    Args:
        url: A HTTPS url.
        json: A JSON-serializable object.
        params: Query parameters to include in the url.
        timeout: The timeout, in seconds.

    Returns:
        The response.
    """
    return _request(url=url, method="GET", json=json, params=params, timeout=timeout)


def post(
    url: str,
    *,
    json: dict[str, bool | int | str | list[str]] | None = None,
    params: dict[str, int | str] | None = None,
    timeout: float | None = 30,
) -> _Response:
    """Send a POST request.

    Args:
        url: A HTTPS url.
        json: A JSON-serializable object.
        params: Query parameters to include in the url.
        timeout: The timeout, in seconds.

    Returns:
        The response.
    """
    return _request(url=url, method="POST", json=json, params=params, timeout=timeout)


def _request(
    *,
    url: str,
    method: str,
    json: dict[str, bool | int | str | list[str]] | None = None,
    params: dict[str, int | str] | None = None,
    timeout: float | None = 30,
) -> _Response:
    """Send a request."""
    if params:
        # The KCDB API values are either an integer or a domain-code string
        # (which does not contain spaces and only letters A-Z or a hyphen),
        # so there is no need to convert the key-value pairs to be URL safe,
        # using urllib.parse.quote_plus(), since they already are safe.
        url += "?" + "&".join(f"{key}={value}" for key, value in params.items())

    data = _json.dumps(json).encode("utf-8") if json else None

    try:
        with urlopen(Request(url, headers=HEADERS, data=data, method=method), timeout=timeout) as response:  # noqa: S310
            return _Response(response)
    except HTTPError as e:
        return _Response(e)
    except OSError as e:
        if "timed out" not in str(e):
            raise

    msg = f"No reply from KCDB server after {timeout} seconds"
    raise TimeoutError(msg)
