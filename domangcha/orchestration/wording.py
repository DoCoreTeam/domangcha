"""Bilingual vocabulary for the status cards.

Every tuple is ordered by LANGS, so index 0 is Korean and index 1 is English.
This is data, not rendering: status.py stays the single renderer and reads its
words from here, which keeps one file from carrying both the layout logic and
the entire phrasebook. Add a language by extending LANGS and every tuple.
"""
from __future__ import annotations

from typing import Dict, Tuple

DEFAULT_LANG = "ko"
LANGS = ("ko", "en")

Phrase = Tuple[str, str]

LABELS: Dict[str, Phrase] = {
    "why": ("이유", "why"),
    "plan": ("계획", "plan"),
    "next": ("다음", "next"),
    "state": ("상태", "state"),
    "budget": ("예산", "budget"),
    "done": ("완료", "done"),
    "running": ("진행", "running"),
    "waiting": ("대기", "waiting"),
    "approval": ("승인 대기", "awaiting approval"),
    "attempt": ("시도", "attempt"),
    "nodes": ("노드", "nodes"),
    "none": ("없음", "none"),
    "deploy": ("배포 상태", "deployment"),
    "in_sync": ("설치본이 저장소와 일치합니다", "installed runtime matches this repository"),
    "not_installed": ("설치본 없음 — ~/.domangcha 미설치", "not installed — no ~/.domangcha runtime"),
    "stale_files": ("오래된 파일", "stale files"),
    "deploy_hint": (
        "커밋·푸시 후 install.sh를 다시 실행하면 반영됩니다",
        "commit, push, then re-run install.sh to deploy",
    ),
    "approval_note": (
        "파괴적·되돌릴 수 없는 작업은 승인을 받은 뒤에만 진행합니다",
        "destructive or irreversible work proceeds only after approval",
    ),
    "ambiguous_note": (
        "경계선 분류라 근거를 함께 보고합니다",
        "borderline classification — reporting the reasoning alongside",
    ),
}

PLAN: Dict[str, Phrase] = {
    "DIRECT": (
        "바로 처리합니다 — planner·루프·에이전트 팬아웃 없음",
        "handled directly — no planner, loop, or agent fan-out",
    ),
    "LOOP": (
        "PLAN → EXECUTE → VALIDATE → ACT 반복 (네이티브 /loop)",
        "bounded PLAN → EXECUTE → VALIDATE → ACT on native /loop",
    ),
    "GRAPH": (
        "Workflow 툴 · 병렬 브랜치 · join · 승인 게이트",
        "Workflow tool with parallel branches, joins, and approval gates",
    ),
}

NEXT: Dict[str, Phrase] = {
    "DIRECT": (
        "관련된 최소 검증만 실행하고 결과를 알려드립니다",
        "run only the relevant minimal validation, then report back",
    ),
    "LOOP": (
        "반복마다 루프 상태(회차·예산·진전)를 보고합니다",
        "report loop state (iteration, budget, progress) every pass",
    ),
    "GRAPH": (
        "노드별·브랜치별 진행 상태를 보고합니다",
        "report progress per node and per parallel branch",
    ),
}
