from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


def load_yaml(path: Path) -> Dict[str, Any]:
    """Load YAML safely. Returns dict (empty if file missing)."""
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        return {}
    return data


def load_projects(path: Path) -> List[Dict[str, Any]]:
    """
    Expected YAML structure:
    projects:
      - title:
        tagline:
        category:
        tags: []
        year:
        status:
        stack: []
        impact:
        links: { demo: "", github: "", report: "" }
        highlights: []
        details: ""
    """
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
                "tags": p.get("tags", []) if isinstance(p.get("tags", []), list) else [],
                "year": str(p.get("year", "")).strip(),
                "status": str(p.get("status", "In progress")).strip(),
                "stack": p.get("stack", []) if isinstance(p.get("stack", []), list) else [],
                "impact": str(p.get("impact", "")).strip(),
                "links": p.get("links", {}) if isinstance(p.get("links", {}), dict) else {},
                "highlights": p.get("highlights", []) if isinstance(p.get("highlights", []), list) else [],
                "details": str(p.get("details", "")).strip(),
                "image": str(p.get("image", "")).strip(),  # optional
            }
        )

    # remove empties
    cleaned = [p for p in cleaned if p["title"]]
    return cleaned
