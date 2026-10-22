"""Spec boundaries. Always proceeds, Ask First stops, Never refuses."""

from __future__ import annotations

import re

LEVELS = ("always", "ask_first", "never")

# Content words shorter than this never count as a lone match (avoids "e" / "a").
_MIN_TOKEN = 2

_STOP = frozenset(
    {
        "a",
        "an",
        "the",
        "to",
        "of",
        "and",
        "or",
        "in",
        "on",
        "for",
        "with",
        "at",
        "by",
        "from",
        "into",
        "as",
        "is",
        "be",
        "it",
        "its",
        "this",
        "that",
        "these",
        "those",
    }
)

# Synonym families: any member stands for the whole set when matching.
# Keep Always/Ask First coherent: the same expansion applies at every level.
_FAMILIES: tuple[frozenset[str], ...] = (
    frozenset(
        {
            "secret",
            "secrets",
            "credential",
            "credentials",
            "password",
            "passwords",
            "token",
            "tokens",
            "apikey",
            "api-key",
            "api_key",
        }
    ),
    frozenset(
        {
            "commit",
            "commits",
            "committed",
            "committing",
            "push",
            "pushes",
            "pushed",
            "pushing",
            "checkin",
            "check-in",
            "checking-in",
        }
    ),
    frozenset({"git", "github", "gitlab", "repo", "repository", "vcs", "remote"}),
    frozenset(
        {
            "dependency",
            "dependencies",
            "package",
            "packages",
            "library",
            "libraries",
            "module",
            "modules",
            "crate",
            "crates",
            "pip",
            "npm",
            "wheel",
        }
    ),
    frozenset(
        {
            "new",
            "add",
            "adding",
            "added",
            "install",
            "installing",
            "installed",
            "introduce",
            "introducing",
            "fetch",
            "fetching",
            "download",
            "downloading",
            "downloaded",
        }
    ),
    frozenset({"schema", "schemas", "contract", "contracts", "openapi", "proto", "protobuf"}),
    frozenset({"change", "changing", "changed", "modify", "modifying", "modified", "alter", "altering", "edit", "editing", "edited", "update", "updating", "updated"}),
    frozenset({"public", "published", "api", "cli", "command", "commands"}),
    frozenset({"delete", "deleting", "deleted", "remove", "removing", "removed", "wipe", "wiping", "erase", "erasing"}),
    frozenset({"store", "history", "mazu-data", "backlog"}),
)

_CANON: dict[str, str] = {}
for _family in _FAMILIES:
    _rep = sorted(_family, key=len)[0]
    for _word in _family:
        _CANON[_word] = _rep

_TOKEN_RE = re.compile(r"[a-z0-9]+(?:[-_][a-z0-9]+)*", re.IGNORECASE)


def normalize(boundaries: dict | None) -> dict[str, list[str]]:
    source = boundaries or {}
    out = {}
    for level in LEVELS:
        values = source.get(level) or []
        if isinstance(values, str):
            values = [values]
        out[level] = [str(item).strip() for item in values if str(item).strip()]
    return out


def boundary_issues(boundaries: dict | None) -> list[str]:
    data = normalize(boundaries)
    if not any(data.values()):
        return ["BOUND-5 boundaries are missing"]
    return []


def _tokens(text: str) -> list[str]:
    return [m.group(0).lower() for m in _TOKEN_RE.finditer(text or "")]


def _concepts(text: str) -> set[str]:
    """Content concepts: stopwords dropped, synonyms collapsed to a family id."""
    out: set[str] = set()
    for tok in _tokens(text):
        if tok in _STOP or len(tok) < _MIN_TOKEN:
            continue
        out.add(_CANON.get(tok, tok))
    return out


def _matches(rule: str, action: str) -> bool:
    """True when the rule applies to the action.

    1. One-way substring: the rule text appears in the action (legacy).
       Reverse match ("e" inside "commit secrets") is refused.
    2. Concept cover: every content concept in the rule is present in the
       action after synonym collapse. So Never "commit secrets" hits
       "push credentials to git".
    """
    rule_l = (rule or "").strip().lower()
    text = (action or "").strip().lower()
    if not rule_l or not text:
        return False
    if rule_l in text:
        return True
    need = _concepts(rule_l)
    if not need:
        return False
    have = _concepts(text)
    return need <= have


def decide(action: str, boundaries: dict | None) -> str:
    """Return always, ask_first, never, or unspecified.

    A Never hit wins over Ask First. Ask First wins over Always.
    Matching is substring or synonym-aware concept cover (same at every level).
    """
    text = (action or "").strip()
    data = normalize(boundaries)
    if not text:
        return "unspecified"
    for level in ("never", "ask_first", "always"):
        for rule in data[level]:
            if _matches(rule, text):
                return level
    return "unspecified"


def guard(action: str, boundaries: dict | None) -> str | None:
    """None means proceed. A string is the stop or refuse reason."""
    level = decide(action, boundaries)
    if level == "never":
        return "BOUND-3 refuse: " + action
    if level == "ask_first":
        return "BOUND-2 stop and ask: " + action
    return None


def merge(base: dict | None, extra: dict | None) -> dict[str, list[str]]:
    """Story rules add to the spec. They never delete a Never."""
    left = normalize(base)
    right = normalize(extra)
    return {level: left[level] + [item for item in right[level] if item not in left[level]] for level in LEVELS}
