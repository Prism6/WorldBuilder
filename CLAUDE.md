# WorldBuilder — CLAUDE.md

SF/판타지 창작자를 위한 세계관 구축 도구. Python 3.11 + Streamlit 기반 웹 애플리케이션.

---

## 명령어

```bash
# 앱 실행
streamlit run app.py

# 테스트
pytest
pytest -v --cov=. --cov-report=term-missing

# 코드 품질
mypy models/ services/ repositories/ components/
flake8 .
radon cc . -a   # 복잡도
radon mi .      # 유지보수성
```

---

## 아키텍처

상세 내용은 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) 참조.

```
app.py (Presentation)
  └─ 콜백 함수 정의 및 주입
components/
  └─ UI 렌더링만 담당, 콜백으로 로직 위임
services/
  └─ 비즈니스 로직 (ProjectManager)
repositories/
  └─ 데이터 접근 추상화 (ABC 인터페이스 → JSON 구현체)
models/
  └─ 데이터 클래스 + 자체 유효성 검증
```

---

## 코딩 규칙

**필수**
- 모든 함수에 타입 힌트 적용 (mypy 0 경고 유지)
- public 메서드에 Google 스타일 docstring
- PEP8 준수 (flake8 0 경고 유지, W504 제외)
- 매직 넘버·문자열 금지 → `constants.py` 사용
- SOLID 원칙 준수

**로깅**
```python
from utils.logger import get_logger
logger = get_logger(__name__)
# 레벨: DEBUG / INFO / WARNING / ERROR
```

**예외 처리** — `exceptions.py`의 커스텀 예외 사용
```
WorldBuilderException       (기본)
ProjectNotFoundException
ProjectValidationError
ProjectSaveError / ProjectLoadError
```

---

## 커밋 컨벤션

```
feat:     새 기능
fix:      버그 수정
refactor: 리팩토링
docs:     문서 변경
test:     테스트 추가/수정
```

예: `feat: 연결 관계 필터링 기능 추가`

---

## 코드 품질 목표

| 항목 | 목표 |
|---|---|
| mypy | 0 경고 |
| flake8 | 0 경고 (W504 제외) |
| Cyclomatic Complexity | A등급 (평균 < 3) |
| 테스트 커버리지 | 80% 이상 |
