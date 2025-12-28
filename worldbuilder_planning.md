# WorldBuilder - 세계 구축 도우미 앱 기획 문서

## 1. 프로젝트 개요

### 1.1 프로젝트명
**WorldBuilder** (가칭: 월드빌더)

### 1.2 목적
SF/판타지 장르의 창작자들이 체계적이고 빠르게 세계관을 구축할 수 있도록 돕는 Python 기반 데스크톱 애플리케이션

### 1.3 배경
- 서강대 메타버스전문대학원 월드빌딩워크숍의 "12가지 세계 구축 요소" 프레임워크 기반
- 기존에는 수작업으로 각 요소를 정리해야 했음
- 요소 간 연결성과 일관성 검토가 어려웠음

### 1.4 타겟 사용자
- 소설/웹소설 작가
- 게임 기획자
- TRPG 마스터
- 메타버스/가상세계 기획자

---

## 2. 핵심 기능

### 2.1 세계 구축 12요소 입력 시스템

| 요소 | 설명 | 입력 유형 |
|------|------|-----------|
| 세계의 컨셉 | 세계의 핵심 특징 한 줄 요약 | 텍스트 (로그라인) |
| 1. 공간 | 공간적 배경, 랜드마크, 지리 | 텍스트 + 이미지 첨부 |
| 2. 시간 | 시간적 배경, 역사, 연대기 | 텍스트 + 타임라인 |
| 3. 크리쳐(캐릭터) | 생명체, 종족, 계보 | 텍스트 + 관계도 |
| 4. 자연 | 환경, 광물, 생태계 | 텍스트 + 태그 |
| 5. 문화 | 종교, 건축, 의상, 기술 수준 | 텍스트 + 카테고리 |
| 6. 언어 | 의사소통, 문자 체계 | 텍스트 + 샘플 |
| 7. 신화 | 기원, 예언, 전설 | 텍스트 |
| 8. 철학(세계관) | 믿음체계, 이데올로기 | 텍스트 |
| 9.1 규칙 | 자연/사회/종교적 규칙 | 텍스트 + 규칙 목록 |
| 9.2 경제 | 식량, 생존 방식 | 텍스트 + 선택지 |
| 9.3 정치 | 통치 구조, 군사 조직 | 텍스트 + 조직도 |
| 9.4 에너지 | 핵심 에너지원 | 텍스트 |

### 2.2 가이드 질문 시스템
각 요소별로 창작을 돕는 질문을 순차적으로 제시:
- "이 세계는 어떻게 생겼나요?"
- "이야기는 언제 시작하나요?"
- "어떤 생명체들이 살고 있나요?"
- (등등)

### 2.3 연결성 시각화
- 요소 간 관계를 그래프로 표시
- 빈 요소/미완성 요소 하이라이트
- 일관성 체크 알림

### 2.4 템플릿 & 예시
- 아바타, 반지의 제왕, 스타워즈 등 유명 작품 예시 제공
- 장르별 템플릿 (하이 판타지, 사이버펑크, 포스트아포칼립스 등)

### 2.5 내보내기
- Markdown 문서 출력
- PDF 설정집 생성
- JSON 데이터 저장/불러오기

---

## 3. 기술 스택

### 3.1 언어 & 프레임워크
```
- Python 3.10+
- GUI: PyQt6 또는 CustomTkinter (데스크톱)
       또는 Streamlit (웹 기반, MVP 추천)
- 데이터 저장: SQLite + JSON
```

### 3.2 라이브러리
```
필수:
- pandas: 데이터 처리
- json: 저장/불러오기
- markdown: 문서 변환
- reportlab 또는 fpdf2: PDF 생성

선택:
- networkx + matplotlib: 관계도 시각화
- openai 또는 anthropic: AI 어시스턴트 (확장 기능)
```

### 3.3 MVP 추천 스택
```
Streamlit + SQLite + JSON
- 빠른 개발 (1인 개발에 적합)
- 웹 브라우저로 접근
- 배포 용이 (Streamlit Cloud 무료)
```

---

## 4. 데이터 구조

### 4.1 프로젝트 스키마 (JSON)
```json
{
  "project_id": "uuid",
  "project_name": "나의 세계",
  "created_at": "2025-01-15T10:00:00",
  "updated_at": "2025-01-15T12:00:00",
  "genre": "SF판타지",
  
  "concept": {
    "logline": "한 줄 컨셉",
    "keywords": ["키워드1", "키워드2"]
  },
  
  "elements": {
    "space": {
      "description": "",
      "landmarks": [],
      "map_image": null,
      "boundary": ""
    },
    "time": {
      "description": "",
      "start_year": "",
      "timeline": []
    },
    "creatures": {
      "description": "",
      "species": [],
      "genealogy": []
    },
    "nature": {
      "description": "",
      "minerals": [],
      "ecosystem": ""
    },
    "culture": {
      "description": "",
      "religion": "",
      "architecture": "",
      "clothing": "",
      "technology_level": ""
    },
    "language": {
      "description": "",
      "writing_system": "",
      "samples": []
    },
    "mythology": {
      "description": "",
      "origin_story": "",
      "prophecies": []
    },
    "philosophy": {
      "description": "",
      "belief_system": "",
      "ideology": ""
    },
    "rules": {
      "natural": [],
      "social": [],
      "religious": []
    },
    "economy": {
      "description": "",
      "food_source": "",
      "trade": ""
    },
    "politics": {
      "description": "",
      "government_type": "",
      "military": ""
    },
    "energy": {
      "description": "",
      "power_source": ""
    }
  },
  
  "connections": [],
  "notes": "",
  "completion_rate": 0
}
```

### 4.2 DB 테이블 구조 (SQLite)
```sql
-- 프로젝트 테이블
CREATE TABLE projects (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    genre TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    data JSON
);

-- 템플릿 테이블
CREATE TABLE templates (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    genre TEXT,
    data JSON
);

-- 예시 작품 테이블
CREATE TABLE examples (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    genre TEXT,
    data JSON
);
```

---

## 5. UI/UX 설계

### 5.1 화면 구성 (Streamlit 기준)

```
┌─────────────────────────────────────────────────────────────┐
│  WorldBuilder                        [프로젝트 선택 ▼] [저장]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [사이드바]              │  [메인 영역]                      │
│  ─────────────          │  ─────────────────────────────    │
│  📋 대시보드              │                                   │
│  ✨ 컨셉                  │   현재 선택된 요소의               │
│  🗺️ 1. 공간              │   입력 폼 + 가이드 질문            │
│  ⏰ 2. 시간              │                                   │
│  👽 3. 크리쳐            │   [이전] [다음]                    │
│  🌿 4. 자연              │                                   │
│  🏛️ 5. 문화              │  ─────────────────────────────    │
│  📝 6. 언어              │                                   │
│  📜 7. 신화              │   [팁/예시 접기 ▼]                 │
│  💭 8. 철학              │   아바타 예시:                     │
│  ⚖️ 9.1 규칙            │   "판도라 행성, 할렐루야산"        │
│  💰 9.2 경제            │                                   │
│  🏰 9.3 정치            │                                   │
│  ⚡ 9.4 에너지          │                                   │
│  ─────────────          │                                   │
│  📊 연결성 보기          │                                   │
│  📥 내보내기             │                                   │
│                         │                                   │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 사용자 플로우
```
1. 새 프로젝트 생성
   └─> 프로젝트명, 장르 선택
   
2. 컨셉 입력 (시작점)
   └─> 한 줄 로그라인 작성
   
3. 12요소 순차 입력 (또는 원하는 순서로)
   └─> 각 요소별 가이드 질문 응답
   └─> 예시 참고 가능
   
4. 연결성 검토
   └─> 그래프로 요소 간 관계 확인
   └─> 빈 요소 알림
   
5. 내보내기
   └─> Markdown/PDF/JSON 선택
```

---

## 6. 개발 로드맵

### Phase 1: MVP (2주)
- [ ] 프로젝트 구조 세팅
- [ ] 기본 데이터 구조 구현
- [ ] Streamlit UI 기본 레이아웃
- [ ] 12요소 입력 폼
- [ ] JSON 저장/불러오기
- [ ] Markdown 내보내기

### Phase 2: 핵심 기능 (2주)
- [ ] SQLite 연동
- [ ] 가이드 질문 시스템
- [ ] 아바타 예시 데이터 입력
- [ ] 진행률 표시
- [ ] PDF 내보내기

### Phase 3: 고급 기능 (2주)
- [ ] 연결성 그래프 시각화
- [ ] 장르별 템플릿
- [ ] 타임라인 시각화
- [ ] 검색 기능

### Phase 4: 확장 (선택)
- [ ] AI 어시스턴트 연동 (Claude API)
- [ ] 다국어 지원
- [ ] 클라우드 동기화
- [ ] 협업 기능

---

## 7. 파일/폴더 구조

```
worldbuilder/
├── README.md
├── requirements.txt
├── .gitignore
│
├── app.py                 # Streamlit 메인 앱
├── config.py              # 설정값
│
├── data/
│   ├── elements.json      # 12요소 정의 데이터
│   ├── questions.json     # 가이드 질문
│   ├── examples/
│   │   └── avatar.json    # 아바타 예시
│   └── templates/
│       └── high_fantasy.json
│
├── database/
│   ├── db.py              # DB 연결 및 CRUD
│   └── worldbuilder.db    # SQLite DB
│
├── models/
│   ├── __init__.py
│   └── project.py         # 프로젝트 데이터 클래스
│
├── components/
│   ├── __init__.py
│   ├── sidebar.py         # 사이드바 컴포넌트
│   ├── element_form.py    # 요소 입력 폼
│   ├── dashboard.py       # 대시보드
│   └── export.py          # 내보내기 기능
│
├── utils/
│   ├── __init__.py
│   ├── markdown_export.py
│   └── pdf_export.py
│
└── tests/
    └── test_project.py
```

---

## 8. 핵심 코드 스니펫 (참고용)

### 8.1 요소 정의 데이터 예시
```python
ELEMENTS = {
    "concept": {
        "name": "세계의 컨셉",
        "icon": "✨",
        "questions": [
            "이 세계의 가장 큰 특징은 무엇인가요?",
            "한 문장으로 이 세계를 설명한다면?"
        ],
        "example": "아바타+인간 영혼, 바위산이 하늘에 떠있다"
    },
    "space": {
        "name": "공간",
        "icon": "🗺️",
        "questions": [
            "이 세계는 어떻게 생겼나요?",
            "가장 중요한 랜드마크는 무엇인가요?",
            "현실계와 환상계의 경계는 어디인가요?"
        ],
        "example": "판도라 행성, 할렐루야산"
    },
    # ... 나머지 요소들
}
```

### 8.2 Streamlit 기본 구조
```python
import streamlit as st

st.set_page_config(
    page_title="WorldBuilder",
    page_icon="🌍",
    layout="wide"
)

# 사이드바
with st.sidebar:
    st.title("🌍 WorldBuilder")
    selected = st.radio(
        "요소 선택",
        ["대시보드", "컨셉", "1. 공간", "2. 시간", ...]
    )

# 메인 영역
if selected == "대시보드":
    show_dashboard()
elif selected == "컨셉":
    show_element_form("concept")
# ...
```

---

## 9. 참고 자료

### 레퍼런스
- 들녘, <판타지라이브러리> 시리즈: 무기사전, 지옥 등
- AK커뮤니케이션, <AK 트리비아북> 시리즈: 중세유럽의 복장 등
- 서강대 월드빌딩워크숍 자료

### 유사 서비스 벤치마킹
- World Anvil (worldanvil.com)
- Campfire (campfirewriting.com)
- Notion 세계관 템플릿

---

## 10. 위험 요소 & 대응

| 위험 | 확률 | 영향 | 대응책 |
|------|------|------|--------|
| 기능 과다로 개발 지연 | 높음 | 높음 | MVP 우선, 점진적 확장 |
| UI/UX 복잡성 | 중간 | 중간 | Streamlit으로 단순화 |
| 데이터 손실 | 낮음 | 높음 | 자동 저장, JSON 백업 |

---

## 부록: 빠른 시작 가이드 (개발용)

```bash
# 1. 리포지토리 생성 후 클론
git clone https://github.com/yourusername/worldbuilder.git
cd worldbuilder

# 2. 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 의존성 설치
pip install streamlit pandas

# 4. 앱 실행
streamlit run app.py
```

---

*문서 작성일: 2025년 1월*
*버전: 1.0*
