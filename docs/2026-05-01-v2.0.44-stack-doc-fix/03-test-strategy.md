# Test Strategy — Stack DOC-FIRST Gap Fix (v2.0.44)

## 검증 포인트

### 1. ceo.md 300줄 유지
```bash
wc -l domangcha/commands/ceo.md  # 반드시 300
```

### 2. ceo-ralph.md 300줄 유지
```bash
wc -l domangcha/commands/ceo-ralph.md  # 반드시 ≤ 300
```

### 3. 스택 설명 텍스트 검증
- Ralph: `DOC-FIRST` 키워드 포함 확인
- Superpowers: `docs/` + `GATE` + `deploy` 키워드 포함 확인
- gstack: `DOC-FIRST` 또는 `PHASE 0.65 포함` 명시 확인

### 4. ceo-ralph.md Phase 0 존재 확인
```bash
grep -n "Phase 0: DOC-FIRST" domangcha/commands/ceo-ralph.md
```

### 5. docs/ 파일 생성 확인
```bash
ls docs/2026-05-01-v2.0.44-stack-doc-fix/
ls docs/2026-05-01-v2.0.44-knowledge-registry/
# 각각 5개 파일 (00~04)
```

## 보안 테스트
- 해당 없음 (설정 문서 수정)

## 회귀 테스트
- Standard 스택 플로우 불변 확인 (ceo.md [1] Standard 줄 미변경)
- Ralph Circuit Breaker, WEIGHTED DECISION 섹션 미변경 확인
