# /ceo-ralph — Forced Loop Mode

기존 명령 이름을 유지하는 LOOP adapter다. `/ceo-ralph "업무"`는 canonical TaskRouter에서 최소 route를 LOOP로 설정한다.

```text
PLAN → EXECUTE → VALIDATE → ACT
                     ├─ success → COMPLETE
                     ├─ failure → bounded retry
                     └─ complexity discovered → GRAPH escalation
```

## 실행

LOOP는 네이티브 `/loop` 스킬로 돈다. 회차 간격은 ScheduleWakeup으로 스스로 정하고, 진행은 TodoWrite로 보인다.
매 회차 응답 첫 줄에 지난 회차 대비 실제로 달라진 것 한 줄을 사용자 언어로 쓴다.
같은 자리를 돌고 있으면 숨기지 말고 그렇다고 말한다. 상한 도달 시 어디까지 되었고 무엇이 남았는지 설명한다.

## 종료 조건

- explicit completion criteria
- max iterations
- retry budget
- no-progress detection
- repeated-error fingerprint
- tests/validator evidence
- 사용자 화면이 있는 기능은 `evidence check` 통과 (`policies/evidence.md`)
- independent reviewer evidence when code was meaningfully changed (설치된 code-reviewer, 없으면 general-purpose)

## 중단과 승인

- budget exhaustion 또는 반복 정체는 typed failure로 종료한다.
- destructive, irreversible, security-sensitive action 발견 시 AskUserQuestion 승인이 우선한다.
- 비대화형 runtime은 `.domangcha/checkpoints/`에 `WAITING_FOR_APPROVAL` checkpoint를 남긴다.
- 중단은 사용자 변경사항을 자동 stash하거나 삭제하지 않는다.
