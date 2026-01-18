# src/loaders.py

from pathlib import Path
from typing import List, Dict, Any
import yaml

DEFAULT_INDUSTRY_ORDER = [
    "Bancos & Seguros",
    "Energía",
    "Entretenimiento",
    "Manufactura",
    "Marketing",
    "Política",
    "Transporte",
]

def _projects_path() -> Path:
    return Path(__file__).resolve().parent.parent / "data" / "projects.yaml"

def load_projects() -> List[Dict[str, Any]]:
    path = _projects_path()
    if not path.exists():
        return []

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("projects.yaml debe ser una lista de proyectos")

    for p in data:
        p.setdefault("tracks", [])
        p.setdefault("stack", [])
        p.setdefault("highlights", [])
        p.setdefault("metrics", {})
        p.setdefault("artifacts", {})
        p.setdefault("industry", "Otros")

    return data

def group_by_industry(projects: List[Dict[str, Any]]):
    grouped = {}
    for p in projects:
        ind = p.get("industry", "Otros")
        grouped.setdefault(ind, []).append(p)

    for ind in grouped:
        grouped[ind] = sorted(grouped[ind], key=lambda x: x.get("date", ""), reverse=True)

    return grouped

def filter_by_track(projects: List[Dict[str, Any]], track: str):
    return [p for p in projects if track in p.get("tracks", [])]

def ordered_industries(grouped: dict):
    ordered = [i for i in DEFAULT_INDUSTRY_ORDER if i in grouped]
    rest = sorted([i for i in grouped.keys() if i not in ordered])
    return ordered + rest
