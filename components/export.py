"""
내보내기 컴포넌트.
"""

import streamlit as st
import json
from models.project import Project
from utils.markdown_export import generate_markdown, get_filename
from utils.logger import get_logger

logger = get_logger(__name__)


def render_export_page(project: Project) -> None:
    """
    내보내기 페이지를 렌더링합니다.

    Args:
        project: 현재 프로젝트
    """
    logger.debug(f"Rendering export page for project: {project.project_id}")

    st.title("📤 내보내기")
    st.markdown("프로젝트를 다양한 형식으로 내보내세요.")

    # 프로젝트 정보 표시
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("프로젝트", project.project_name)

    with col2:
        st.metric("완성도", f"{project.completion_rate * 100:.0f}%")

    with col3:
        filled_count = project._count_filled_elements()
        st.metric("작성된 요소", f"{filled_count}/12")

    st.markdown("---")

    # 내보내기 옵션을 탭으로 구분
    tab1, tab2 = st.tabs(["📝 Markdown", "💾 JSON"])

    # === Markdown 내보내기 ===
    with tab1:
        st.subheader("📝 Markdown 내보내기")
        st.caption("프로젝트를 읽기 쉬운 Markdown 문서로 변환합니다.")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("""
            **Markdown 형식의 장점**:
            - 📖 읽기 쉬운 텍스트 형식
            - 🌐 대부분의 플랫폼에서 지원 (GitHub, Notion 등)
            - ✏️ 텍스트 에디터로 추가 편집 가능
            - 📱 모바일에서도 읽기 편함
            """)

        with col2:
            # Markdown 생성 및 다운로드
            if st.button("📝 생성하기", key="generate_md", use_container_width=True, type="primary"):
                with st.spinner("Markdown 문서 생성 중..."):
                    try:
                        markdown_content = generate_markdown(project)
                        st.session_state['markdown_content'] = markdown_content
                        st.session_state['markdown_filename'] = get_filename(project)
                        st.success("✅ Markdown 문서가 생성되었습니다!")
                        logger.info(f"Markdown generated for project: {project.project_name}")
                    except Exception as e:
                        st.error(f"Markdown 생성 실패: {str(e)}")
                        logger.error(f"Markdown generation failed: {str(e)}")

        # 생성된 Markdown 미리보기 및 다운로드
        if 'markdown_content' in st.session_state:
            st.markdown("---")
            st.subheader("📄 미리보기")

            # 미리보기 옵션
            preview_option = st.radio(
                "미리보기 형식",
                ["렌더링된 형식", "원본 텍스트"],
                horizontal=True,
                label_visibility="collapsed"
            )

            if preview_option == "렌더링된 형식":
                # Markdown 렌더링
                with st.container():
                    st.markdown(st.session_state['markdown_content'])
            else:
                # 원본 텍스트
                st.text_area(
                    "Markdown 원본",
                    value=st.session_state['markdown_content'],
                    height=400,
                    label_visibility="collapsed"
                )

            # 다운로드 버튼
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 1, 1])

            with col2:
                st.download_button(
                    label="⬇️ 다운로드",
                    data=st.session_state['markdown_content'],
                    file_name=st.session_state['markdown_filename'],
                    mime="text/markdown",
                    use_container_width=True,
                    type="primary"
                )

    # === JSON 내보내기 ===
    with tab2:
        st.subheader("💾 JSON 백업")
        st.caption("프로젝트 전체 데이터를 JSON 형식으로 백업합니다.")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("""
            **JSON 백업의 장점**:
            - 🔒 완전한 데이터 보존 (모든 정보 포함)
            - 🔄 WorldBuilder로 다시 불러오기 가능
            - 💻 프로그래밍 방식으로 처리 가능
            - 📦 버전 관리 및 백업에 적합
            """)

        with col2:
            # JSON 생성 및 다운로드
            if st.button("💾 생성하기", key="generate_json", use_container_width=True, type="primary"):
                with st.spinner("JSON 백업 생성 중..."):
                    try:
                        json_data = project.to_dict()
                        json_content = json.dumps(json_data, ensure_ascii=False, indent=2)
                        st.session_state['json_content'] = json_content
                        st.session_state['json_filename'] = f"{project.project_name.replace(' ', '_')}.json"
                        st.success("✅ JSON 백업이 생성되었습니다!")
                        logger.info(f"JSON backup generated for project: {project.project_name}")
                    except Exception as e:
                        st.error(f"JSON 생성 실패: {str(e)}")
                        logger.error(f"JSON generation failed: {str(e)}")

        # 생성된 JSON 미리보기 및 다운로드
        if 'json_content' in st.session_state:
            st.markdown("---")
            st.subheader("📄 미리보기")

            # JSON 내용 표시 (접을 수 있는 형태)
            with st.expander("JSON 내용 보기", expanded=False):
                st.code(st.session_state['json_content'], language='json')

            # JSON 통계
            col1, col2, col3 = st.columns(3)

            json_data = json.loads(st.session_state['json_content'])

            with col1:
                st.metric("파일 크기", f"{len(st.session_state['json_content'])} bytes")

            with col2:
                st.metric("프로젝트 ID", json_data.get('project_id', 'N/A')[:8] + "...")

            with col3:
                st.metric("완성도", f"{json_data.get('completion_rate', 0) * 100:.0f}%")

            # 다운로드 버튼
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 1, 1])

            with col2:
                st.download_button(
                    label="⬇️ 다운로드",
                    data=st.session_state['json_content'],
                    file_name=st.session_state['json_filename'],
                    mime="application/json",
                    use_container_width=True,
                    type="primary"
                )

    # 하단 도움말
    st.markdown("---")
    with st.expander("💡 내보내기 팁"):
        st.markdown("""
        **Markdown 내보내기**:
        - 📖 **용도**: 문서화, 공유, 읽기 전용 자료
        - 🌐 **활용**: GitHub README, Notion, 블로그 등에 붙여넣기
        - ✏️ **편집**: 텍스트 에디터로 자유롭게 수정 가능
        - 🎨 **스타일**: 플랫폼에 따라 다르게 렌더링됨

        **JSON 백업**:
        - 💾 **용도**: 완전한 백업, 데이터 이전
        - 🔄 **복원**: WorldBuilder에서 다시 불러올 수 있음
        - 🔒 **안전**: 모든 데이터가 손실 없이 저장됨
        - 📅 **버전 관리**: Git 등으로 변경 이력 추적 가능

        **권장 백업 전략**:
        1. 주기적으로 JSON 백업 생성 (데이터 보존)
        2. 중요 마일스톤마다 Markdown 내보내기 (문서화)
        3. 여러 버전의 백업 파일 보관
        4. 클라우드 스토리지에 백업 저장

        **파일명 규칙**:
        - Markdown: `{프로젝트_이름}.md`
        - JSON: `{프로젝트_이름}.json`
        - 파일명에 특수문자가 있으면 언더스코어(_)로 변환됨
        """)
