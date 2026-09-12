from __future__ import annotations

import re

from astrbot.api import star
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.message_components import Plain


_BLOCK_RE = re.compile(
    r"<(?P<tag>thinking|analysis)\b[^>]*>.*?</(?P=tag)\s*>",
    re.IGNORECASE | re.DOTALL,
)
_UNCLOSED_RE = re.compile(
    r"<(?P<tag>thinking|analysis)\b[^>]*>.*$",
    re.IGNORECASE | re.DOTALL,
)
_END_TAG_RE = re.compile(r"</(?:thinking|analysis)\s*>", re.IGNORECASE)


def strip_reasoning(text: str) -> str:
    """Remove leaked reasoning markup while preserving the final answer."""
    cleaned = _BLOCK_RE.sub("", text)
    # A provider may omit the closing tag. The remainder is internal content
    # and cannot be safely distinguished from the answer.
    cleaned = _UNCLOSED_RE.sub("", cleaned)
    return _END_TAG_RE.sub("", cleaned)


class ThinkingFilterPlugin(star.Star):
    """Remove literal model reasoning blocks immediately before sending."""

    @filter.on_llm_response(priority=100)
    async def strip_llm_response(self, event: AstrMessageEvent, response) -> None:
        if response is None:
            return
        result_chain = getattr(response, "result_chain", None)
        if result_chain is not None:
            self._sanitize_chain(result_chain.chain)
        else:
            response.completion_text = strip_reasoning(response.completion_text or "")

    @filter.on_decorating_result(priority=100)
    async def strip_before_send(self, event: AstrMessageEvent) -> None:
        result = event.get_result()
        if result is None or not getattr(result, "chain", None):
            return
        self._sanitize_chain(result.chain)

    @staticmethod
    def _sanitize_chain(chain) -> None:
        for component in chain:
            if isinstance(component, Plain):
                component.text = strip_reasoning(component.text)
