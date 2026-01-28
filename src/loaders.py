from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import yaml


def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data if isinstance(data, dict) else {}


def _as_list(x: Any) -> List[str]:
    if isinstance(x, list):
        return [str(v).strip() for v in x if str(v).strip()]
    if x is None:
        return []
    s = str(x).strip()
    return [s] if s else []


def _as_dict(x: Any) -> Dict[str, Any]:
    return x if isinstance(x, dict) else {}


def load_projects(path: Path) -> List[Dict[str, Any]]:
    """
    Reads data/projects.yaml.
    Expected structure:
      projects:
        - id: "taxi_demand"
          title: ...
          lab:
            demo_asset: "data/lab/taxi_demo.csv"
    Returns a LIST of project dicts ready for UI.
    """
    data = load_yaml(path)
    projects = data.get("projects", [])
    if not isinstance(projects, list):
        return []

    cleaned: List[Dict[str, Any]] = []
    for p in projects:
        if not isinstance(p, dict):
            continue

        # Backward-compatible aliases (in case older YAML used different keys)
        tags = _as_list(p.get("tags"))
        stack = _as_list(p.get("stack"))
        skills = _as_list(p.get("skills")) or tags
        tools = _as_list(p.get("tools")) or stack

        # category fallback to industry (older schema)
        category = str(p.get("category", "")).strip()
        industry = str(p.get("industry", "")).strip() or category

        # type can exist; otherwise leave empty
        ptype = str(p.get("type", "")).strip()

        links = _as_dict(p.get("links"))
        lab = _as_dict(p.get("lab"))

        cleaned.append(
    {
        # Critical identifiers
        "id": str(p.get("id", "")).strip(),
        "title": str(p.get("title", "")).strip(),
        "tagline": str(p.get("tagline", "")).strip(),
        "spotlight": bool(p.get("spotlight", False)),

        # Metadata
        "industry": industry,
        "type": ptype,
        "impact_type": str(p.get("impact_type", "")).strip(),
        "status": str(p.get("status", "In progress")).strip(),
        "year": str(p.get("year", "")).strip(),

        # ✅ Cover image (path relative to repo, e.g. "assets/covers/taxi.png")
        "cover": str(p.get("cover", "")).strip(),

        # Skills / tools / outcomes
        "skills": skills,
        "tools": tools,
        "outcomes": _as_list(p.get("outcomes")),

        # Long-form recruiter view
        "problem": str(p.get("problem", "")).strip(),
        "approach": str(p.get("approach", "")).strip(),
        "results": str(p.get("results", "")).strip(),
        "details": str(p.get("details", "")).strip(),

        # Links + Lab config
        "links": links,
        "lab": lab,
    }
)

    # Keep only valid entries (title is required; id is strongly recommended)
    cleaned = [p for p in cleaned if p.get("title")]
    return cleaned
