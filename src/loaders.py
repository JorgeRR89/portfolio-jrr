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
    return x if isinstance(x, list) else []


def load_projects(path: Path) -> List[Dict[str, Any]]:
    data = load_yaml(path)
    projects = data.get("projects", [])
    if not isinstance(projects, list):
        return []

    cleaned: List[Dict[str, Any]] = []
    for p in projects:
        if not isinstance(p, dict):
            continue

        cleaned.append(
            {
                "title": str(p.get("title", "")).strip(),
                "tagline": str(p.get("tagline", "")).strip(),
                "category": str(p.get("category", "General")).strip(),
                "status": str(p.get("status", "In progress")).strip(),
                "year": str(p.get("year", "")).strip(),
                "spotlight": bool(p.get("spotlight", False)),

                "impact_type": str(p.get("impact_type", "")).strip(),
                "outcomes": _as_list(p.get("outcomes", [])),

                "tags": _as_list(p.get("tags", [])),
                "stack": _as_list(p.get("stack", [])),

                "problem": str(p.get("problem", "")).strip(),
                "approach": str(p.get("approach", "")).strip(),
                "results": str(p.get("results", "")).strip(),
                "details": str(p.get("details", "")).strip(),

                "links": p.get("links", {}) if isinstance(p.get("links", {}), dict) else {},
            }
        )

    cleaned = [p for p in cleaned if p["title"]]
    return cleaned
