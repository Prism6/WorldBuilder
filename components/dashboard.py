"""
Dashboard component for project overview.
"""

import streamlit as st
from models.project import Project
from typing import Callable
from utils.logger import get_logger
from constants import ELEMENT_NAMES, ALL_ELEMENT_NAMES

logger = get_logger(__name__)


def render_project_header(project: Project) -> None:
    """
    Render project header with title and basic info.

    Args:
        project: The current project
    """
    col1, col2 = st.columns([3, 1])

    with col1:
        st.title(f"🌏 {project.project_name}")
        st.caption(f"장르: {project.genre}")

    with col2:
        completion = project.completion_rate
        st.metric(
            "완성도",
            f"{completion * 100:.0f}%",
            delta=None
        )


def render_project_stats(project: Project) -> None:
    """
    Render project statistics cards.

    Args:
        project: The current project
    """
    st.subheader("📊 프로젝트 통계")

    col1, col2, col3, col4 = st.columns(4)

    # Count filled elements
    filled_count = project._count_filled_elements()

    with col1:
        st.metric("작성된 요소", f"{filled_count}/12")

    with col2:
        # Count keywords
        keyword_count = len(project.concept.keywords)
        st.metric("키워드", f"{keyword_count}")

    with col3:
        # Count connections
        connection_count = len(project.connections)
        st.metric("연결 관계", f"{connection_count}")

    with col4:
        # Notes length
        notes_length = len(project.notes)
        st.metric("노트 길이", f"{notes_length}자")


def render_element_progress(project: Project) -> None:
    """
    Render progress bars for each world element.

    Args:
        project: The current project
    """
    st.subheader("📝 요소별 진행도")

    element_labels = {
        'space': '🌌 공간',
        'time': '⏰ 시간',
        'creatures': '👥 생물',
        'nature': '🌿 자연',
        'culture': '🎭 문화',
        'language': '🗣️ 언어',
        'mythology': '⚡ 신화',
        'philosophy': '💭 철학',
        'rules': '⚖️ 규칙',
        'economy': '💰 경제',
        'politics': '🏛️ 정치',
        'energy': '✨ 에너지'
    }

    # Create two columns for elements
    col1, col2 = st.columns(2)

    for idx, element_name in enumerate(ALL_ELEMENT_NAMES):
        element = getattr(project.elements, element_name)
        label = element_labels.get(element_name, element_name)

        # Determine if element is filled
        if element_name == 'rules':
            is_filled = (element.natural or element.social or element.religious)
        else:
            is_filled = bool(element.description and element.description.strip())

        # Display in alternating columns
        with col1 if idx % 2 == 0 else col2:
            if is_filled:
                st.progress(1.0, text=f"{label} ✅")
            else:
                st.progress(0.0, text=f"{label} ⬜")


def render_concept_overview(project: Project) -> None:
    """
    Render project concept overview.

    Args:
        project: The current project
    """
    st.subheader("💡 컨셉")

    if project.concept.logline:
        st.info(f"**로그라인**: {project.concept.logline}")
    else:
        st.info("💡 로그라인이 아직 작성되지 않았습니다.")

    if project.concept.keywords:
        st.write("**키워드**:")
        # Display keywords as tags
        keywords_html = " ".join(
            [f'<span style="background-color: #2196F3; color: white; '
             f'padding: 4px 12px; border-radius: 12px; margin: 2px; '
             f'display: inline-block;">{kw}</span>'
             for kw in project.concept.keywords]
        )
        st.markdown(keywords_html, unsafe_allow_html=True)
    else:
        st.caption("키워드가 아직 추가되지 않았습니다.")


def render_quick_actions(
    project: Project,
    on_edit_concept: Callable[[], None],
    on_goto_elements: Callable[[], None],
    on_goto_connections: Callable[[], None]
) -> None:
    """
    Render quick action buttons.

    Args:
        project: The current project
        on_edit_concept: Callback for editing concept
        on_goto_elements: Callback for navigating to elements page
        on_goto_connections: Callback for navigating to connections page
    """
    st.subheader("🚀 빠른 작업")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("✏️ 컨셉 편집", use_container_width=True):
            on_edit_concept()

    with col2:
        if st.button("🌍 요소 작성", use_container_width=True):
            on_goto_elements()

    with col3:
        if st.button("🔗 연결 추가", use_container_width=True):
            on_goto_connections()


def render_dashboard(
    project: Project,
    on_edit_concept: Callable[[], None],
    on_goto_elements: Callable[[], None],
    on_goto_connections: Callable[[], None]
) -> None:
    """
    Render complete dashboard page.

    Args:
        project: The current project
        on_edit_concept: Callback for editing concept
        on_goto_elements: Callback for navigating to elements page
        on_goto_connections: Callback for navigating to connections page
    """
    logger.debug(f"Rendering dashboard for project: {project.project_id}")

    # Header
    render_project_header(project)

    st.markdown("---")

    # Statistics
    render_project_stats(project)

    st.markdown("---")

    # Element Progress
    render_element_progress(project)

    st.markdown("---")

    # Concept Overview
    render_concept_overview(project)

    st.markdown("---")

    # Quick Actions
    render_quick_actions(project, on_edit_concept, on_goto_elements, on_goto_connections)
