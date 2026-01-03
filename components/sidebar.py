"""
Sidebar component for project management.
"""

import streamlit as st
from typing import Callable, Dict, Optional
from utils.logger import get_logger

logger = get_logger(__name__)


def render_project_management(
    on_new_project: Callable[[Optional[str]], None],
    on_load_project: Callable[[str], None],
    on_save_project: Callable[[], None],
    available_projects: Dict[str, str],
    available_templates: Dict[str, Dict[str, str]],
    is_project_saved: bool
) -> None:
    """
    Render project management section in sidebar.

    Args:
        on_new_project: Callback for creating new project (with optional template_id)
        on_load_project: Callback for loading a project
        on_save_project: Callback for saving current project
        available_projects: Dictionary of project IDs to names
        available_templates: Dictionary of template IDs to template metadata
        is_project_saved: Whether current project has unsaved changes
    """
    st.header("프로젝트 관리")

    # Template selection in expander
    with st.expander("🎨 템플릿 선택", expanded=False):
        st.caption("템플릿을 선택하면 예시 데이터가 포함된 프로젝트가 생성됩니다")

        template_id = st.radio(
            "템플릿",
            options=list(available_templates.keys()),
            format_func=lambda x: available_templates[x]["name"],
            help="프로젝트 템플릿을 선택하세요",
            label_visibility="collapsed"
        )

        # Show template description
        if template_id:
            st.caption(available_templates[template_id]["description"])

    # New Project Button
    if st.button("📝 새 프로젝트", use_container_width=True,
                 help="새로운 월드 빌딩 프로젝트를 시작합니다."):
        if not is_project_saved:
            st.warning("⚠️ 현재 프로젝트가 저장되지 않았습니다.")
            if st.button("강제로 새 프로젝트 생성", key="force_new"):
                on_new_project(template_id)
                st.rerun()
        else:
            on_new_project(template_id)
            st.rerun()

    # Load Project
    if available_projects:
        st.subheader("프로젝트 로드")
        project_names = list(available_projects.values())
        selected_project_name = st.selectbox(
            "프로젝트 선택",
            project_names,
            help="기존 프로젝트를 선택하여 로드합니다.",
            label_visibility="collapsed"
        )

        # Get the ID of the selected project
        selected_project_id = next(
            (pid for pid, name in available_projects.items()
             if name == selected_project_name),
            None
        )

        if selected_project_id and st.button(
            "📂 로드",
            use_container_width=True,
            help=f"'{selected_project_name}' 프로젝트를 로드합니다."
        ):
            if not is_project_saved:
                st.warning("⚠️ 현재 프로젝트가 저장되지 않았습니다.")
                if st.button("강제로 프로젝트 로드", key="force_load"):
                    on_load_project(selected_project_id)
                    st.rerun()
            else:
                on_load_project(selected_project_id)
                st.rerun()
    else:
        st.info("💡 저장된 프로젝트가 없습니다.")

    # Save Project Button
    st.button(
        "💾 프로젝트 저장",
        use_container_width=True,
        on_click=on_save_project,
        help="현재 프로젝트를 파일로 저장합니다.",
        type="primary" if not is_project_saved else "secondary"
    )


def render_navigation(current_page: Optional[str] = None) -> Optional[str]:
    """
    Render navigation menu in sidebar.

    Args:
        current_page: Currently active page

    Returns:
        Selected page name, or None if no change
    """
    st.header("메뉴")

    pages = {
        "dashboard": "📊 대시보드",
        "elements": "🌍 12요소 편집",
        "connections": "🔗 연결 관계",
        "export": "📤 내보내기"
    }

    selected = st.radio(
        "페이지 선택",
        list(pages.keys()),
        format_func=lambda x: pages[x],
        index=list(pages.keys()).index(current_page) if current_page else 0,
        label_visibility="collapsed"
    )

    return selected if selected != current_page else None


def render_sidebar(
    on_new_project: Callable[[Optional[str]], None],
    on_load_project: Callable[[str], None],
    on_save_project: Callable[[], None],
    available_projects: Dict[str, str],
    available_templates: Dict[str, Dict[str, str]],
    is_project_saved: bool,
    current_page: Optional[str] = "dashboard"
) -> Optional[str]:
    """
    Render complete sidebar.

    Args:
        on_new_project: Callback for creating new project (with optional template_id)
        on_load_project: Callback for loading a project
        on_save_project: Callback for saving current project
        available_projects: Dictionary of project IDs to names
        available_templates: Dictionary of template IDs to template metadata
        is_project_saved: Whether current project has unsaved changes
        current_page: Currently active page

    Returns:
        New page selection, or None if no change
    """
    with st.sidebar:
        st.title("🌏 WorldBuilder")
        st.markdown("---")

        # Project Management Section
        render_project_management(
            on_new_project,
            on_load_project,
            on_save_project,
            available_projects,
            available_templates,
            is_project_saved
        )

        st.markdown("---")

        # Navigation Section
        new_page = render_navigation(current_page)

        st.markdown("---")

        # Footer
        st.caption("v0.1.0 - WB03")
        st.caption("Made with Claude Code")

        return new_page
