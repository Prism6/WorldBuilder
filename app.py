"""
WorldBuilder main application entry point.
"""

import streamlit as st
from repositories.json_project_repository import JsonProjectRepository
from services.project_manager import ProjectManager
from exceptions import (
    ProjectNotFoundException,
    ProjectValidationError,
    ProjectSaveError,
    ProjectLoadError
)
from constants import DEFAULT_STORAGE_DIR
from utils.logger import get_logger
from components.sidebar import render_sidebar
from components.dashboard import render_dashboard

logger = get_logger(__name__)

# --- Initialize Services (Dependency Injection) ---
# Create repository and service instances
repository = JsonProjectRepository(storage_dir=DEFAULT_STORAGE_DIR)
project_manager = ProjectManager(repository=repository)

logger.info("WorldBuilder application initialized")

# --- Helper Functions ---
def create_new_project() -> None:
    """Initialize a new project in session state."""
    try:
        logger.debug("Creating new project from UI")
        st.session_state.current_project = project_manager.create_new_project()
        st.session_state.project_saved = False
        st.success("새 프로젝트가 생성되었습니다.")
        logger.info("New project created successfully")
    except ProjectValidationError as e:
        error_msg = f"프로젝트 생성 실패: {str(e)}"
        st.error(error_msg)
        logger.error(error_msg)

def load_project(project_id: str) -> None:
    """
    Load a project by ID into session state.

    Args:
        project_id: The unique identifier of the project to load
    """
    try:
        logger.debug(f"Loading project from UI: {project_id}")
        project = project_manager.load_project(project_id)
        st.session_state.current_project = project
        st.session_state.project_saved = True
        st.success(f"프로젝트 '{project.project_name}'을(를) 로드했습니다.")
        logger.info(f"Project loaded successfully: {project.project_name}")
    except ProjectNotFoundException as e:
        error_msg = f"프로젝트를 찾을 수 없습니다: {str(e)}"
        st.error(error_msg)
        logger.error(error_msg)
    except ProjectLoadError as e:
        error_msg = f"프로젝트 로드 실패: {str(e)}"
        st.error(error_msg)
        logger.error(error_msg)

def save_project() -> None:
    """Save the current project from session state to disk."""
    if 'current_project' not in st.session_state or not st.session_state.current_project:
        st.warning("저장할 프로젝트가 없습니다.")
        logger.warning("Save attempted with no current project")
        return

    try:
        project = st.session_state.current_project
        logger.debug(f"Saving project from UI: {project.project_id}")
        project_manager.save_project(project)
        st.session_state.project_saved = True
        st.success(f"프로젝트 '{project.project_name}'이(가) 저장되었습니다.")
        logger.info(f"Project saved successfully: {project.project_name}")
    except ProjectValidationError as e:
        error_msg = f"유효성 검증 실패: {str(e)}"
        st.error(error_msg)
        logger.error(error_msg)
    except ProjectSaveError as e:
        error_msg = f"프로젝트 저장 실패: {str(e)}"
        st.error(error_msg)
        logger.error(error_msg)

def get_available_projects() -> dict[str, str]:
    """
    Get all available projects.

    Returns:
        Dictionary mapping project IDs to project names
    """
    logger.debug("Getting available projects from UI")
    return project_manager.list_all_projects()

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="WorldBuilder",
    layout="wide"
)

# --- Session State Initialization ---
if 'current_project' not in st.session_state:
    create_new_project()

if 'project_saved' not in st.session_state:
    st.session_state.project_saved = True

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'dashboard'

# --- Sidebar ---
available_projects = get_available_projects()
new_page = render_sidebar(
    on_new_project=create_new_project,
    on_load_project=load_project,
    on_save_project=save_project,
    available_projects=available_projects,
    is_project_saved=st.session_state.project_saved,
    current_page=st.session_state.current_page
)

if new_page:
    st.session_state.current_page = new_page
    st.rerun()

# --- Main Content Area ---
project = st.session_state.current_project

# Unsaved changes warning
if not st.session_state.project_saved:
    st.warning("⚠️ 저장되지 않은 변경 사항이 있습니다.")

# Render current page
if st.session_state.current_page == 'dashboard':
    render_dashboard(
        project=project,
        on_edit_concept=lambda: st.info("컨셉 편집 기능은 곧 추가될 예정입니다."),
        on_goto_elements=lambda: st.session_state.update({'current_page': 'elements'})
    )
elif st.session_state.current_page == 'elements':
    st.title("🌍 12요소 편집")
    st.info("12요소 편집 페이지는 곧 구현될 예정입니다.")
elif st.session_state.current_page == 'connections':
    st.title("🔗 연결 관계")
    st.info("연결 관계 페이지는 곧 구현될 예정입니다.")
elif st.session_state.current_page == 'export':
    st.title("📤 내보내기")
    st.info("내보내기 페이지는 곧 구현될 예정입니다.")
