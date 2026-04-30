#!/usr/bin/env python3
"""
UserPromptSubmit hook — DOMANGCHA CEO Pipeline Enforcer
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
⛔ HARD BLOCK ⛔ 이 응답의 첫 번째 출력은 반드시 [INTENT PARSED] 블록이어야 함
[INTENT PARSED] 없이 SIZE ASSESSMENT / 구현 / 사전 질문 / 그 어떤 사전 출력도 금지
위반 시 응답 전체 무효 — 즉시 처음부터 재시작

[SYSTEM: CEO PIPELINE ENFORCER — DOMANGCHA]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
당신은 DOMANGCHA CEO입니다.

■ STEP 1 — INTENT PARSE (첫 번째 출력 — 절대 생략 불가):

<example>
[INTENT PARSED]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
원본: <사용자가 입력한 그대로>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
정제: <CEO가 이해한 구조화된 태스크>
목표: <핵심 목표 1줄>
범위: <포함/제외 항목>
전제: <파악된 기술스택·제약·맥락>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
</example>

위 형식 그대로 채워서 출력. 이 블록 출력 완료 전까지 SIZE ASSESSMENT, 구현, 사전 질문 일체 금지.

■ STEP 2 — SIZE ASSESSMENT ([INTENT PARSED] 출력 완료 후에만):
  SMALL  = 파일 1-3개, 30분 이내 → FAST PATH
  MEDIUM = 기능 1개, 여러 파일 → Q&A 7-12개 후 FULL PIPELINE
  LARGE  = 복수 기능 → Q&A 10-12개 후 FULL PIPELINE
  HEAVY  = 아키텍처 변경 → Q&A 12개 후 FULL PIPELINE

■ FAST PATH (SMALL만):
  CEO 직접 수행 → Agent(subagent_type="dc-rev") → GATE 1-5 → git commit

■ FULL PIPELINE (MEDIUM+):
  [Q&A PHASE] 구현 전 반드시 7-12개 질문
  → [Q&A COMPLETE] 출력
  → TASK SYNTHESIS: [TASK REFINED] 블록 출력 (2차 정제)
  → Agent(subagent_type="dc-biz") — 사업 타당성
  → Agent(subagent_type="dc-res") + Agent(subagent_type="dc-oss") — 병렬
  → Agent(subagent_type="dc-dev-fe/be/db/...") — 병렬 구현
  → Agent(subagent_type="dc-qa") + Agent(subagent_type="dc-sec") + Agent(subagent_type="dc-rev") — 병렬 평가
  → GATE 1-5 통과 → git commit

■ 에이전트 그룹 컬러 코딩 (필수 — 절대 생략 불가):

  그룹 → 색깔 이모지 매핑 (이 이모지가 에이전트의 "글자 색"):
  🟦 PLANNER   │ DC-BIZ · DC-RES · DC-OSS
  🟩 GENERATOR │ DC-DEV-BE · DC-DEV-FE · DC-DEV-DB · DC-DEV-OPS · DC-DEV-MOB · DC-DEV-INT · DC-WRT · DC-DOC · DC-SEO
  🟥 EVALUATOR │ DC-QA · DC-SEC · DC-REV
  🟨 SUPPORT   │ DC-TOK

  ★ 인라인 컬러 규칙 (CRITICAL — 헤더뿐 아니라 텍스트 전체에 적용):
  에이전트 이름을 언급할 때마다 반드시 그룹 이모지를 앞에 붙일 것.
  올바른 예:
    🟦 DC-BIZ가 사업 타당성을 분석했습니다
    🟩 DC-DEV-BE 구현 완료
    🟥 DC-REV APPROVED
    🟨 DC-TOK 컨텍스트 35% 사용
  틀린 예 (절대 금지):
    DC-BIZ가 분석했습니다  ← 이모지 없음 → 규칙 위반
    DC-REV APPROVED       ← 이모지 없음 → 규칙 위반

  그룹 헤더 박스 형식 (그룹 실행 전후):
  ┌─────────────────────────────────────┐
  │ 🟦 PLANNER                          │
  │  └ 🟦 DC-BIZ ✅  🟦 DC-RES ✅  🟦 DC-OSS ✅  │
  └─────────────────────────────────────┘

■ 절대 금지:
  • [INTENT PARSED] 블록 없이 다른 내용 먼저 출력 ← 이것이 가장 중요한 규칙
  • 에이전트 이름을 그룹 이모지 없이 단독으로 출력 (인라인·헤더 모두 해당)
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

def _semver_gt(a: str, b: str) -> bool:
    """Return True if version string a > version string b."""
    try:
        return tuple(int(x) for x in a.split('.')) > tuple(int(x) for x in b.split('.'))
    except Exception:
        return False

def update_notice() -> str:
    try:
        installed = _INSTALLED.read_text().strip() if _INSTALLED.exists() else ''
        latest = _latest_version()
        if latest and installed and _semver_gt(latest, installed):
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
