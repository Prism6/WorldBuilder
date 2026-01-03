# 🌏 WorldBuilder

> **체계적인 세계관 구축 도구** - SF/판타지 창작자를 위한 인터랙티브 월드빌딩 애플리케이션

WorldBuilder는 작가, 게임 디자이너, TRPG 마스터들이 깊이 있고 일관성 있는 세계관을 만들 수 있도록 돕는 Streamlit 기반 웹 애플리케이션입니다. 12가지 핵심 요소 프레임워크를 통해 체계적으로 세계를 설계하고, 요소 간 연결 관계를 시각화하며, 완성된 세계관을 문서로 내보낼 수 있습니다.

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.52.2-FF4B4B.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## ✨ 주요 기능

### 🎯 12요소 프레임워크

WorldBuilder는 세계관을 구성하는 12가지 핵심 요소를 제공합니다:

| 요소 | 아이콘 | 설명 |
|------|--------|------|
| **공간** | 🌌 | 지리, 지형, 지도, 랜드마크 |
| **시간** | ⏰ | 역사, 타임라인, 달력 체계 |
| **생물** | 👥 | 종족, 생명체, 인구 구성 |
| **자연** | 🌿 | 기후, 생태계, 자연 환경 |
| **문화** | 🎭 | 예술, 전통, 관습, 가치관 |
| **언어** | 🗣️ | 언어 체계, 문자, 방언 |
| **신화** | ⚡ | 종교, 신화, 전설, 믿음 |
| **철학** | 💭 | 사상, 이념, 세계관 |
| **규칙** | ⚖️ | 자연법칙, 사회규범, 종교법 |
| **경제** | 💰 | 경제 체제, 무역, 화폐 |
| **정치** | 🏛️ | 정치 체제, 권력 구조, 외교 |
| **에너지** | ✨ | 마법, 과학기술, 에너지원 |

### 📋 완성된 기능 (6/6)

✅ **프로젝트 관리**
- 새 프로젝트 생성
- 프로젝트 저장 및 로드
- JSON 기반 파일 저장
- 자동 타임스탬프 관리

✅ **대시보드**
- 프로젝트 통계 (작성된 요소, 키워드 수, 연결 수)
- 12요소 진행도 시각화
- 완성도 퍼센트 표시
- 빠른 작업 버튼

✅ **컨셉 편집**
- 프로젝트명 및 장르 설정
- 로그라인 작성 (500자 제한)
- 키워드 관리 (태그 스타일 UI, 최대 20개)
- 실시간 글자 수 카운터

✅ **12요소 편집**
- 탭 기반 UI (12개 탭)
- 각 요소별 상세 설명 작성
- 규칙 요소 특수 처리 (자연법칙/사회규범/종교법)
- 진행도 자동 업데이트
- 작성 팁 제공

✅ **연결 관계**
- 요소 간 관계 정의 (6가지 관계 타입)
- 카드 기반 목록 표시
- 관계 타입 필터링
- 통계 대시보드
- 연결 관계 설명 추가

✅ **내보내기**
- **Markdown**: 구조화된 문서로 변환
- **JSON**: 완전한 데이터 백업
- 미리보기 기능 (렌더링/원본)
- 안전한 파일명 생성

---

## 🚀 빠른 시작

### 필수 요구사항

- Python 3.11 이상
- pip (Python 패키지 관리자)

### 설치 방법

1. **저장소 클론**
```bash
git clone https://github.com/Prism6/WorldBuilder.git
cd WorldBuilder
```

2. **의존성 설치**
```bash
pip install -r requirements.txt
```

3. **애플리케이션 실행**
```bash
streamlit run app.py
```

4. **브라우저 접속**
```
http://localhost:8501
```

---

## 📖 사용 가이드

### 1. 새 프로젝트 시작

1. 좌측 사이드바에서 **"🆕 새 프로젝트"** 클릭
2. 프로젝트가 자동으로 생성됩니다
3. 대시보드에서 현재 프로젝트 상태 확인

### 2. 컨셉 정의

1. 대시보드에서 **"✏️ 컨셉 편집"** 클릭
2. 프로젝트명과 장르 입력
3. 로그라인 작성 (세계관을 한 문장으로 요약)
4. 키워드 추가 (최대 20개)

**예시**:
- **프로젝트명**: 크리스탈 제국
- **장르**: 하이 판타지
- **로그라인**: 마법 크리스탈의 힘으로 움직이는 거대 공중도시들이 떠 있는 세계
- **키워드**: 공중도시, 크리스탈 마법, 떠있는 섬, 스카이 파이럿

### 3. 12요소 작성

1. 사이드바 또는 대시보드에서 **"🌍 12요소 편집"** 선택
2. 12개 탭 중 하나를 선택
3. 각 요소에 대한 설명 작성
4. **💾 저장** 버튼 클릭
5. 진행도 바에서 완성도 확인

**작성 팁**:
- 구체적으로: "큰 산이 있다" → "북부에 3,000m급 설산 산맥이 동서로 뻗어있다"
- 독창성: 다른 세계관과 차별화되는 요소 추가
- 일관성: 요소 간 모순이 없도록 주의

### 4. 연결 관계 설정

1. 사이드바에서 **"🔗 연결 관계"** 선택
2. 우측 폼에서:
   - **시작 요소** 선택
   - **대상 요소** 선택
   - **관계 유형** 선택 (영향, 의존, 충돌, 조화, 원인, 가능)
   - **설명** 입력
3. **✅ 연결 추가** 클릭

**연결 예시**:
- 🌌 공간 → 영향을 준다 → 🎭 문화
  - "산악 지형이 폐쇄적인 부족 문화를 형성했다"
- 💰 경제 ⇆ 의존한다 → 🏛️ 정치
  - "크리스탈 무역 길드가 정치적 영향력을 행사한다"

### 5. 프로젝트 저장

1. 좌측 사이드바에서 **"💾 프로젝트 저장"** 클릭
2. `data/projects/` 폴더에 JSON 파일로 저장됨
3. 미저장 경고가 사라지면 저장 완료

### 6. 내보내기

1. 사이드바에서 **"📤 내보내기"** 선택
2. **Markdown** 또는 **JSON** 탭 선택
3. **생성하기** 버튼 클릭
4. 미리보기 확인
5. **⬇️ 다운로드** 버튼으로 파일 저장

**용도**:
- **Markdown**: 문서화, GitHub, 블로그, Notion
- **JSON**: 백업, 다른 도구로 데이터 이전

---

## 🏗️ 프로젝트 구조

```
WorldBuilder/
├── app.py                          # 메인 애플리케이션
├── config.py                       # 설정
├── constants.py                    # 상수 정의
├── exceptions.py                   # 커스텀 예외
├── requirements.txt                # Python 의존성
│
├── components/                     # UI 컴포넌트
│   ├── sidebar.py                 # 사이드바
│   ├── dashboard.py               # 대시보드
│   ├── element_form.py            # 12요소 편집 폼
│   ├── concept_form.py            # 컨셉 편집 폼
│   ├── connections.py             # 연결 관계 UI
│   └── export.py                  # 내보내기 UI
│
├── models/                         # 데이터 모델
│   └── project.py                 # Project, Concept, WorldElements
│
├── repositories/                   # 데이터 저장소
│   ├── project_repository.py      # 인터페이스
│   └── json_project_repository.py # JSON 구현
│
├── services/                       # 비즈니스 로직
│   └── project_manager.py         # 프로젝트 관리 서비스
│
├── utils/                          # 유틸리티
│   ├── json_utils.py              # JSON 처리
│   ├── logger.py                  # 로깅
│   └── markdown_export.py         # Markdown 변환
│
├── data/                           # 데이터 저장
│   └── projects/                  # 프로젝트 JSON 파일
│
└── docs/                           # 문서
    ├── 20251228_DevLog_WB01.md
    ├── 20251229_DevLog_WB02.md
    ├── 20260102_DevLog_WB03.md
    └── 20260103_DevLog_WB04.md
```

---

## 🛠️ 기술 스택

### 프론트엔드
- **Streamlit 1.52.2**: 웹 UI 프레임워크
- **Python 3.11**: 메인 언어

### 백엔드
- **JSON**: 데이터 저장 형식
- **Python dataclasses**: 데이터 모델

### 개발 도구
- **mypy**: 정적 타입 체크
- **flake8**: 코드 스타일 검사 (PEP8)
- **radon**: 복잡도 분석

### 아키텍처 패턴
- **Repository Pattern**: 데이터 접근 추상화
- **Dependency Injection**: 느슨한 결합
- **Callback Pattern**: UI와 로직 분리
- **SOLID 원칙**: 객체지향 설계

---

## 📊 코드 품질

```bash
# 타입 체크
mypy models/ services/ repositories/ components/

# 스타일 체크
flake8 .

# 복잡도 분석
radon cc . -a

# 유지보수성 지수
radon mi .
```

**현재 메트릭**:
- ✅ mypy: 0 경고
- ✅ flake8: 0 경고
- ✅ Cyclomatic Complexity: A등급 (평균 2.1)
- ✅ Maintainability Index: A등급 (평균 92.3)

---

## 📚 개발 문서

자세한 개발 과정과 설계 결정은 DevLog를 참조하세요:

- [WB01 - 초기 프로젝트 구조](20251228_DevLog_WB01.md)
- [WB02 - 객체지향 리팩토링](20251229_DevLog_WB02.md)
- [WB03 - UI 컴포넌트 구현 (Phase 1-4)](20260102_DevLog_WB03.md)
- [WB04 - 연결 관계 기능 완성 (Phase 5)](20260103_DevLog_WB04.md)

---

## 🗺️ 로드맵

### ✅ 완료된 기능 (v1.0 - MVP)

- [x] 프로젝트 관리 (생성, 로드, 저장)
- [x] 대시보드 및 통계
- [x] 컨셉 편집
- [x] 12요소 편집
- [x] 연결 관계 관리
- [x] Markdown/JSON 내보내기

### 🔮 향후 계획

**v1.1 - 품질 개선**
- [ ] pytest 테스트 작성
- [ ] 사용자 가이드 문서
- [ ] 에러 처리 개선

**v1.2 - 기능 확장**
- [ ] 연결 관계 네트워크 그래프 시각화
- [ ] 프로젝트 템플릿 제공 (판타지, SF, 현대)
- [ ] PDF 내보내기

**v2.0 - 협업 기능**
- [ ] 다중 사용자 지원
- [ ] 프로젝트 공유 및 협업
- [ ] 버전 관리

---

## 🤝 기여하기

WorldBuilder에 기여하고 싶으시다면:

1. 이 저장소를 Fork하세요
2. 새 브랜치를 만드세요 (`git checkout -b feature/amazing-feature`)
3. 변경사항을 커밋하세요 (`git commit -m 'Add amazing feature'`)
4. 브랜치에 Push하세요 (`git push origin feature/amazing-feature`)
5. Pull Request를 생성하세요

### 개발 환경 설정

```bash
# 저장소 클론
git clone https://github.com/Prism6/WorldBuilder.git
cd WorldBuilder

# 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 개발 의존성 설치
pip install -r requirements.txt

# 코드 품질 검사
mypy models/ services/ repositories/
flake8 .

# 앱 실행
streamlit run app.py
```

---

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

---

## 👏 크레딧

**개발**:
- Claude Sonnet 4.5 (Anthropic) - AI 개발 파트너
- Sangbuhm Hahn (a.k.a. Buhmtastic) (snakelogan202@gmail.com) - 프로젝트 기획 및 설계

**기술**:
- [Streamlit](https://streamlit.io/) - 웹 UI 프레임워크
- [Python](https://www.python.org/) - 프로그래밍 언어

---

## 📞 문의 및 지원

- **이슈**: [GitHub Issues](https://github.com/Prism6/WorldBuilder/issues)
- **문서**: [DevLogs](https://github.com/Prism6/WorldBuilder/tree/main/)

---

<div align="center">

**🌏 WorldBuilder로 당신만의 세계를 만들어보세요! 🌏**

Made with ❤️ and [Claude Code](https://claude.com/claude-code)

</div>
