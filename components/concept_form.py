"""
컨셉 편집 폼 컴포넌트.
"""

import streamlit as st
from models.project import Project
from typing import Callable, Optional
from utils.logger import get_logger

logger = get_logger(__name__)


def render_keyword_manager(
    current_keywords: list[str],
    on_update: Callable[[list[str]], None]
) -> None:
    """
    키워드 관리 UI를 렌더링합니다.

    Args:
        current_keywords: 현재 키워드 목록
        on_update: 키워드 업데이트 콜백
    """
    st.subheader("🏷️ 키워드")
    st.caption("세계관의 핵심 키워드를 관리하세요 (최대 10개 권장)")

    # 현재 키워드 표시
    if current_keywords:
        st.markdown("**현재 키워드**:")

        # 키워드를 3열로 표시
        cols_per_row = 3
        for i in range(0, len(current_keywords), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, col in enumerate(cols):
                idx = i + j
                if idx < len(current_keywords):
                    with col:
                        # 키워드와 삭제 버튼을 같은 행에 표시
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.markdown(
                                f'<span style="background-color: #2196F3; color: white; '
                                f'padding: 6px 12px; border-radius: 12px; '
                                f'display: inline-block; margin: 2px;">'
                                f'{current_keywords[idx]}</span>',
                                unsafe_allow_html=True
                            )
                        with col2:
                            if st.button("🗑️", key=f"del_kw_{idx}", help=f"'{current_keywords[idx]}' 삭제"):
                                new_keywords = [kw for k, kw in enumerate(current_keywords) if k != idx]
                                on_update(new_keywords)
                                st.rerun()
    else:
        st.info("💡 아직 추가된 키워드가 없습니다. 아래에서 키워드를 추가하세요.")

    # 새 키워드 추가
    st.markdown("---")
    st.markdown("**새 키워드 추가**:")

    col1, col2 = st.columns([3, 1])

    with col1:
        new_keyword = st.text_input(
            "키워드 입력",
            key="new_keyword_input",
            placeholder="예: 사이버펑크, 디스토피아, AI",
            label_visibility="collapsed"
        )

    with col2:
        if st.button("➕ 추가", use_container_width=True):
            if new_keyword and new_keyword.strip():
                keyword = new_keyword.strip()
                if keyword in current_keywords:
                    st.warning(f"'{keyword}'는 이미 추가된 키워드입니다.")
                elif len(current_keywords) >= 20:
                    st.warning("키워드는 최대 20개까지 추가할 수 있습니다.")
                else:
                    new_keywords = current_keywords + [keyword]
                    on_update(new_keywords)
                    st.success(f"'{keyword}' 키워드가 추가되었습니다!")
                    st.rerun()
            else:
                st.warning("키워드를 입력해주세요.")


def render_concept_form(
    project: Project,
    on_update_metadata: Callable[[Optional[str], Optional[str]], None],
    on_update_logline: Callable[[str], None],
    on_update_keywords: Callable[[list[str]], None]
) -> None:
    """
    컨셉 편집 폼 전체를 렌더링합니다.

    Args:
        project: 현재 프로젝트
        on_update_metadata: 메타데이터 업데이트 콜백 (project_name, genre)
        on_update_logline: 로그라인 업데이트 콜백
        on_update_keywords: 키워드 업데이트 콜백
    """
    logger.debug(f"Rendering concept form for project: {project.project_id}")

    st.title("💡 컨셉 편집")
    st.markdown("프로젝트의 핵심 컨셉과 메타데이터를 관리하세요.")

    st.markdown("---")

    # 1. 프로젝트 메타데이터 (폼 사용)
    st.subheader("📋 프로젝트 정보")

    with st.form("metadata_form"):
        col1, col2 = st.columns(2)

        with col1:
            project_name = st.text_input(
                "프로젝트 이름",
                value=project.project_name,
                help="세계관의 이름을 입력하세요.",
                max_chars=100
            )

        with col2:
            genre = st.text_input(
                "장르",
                value=project.genre,
                help="예: SF, 판타지, 현대판타지, 스팀펑크 등",
                max_chars=50
            )

        # 변경 여부 확인
        has_changes = (
            project_name != project.project_name or
            genre != project.genre
        )

        # 저장 버튼
        col1, col2, col3 = st.columns([2, 1, 1])

        with col2:
            if has_changes:
                st.caption("⚠️ 변경사항 있음")

        with col3:
            submitted = st.form_submit_button(
                "💾 저장",
                use_container_width=True,
                type="primary" if has_changes else "secondary"
            )

        if submitted:
            if not project_name or not project_name.strip():
                st.error("프로젝트 이름은 필수입니다.")
            elif not genre or not genre.strip():
                st.error("장르는 필수입니다.")
            else:
                on_update_metadata(project_name.strip(), genre.strip())
                st.success("프로젝트 정보가 저장되었습니다!")
                st.rerun()

    st.markdown("---")

    # 2. 로그라인 편집
    st.subheader("📝 로그라인")
    st.caption("세계관을 한 문장으로 표현하세요 (1-2줄 권장)")

    logline = st.text_area(
        "로그라인",
        value=project.concept.logline,
        height=100,
        help="세계관의 핵심을 간결하게 표현하는 한두 문장",
        max_chars=500,
        label_visibility="collapsed"
    )

    # 글자 수 표시
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        if logline:
            st.caption(f"✍️ {len(logline)}자 작성됨")
        else:
            st.caption("💡 로그라인을 작성해주세요.")

    with col2:
        if logline != project.concept.logline:
            st.caption("⚠️ 저장 필요")

    with col3:
        if st.button("💾 저장", key="save_logline", use_container_width=True):
            on_update_logline(logline)
            st.success("로그라인이 저장되었습니다!")
            st.rerun()

    st.markdown("---")

    # 3. 키워드 관리
    render_keyword_manager(
        current_keywords=project.concept.keywords,
        on_update=on_update_keywords
    )

    st.markdown("---")

    # 4. 도움말
    with st.expander("💡 컨셉 작성 가이드"):
        st.markdown("""
        **프로젝트 이름**:
        - 세계관의 정체성을 나타내는 이름
        - 기억하기 쉽고 발음하기 쉬운 이름 권장
        - 예: "네오 에덴", "크로니클 오브 아스트라", "붕괴된 세계"

        **장르**:
        - 세계관의 기본 톤과 분위기를 결정
        - 여러 장르를 혼합할 수 있음 (예: "SF + 판타지")
        - 일반적인 장르: SF, 판타지, 하이판타지, 로우판타지,
          사이버펑크, 스팀펑크, 포스트 아포칼립스, 현대판타지 등

        **로그라인**:
        - 세계관의 핵심을 1-2문장으로 압축
        - "이 세계는 ~한 곳이다" 형식으로 작성 가능
        - 핵심 갈등이나 특징을 포함
        - 예시:
          - "마법이 과학으로 발전한 세계, 마법공학이 모든 것을 지배한다"
          - "인류가 멸망한 후 AI가 지배하는 디스토피아"
          - "신들이 죽고 인간이 그 자리를 차지하려는 세계"

        **키워드**:
        - 세계관을 대표하는 핵심 단어들
        - 3-10개 권장
        - 분위기, 테마, 중요 요소를 포함
        - 예시:
          - SF: "AI", "사이버네틱", "우주 식민지", "시간여행"
          - 판타지: "드래곤", "고대 마법", "선택받은 자", "신화"
        """)

    # 5. 프로젝트 ID 및 생성 정보 (읽기 전용)
    with st.expander("ℹ️ 프로젝트 세부정보"):
        st.text(f"프로젝트 ID: {project.project_id}")
        st.text(f"생성일: {project.created_at}")
        st.text(f"최종 수정일: {project.updated_at}")
        st.text(f"완성도: {project.completion_rate * 100:.1f}%")
