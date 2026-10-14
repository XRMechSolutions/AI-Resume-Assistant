"""Test data factories: valid defaults, tests override only what they check."""

import asyncio
import json

import httpx

from job_mcp.models import Job
from job_mcp.pacing import Pacer
from job_mcp.providers.base import Http


def make_job(**overrides) -> Job:
    base = dict(source="test", title="Senior Unity Developer", company="Acme XR",
                url="https://jobs.example.com/acme/123")
    base.update(overrides)
    return Job(**base)


def make_element(**overrides) -> dict:
    base = dict(tag="button", type="", role="", text="Next", label="", in_form=True, form_fields=8,
                aria_autocomplete="")
    base.update(overrides)
    return base


async def _no_sleep(_seconds: float) -> None:
    return None


def make_http(routes: dict[str, object]) -> Http:
    """routes: URL prefix -> JSON-able body, str body, or int status code."""

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        for prefix, body in routes.items():
            if url.startswith(prefix):
                if isinstance(body, int):
                    return httpx.Response(body)
                if isinstance(body, str):
                    return httpx.Response(200, text=body)
                return httpx.Response(200, text=json.dumps(body), headers={"content-type": "application/json"})
        return httpx.Response(404)

    return Http("test-agent", Pacer(0, sleep=_no_sleep), transport=httpx.MockTransport(handler))


def run(coro):
    return asyncio.run(asyncio.wait_for(coro, timeout=5))
