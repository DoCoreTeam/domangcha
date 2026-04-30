# FAST PATH Summary
작업: ceo-update + ceo-version의 업데이트 실행 방식을 npx primary / curl fallback으로 변경
대상: domangcha/commands/ceo-update.md, domangcha/commands/ceo-version.md
이유: npx domangcha가 공식 배포 채널(npm 레지스트리)이므로 1순위여야 함. curl|bash(raw GitHub)는 npx 실패 시 fallback
영향: ~/.claude/commands/ 동기화 필요
