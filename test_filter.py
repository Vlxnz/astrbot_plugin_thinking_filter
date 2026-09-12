import sys
import types

api = types.ModuleType("astrbot.api")
star = types.ModuleType("astrbot.api.star")
event = types.ModuleType("astrbot.api.event")
components = types.ModuleType("astrbot.api.message_components")
api.star = star
api.event = event
api.message_components = components
sys.modules.update({
    "astrbot": types.ModuleType("astrbot"),
    "astrbot.api": api,
    "astrbot.api.star": star,
    "astrbot.api.event": event,
    "astrbot.api.message_components": components,
})
star.Star = type("Star", (), {})
event.AstrMessageEvent = object
event.filter = types.SimpleNamespace(
    on_llm_response=lambda **_: lambda func: func,
    on_decorating_result=lambda **_: lambda func: func,
)
components.Plain = type("Plain", (), {})

from main import strip_reasoning  # noqa: E402


def test_closed_thinking_block_keeps_answer():
    assert strip_reasoning("<thinking>hidden</thinking>answer") == "answer"


def test_closed_analysis_block_preserves_surrounding_text():
    assert strip_reasoning("before <analysis>hidden</analysis> after") == "before  after"


def test_unclosed_block_drops_remainder():
    assert strip_reasoning("answer<thinking>hidden") == "answer"


def test_case_and_attributes_are_supported():
    assert strip_reasoning('<THINKING foo="x">hidden</THINKING>ok') == "ok"


def test_end_tag_is_removed_if_left_alone():
    assert strip_reasoning("answer</analysis>") == "answer"


def test_plain_text_is_unchanged():
    text = "这是正常回答，不包含推理标签。"
    assert strip_reasoning(text) == text
