# DOMANGCHA v4.1.1

이 프로젝트는 DOMANGCHA 프로젝트 자율개발 루프로 운영되고 이 규정이 전역 규정보다 우선함
전체 규정은 LOOP.md 이고 상시 로드하지 않음, 아래 핵심만 따르고 표시된 시점에 해당 절만 읽음

- 재개 근거는 .loop/PLAN.md 하나, 세션 시작 훅이 loop resume 을 출력함 (안 보이면 node scripts/loop.mjs resume)
- 매 프롬프트 훅이 지시 또는 개입으로 기록하고 다음 행동과 활성 정책(.loop/POLICY.md)을 출력하므로 그대로 따름
- 질문 조회 설명과 오타 한 줄은 플랜 없이 바로 처리, 저장소를 바꾸는 지시는 코드 전에 플랜부터 (LOOP.md 1절)
- 항목마다 loop start Ixx → 범위 안 구현 → 자가감사 a~h → loop pass 또는 fail, 통과 전 다음 항목 금지 (LOOP.md 2절)
- 플랜을 바꿔야 하면 PLAN.md 수정 후 loop plan revise (LOOP.md 2절 5)
- 전 항목 통과 후 종합 감사 (LOOP.md 4절), 중량 항목은 LOOP.md 5절, 정책 승격은 6절
- 사용자 화면이나 기능을 바꾼 항목은 LOOP.md 8절 화면 감사와 9절 완결성 검증을 읽고 수행
- 진행 보고: 루프 카드로 시작, 단계와 항목 ID 를 말함, 30초 넘는 단계는 시작 중간 끝을 알림, 승인 앞에서는 멈춤, 실패는 숨기지 않음
- 중량 규정(DOMANGCHA 하네스)은 .claude/heavy/CEO.md, /ceo 는 요청 전체를 하네스로 올림
