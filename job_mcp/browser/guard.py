"""Decides whether a click would send an application. Those clicks are always left to the person applying.

Opening an application ("Apply", "Easy Apply") and moving between steps ("Next", "Review") are
allowed; the final send ("Submit application", a submit button on a filled form) is not.
"""

import re
from dataclasses import dataclass

_FINAL_SEND = re.compile(
    r"\b(submit|send (my |your )?application|finish (and )?(apply|application)|complete (my |your )?application"
    r"|confirm (and )?(apply|submit)|apply and submit|i'?m done|place order|pay now)\b",
    re.I,
)
# "Apply" is deliberately absent: on a filled form, a submit button labeled "Apply" is the final send.
_STEP_OK = re.compile(r"^(next|continue|review|save( and continue| & continue)?|back|previous|search|find jobs"
                      r"|sign in|log ?in|upload|add( another)?|show more|see more|load more)$", re.I)
# A submit-type button on a form this size is an application, not a search or login box.
_FORM_FIELD_THRESHOLD = 3


@dataclass(frozen=True)
class Verdict:
    allowed: bool
    reason: str


def classify_click(element: dict) -> Verdict:
    """element: the snapshot entry plus `form_fields`, the count of fillable fields in its form."""
    # A button's own text is what the person sees; the wrapper-derived label is only a fallback.
    words = str(element.get("text") or element.get("value") or element.get("label") or "").strip()
    if _FINAL_SEND.search(words):
        return Verdict(False, f"'{words[:60]}' would send the application; left for you to click")
    is_submit = element.get("type") == "submit" or (element.get("tag") == "button" and element.get("type") in ("", None)
                                                    and element.get("in_form"))
    if is_submit and element.get("form_fields", 0) >= _FORM_FIELD_THRESHOLD and not _STEP_OK.match(words):
        return Verdict(False, f"submit button '{words[:60] or '(unlabeled)'}' on a {element['form_fields']}-field form; "
                              "left for you to click")
    return Verdict(True, "ok")


_ENTER_OK_ROLES = {"combobox", "listbox", "option", "searchbox"}


def classify_key(key: str, focused: dict) -> Verdict:
    """Enter inside a form can submit it, so it is only allowed on dropdown-style widgets."""
    if key not in ("Enter", "Tab", "Shift+Tab", "ArrowDown", "ArrowUp", "Escape", "Space"):
        return Verdict(False, f"key '{key}' is not on the allowed list")
    if key == "Enter" and focused.get("in_form") and focused.get("role") not in _ENTER_OK_ROLES \
            and focused.get("aria_autocomplete") in (None, "", "none"):
        return Verdict(False, "Enter in a form field can submit the application; use a click on a non-submit control")
    return Verdict(True, "ok")
