from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import yaml


ROOT = Path(__file__).resolve().parent.parent
PROJECTS_YAML = ROOT / "data" / "projects.yaml"


REQUIRED_FIELDS = ["id", "title", "summary", "industry", "date"]
OPTIONAL_DEFAULTS = {
    "tracks": [],
    "stack": [],
    "highlights": [],
    "metrics": {},
    "artifacts": {},
    "tags": [],
    "featured": False,
    "status": "done",     # done | wip | planned
}


def load_yaml(path: Path) -> Any:
    if not path.exists():
        return []
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def validate_projects(items: Any) -> Tuple[List[Dict[str, Any]], List[str]]:
    errors: List[str] = []
    if items is None:
        return [], ["projects.yaml está vacío (None). Debe ser una lista."]
    if not isinstance(items, list):
        return [], ["projects.yaml debe ser una LISTA (guiones -), no un dict."]

    seen_ids = set()
    normalized: List[Dict[str, Any]] = []

    for i, p in enumerate(items):
        if not isinstance(p, dict):
            errors.append(f"Item #{i+1} no es dict (objeto YAML).")
            continue

        # defaults
        for k, v in OPTIONAL_DEFAULTS.items():
            p.setdefault(k, v)

        # required
        missing = [k for k in REQUIRED_FIELDS if not p.get(k)]
        if missing:
            errors.append(f"Proyecto #{i+1} le faltan campos obligatorios: {missing}")

        pid = p.get("id")
        if pid:
            if pid in seen_ids:
                errors.append(f"ID duplicado: '{pid}'")
            seen_ids.add(pid)

        normalized.append(p)

    return normalized, errors


def load_projects() -> Tuple[List[Dict[str, Any]], List[str]]:
    raw = load_yaml(PROJECTS_YAML)
    return validate_projects(raw)


def group_by_industry(projects: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for p in projects:
        industry = p.get("industry", "Otros")
        grouped.setdefault(industry, []).append(p)

    # ordenar por fecha desc (string ISO YYYY-MM-DD funciona)
    for ind in grouped:
        grouped[ind] = sorted(grouped[ind], key=lambda x: x.get("date", ""), reverse=True)

    return grouped


def filter_by_track(projects: List[Dict[str, Any]], track: str) -> List[Dict[str, Any]]:
    return [p for p in projects if track in (p.get("tracks") or [])]


def get_featured(projects: List[Dict[str, Any]], limit: int = 6) -> List[Dict[str, Any]]:
    featured = [p for p in projects if p.get("featured") is True]
    featured = sorted(featured, key=lambda x: x.get("date", ""), reverse=True)
    return featured[:limit]
