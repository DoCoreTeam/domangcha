#!/usr/bin/env python3
"""
UserPromptSubmit hook — MACC CEO Pipeline Enforcer
1. Injects CEO pipeline reminder for task requests
2. Loads domain-specific manual context based on keywords
3. Checks for DOMANGCHA updates (cached, max 1x/hour — no npm calls on cache hit)
"""
import json, sys, os, re, time, subprocess
from pathlib import Path

P = os.environ.get('CLAUDE_PROJECT_DIR', os.getcwd())
U = Path.home() / '.claude' / 'manuals'
R = Path(P) / '.claude' / 'manuals'

KW = {
    'frontend': ['component','page','layout','css','ui','react','next','vue','tailwind','컴포넌트','페이지','프론트'],
    'backend': ['api','endpoint','route','controller','server','auth','jwt','서버','인증','백엔드'],
    'database': ['migration','schema','query','db','sql','prisma','supabase','마이그레이션','스키마','데이터베이스'],
    'infra': ['docker','deploy','ci','cd','kubernetes','vercel','aws','배포','도커','인프라']
}

CEO_REMINDER = """
[SYSTEM: CEO PIPELINE ENFORCER]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
당신은 MACC CEO입니다. 이 요청을 처리하기 전에 반드시:

▶ STEP 0: INTENT PARSE (항상 먼저 — 생략 불가)
  모든 입력을 구조화된 태스크로 변환 후 [INTENT PARSED] 블록 출력
  → 원본 / 정제 / 목표 / 범위 / 전제

▶ SIZE ASSESSMENT (INTENT PARSE 완료 후)
  SMALL  = 파일 1-3개, 30분 이내 → FAST PATH
  MEDIUM = 기능 1개, 여러 파일 → Q&A 7-12개 후 FULL PIPELINE
  LARGE  = 복수 기능 → Q&A 10-12개 후 FULL PIPELINE
  HEAVY  = 아키텍처 변경 → Q&A 12개 후 FULL PIPELINE

▶ FAST PATH (SMALL만)
  CEO 직접 수행 → Agent(subagent_type="dc-rev") → GATE 1-5 → git commit

▶ FULL PIPELINE (MEDIUM+)
  [Q&A PHASE] 구현 전 반드시 7-12개 질문
  → [Q&A COMPLETE] 출력
  → TASK SYNTHESIS: [TASK REFINED] 블록 출력 (2차 정제)
  → Agent(subagent_type="dc-biz") — 사업 타당성
  → Agent(subagent_type="dc-res") + Agent(subagent_type="dc-oss") — 병렬
  → Agent(subagent_type="dc-dev-fe/be/db/...") — 병렬 구현
  → Agent(subagent_type="dc-qa") + Agent(subagent_type="dc-sec") + Agent(subagent_type="dc-rev") — 병렬 평가
  → GATE 1-5 통과
  → git commit

▶ 절대 금지
  • INTENT PARSE 없이 SIZE ASSESSMENT 진행
  • DC-* 에이전트 텍스트 시뮬레이션 (반드시 Agent() 도구 사용)
  • Q&A 없이 MEDIUM+ 구현 시작
  • TASK SYNTHESIS 없이 PHASE 1 진입
  • GATE 통과 전 사용자 보고
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

def load(d):
    for b in [R, U]:
        f = b / d / 'index.md'
        if f.exists():
            return f.read_text()[:1500]
    return None

# ── Cached version check (TTL 1 hour) ────────────────────────────────────────
_CACHE = Path.home() / '.claude' / '.domangcha-version-cache'
_INSTALLED = Path.home() / '.claude' / 'domangcha-installed-version'
_TTL = 3600  # seconds

def _latest_version() -> str:
    if _CACHE.exists():
        try:
            ver, ts = _CACHE.read_text().strip().rsplit(':', 1)
            if time.time() - float(ts) < _TTL:
                return ver
        except Exception:
            pass
    try:
        r = subprocess.run(['npm', 'view', 'domangcha', 'version'],
                           capture_output=True, text=True, timeout=5)
        v = r.stdout.strip()
        if v:
            _CACHE.write_text(f'{v}:{time.time():.0f}')
            return v
    except Exception:
        pass
    return ''

def update_notice() -> str:
    try:
        installed = _INSTALLED.read_text().strip() if _INSTALLED.exists() else ''
        latest = _latest_version()
        if latest and installed and latest != installed:
            return (f'\n[⚠️ UPDATE] DOMANGCHA v{latest} available '
                    f'(installed: v{installed}). '
                    f'CEO: ask user "Update before continuing? (y/n)" — '
                    f'y → run `npx domangcha` then proceed | n → proceed as-is.')
    except Exception:
        pass
    return ''
# ─────────────────────────────────────────────────────────────────────────────

def is_task_request(prompt):
    """Detect if this is a CEO task request requiring pipeline enforcement."""
    p_lower = prompt.lower()
    # Strong signals: explicit CEO commands
    if re.search(r'/ceo(-ralph|-init|-status|-review|-plan|-feature|-ship|-version|-debug|-learn|-doc|-design|-security|-test|-quality|-update)?', p_lower):
        return True
    # Korean task imperatives — broad coverage
    korean_task = [
        r'구현해', r'만들어', r'수정해', r'고쳐줘', r'추가해', r'삭제해',
        r'변경해', r'해줘', r'해봐', r'진행해', r'시작해', r'완성해',
        r'작성해', r'설계해', r'개발해', r'배포해', r'테스트해', r'빌드해',
        r'리팩터', r'마이그레이션', r'최적화해', r'분석해', r'검토해',
        r'리뷰해', r'확인해줘', r'검증해', r'업데이트해', r'셋업해',
        r'세팅해', r'연결해', r'통합해', r'생성해', r'등록해', r'적용해',
    ]
    if any(re.search(p, p_lower) for p in korean_task):
        return True
    # English task imperatives
    if prompt.endswith('?') or p_lower.startswith(('what', 'why', 'how', 'can', 'does', 'is ', 'are ', 'explain')):
        return False
    explicit_task = [
        r'\bimplement\b', r'\brefactor\b', r'\bdeploy\b', r'\bmigrate\b',
        r'\bbuild\b', r'\bcreate\b', r'\badd\b', r'\bfix\b', r'\bupdate\b',
        r'\bsetup\b', r'\bintegrate\b', r'\boptimize\b', r'\btest\b',
    ]
    return any(re.search(p, p_lower) for p in explicit_task)

try:
    data = json.load(sys.stdin)
    prompt = data.get('prompt', '')
    if not prompt:
        sys.exit(0)

    p_lower = prompt.lower()
    parts = []

    if is_task_request(prompt):
        parts.append(CEO_REMINDER + update_notice())

    found = set()
    for domain, kws in KW.items():
        if any(k in p_lower for k in kws):
            found.add(domain)

    for d in found:
        m = load(d)
        if m:
            parts.append(f"[📖 {d.upper()}]\n{m}")

    c = load('common')
    if c:
        parts.append(f"[📋 공통]\n{c}")

    if parts:
        print('\n---\n'.join(parts))

except Exception:
    pass

sys.exit(0)
