# WorldBuilder — 아키텍처 설명

---

## 레이어 구조

```
┌─────────────────────────────────────────┐
│  app.py  (Presentation / Entry Point)   │
│  - 의존성 조립 및 콜백 함수 정의        │
│  - Streamlit 페이지 라우팅              │
└───────────────────┬─────────────────────┘
                    │ 콜백 주입
┌───────────────────▼─────────────────────┐
│  components/  (UI Layer)                │
│  - UI 렌더링만 담당                     │
│  - 비즈니스 로직 없음                   │
│  - 콜백으로 상위 레이어에 위임          │
└───────────────────┬─────────────────────┘
                    │ 콜백 호출
┌───────────────────▼─────────────────────┐
│  services/  (Business Logic Layer)      │
│  - ProjectManager                       │
│  - 유효성 검사, 상태 관리               │
└───────────────────┬─────────────────────┘
                    │
┌───────────────────▼─────────────────────┐
│  repositories/  (Data Access Layer)     │
│  - ProjectRepository (ABC 인터페이스)   │
│  - JsonProjectRepository (JSON 구현체)  │
└───────────────────┬─────────────────────┘
                    │
┌───────────────────▼─────────────────────┐
│  models/  (Domain Model Layer)          │
│  - Project, Concept, WorldElements      │
│  - Rules, Element, Connection           │
│  - 데이터 클래스 + 자체 유효성 검증    │
└─────────────────────────────────────────┘
```

---

## 설계 패턴

### Repository 패턴
데이터 저장 방식을 Service 레이어로부터 격리한다. `ProjectRepository` ABC를 통해 의존하고, `JsonProjectRepository`가 구현체로 주입된다. 향후 SQLite나 클라우드 저장소로 교체 시 Service 코드 변경 없이 구현체만 교체 가능하다.

```python
# 인터페이스 (repositories/project_repository.py)
class ProjectRepository(ABC):
    @abstractmethod
    def save(self, project: Project) -> None: ...
    @abstractmethod
    def load(self, project_id: str) -> Project: ...

# 구현체 (repositories/json_project_repository.py)
class JsonProjectRepository(ProjectRepository):
    def save(self, project: Project) -> None: ...
```

### Dependency Injection
`app.py`에서 구체적인 구현체를 생성해 Service에 주입한다. Service는 추상 인터페이스에만 의존하므로 테스트 시 Mock 저장소로 쉽게 교체할 수 있다.

```python
# app.py
repository = JsonProjectRepository(storage_dir)
project_manager = ProjectManager(repository)  # 주입
```

### Callback 패턴
UI 컴포넌트는 비즈니스 로직을 알지 못한다. `app.py`에서 정의한 콜백 함수를 파라미터로 받아 실행만 한다.

```python
# components/sidebar.py — UI만 담당
def render_sidebar(
    on_save_project: Callable[[], None],
    ...
) -> None:
    if st.button("💾 저장"):
        on_save_project()  # 실제 로직은 app.py에서 주입

# app.py — 로직 정의 후 주입
def save_project() -> None:
    project_manager.save_project(project)

render_sidebar(on_save_project=save_project, ...)
```

### Factory Method
`Project.from_dict(data)`로 딕셔너리에서 도메인 객체를 생성한다. 역직렬화 로직이 모델 내부에 캡슐화되어 있다.

---

## UI 컴포넌트 구조

```
app.py
├── render_sidebar()
│   ├── render_project_management()
│   └── render_navigation()
├── render_dashboard()
│   ├── render_project_header()
│   ├── render_project_stats()
│   ├── render_element_progress()
│   ├── render_concept_overview()
│   └── render_quick_actions()
├── render_element_form()
│   ├── render_element_editor()    (일반 요소 × 11)
│   └── render_rules_editor()      (규칙 요소 특수 처리)
├── render_concept_form()
│   └── render_keyword_manager()
├── render_connections_page()
│   ├── render_connection_list()
│   ├── render_network_graph()     (Plotly 인터랙티브 그래프)
│   └── render_connection_form()
└── render_export_page()
```

**컴포넌트 설계 원칙**
- 각 컴포넌트는 하나의 UI 섹션만 담당 (SRP)
- 작은 함수들을 조합해 큰 컴포넌트 구성
- 콜백을 파라미터로 받아 독립적으로 테스트 가능

---

## Streamlit 상태 관리

Streamlit은 매 상호작용마다 전체 스크립트를 재실행한다. `st.session_state`로 상태를 유지한다.

| 키 | 타입 | 설명 |
|---|---|---|
| `current_project` | `Project` | 현재 편집 중인 프로젝트 |
| `project_saved` | `bool` | 미저장 변경 여부 |
| `current_page` | `str` | 현재 페이지 (`dashboard`, `elements`, `connections`, `export`, `concept`) |

---

## 데이터 흐름

```
사용자 입력
  → Streamlit 위젯
  → 콜백 함수 (app.py)
  → ProjectManager (services/)
  → Project.update_*() (models/)
  → JsonProjectRepository.save() (repositories/)
  → JSON 파일 (data/projects/)
```

---

## 주요 설계 결정

| 결정 | 이유 |
|---|---|
| JSON 저장 (SQLite 미사용) | 1인 개발 MVP, 파일 단위로 백업/이동 용이 |
| Streamlit (PyQt 미사용) | 빠른 개발, 웹 접근성, 배포 용이 |
| ABC 인터페이스 유지 | 향후 DB 전환 시 Service 코드 변경 없이 구현체 교체 |
| Callback 패턴 | Streamlit 재실행 모델에서 컴포넌트 재사용성 확보 |
| `dataclasses` 사용 | 보일러플레이트 최소화, `asdict()`로 OCP 준수 |
