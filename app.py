"""
WorldBuilder main application entry point.
"""

from typing import Optional
import streamlit as st
from repositories.json_project_repository import JsonProjectRepository
from services.project_manager import ProjectManager
from models.project import Connection
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
from components.element_form import render_element_form
from components.concept_form import render_concept_form
from components.export import render_export_page
from components.connections import render_connections_page

logger = get_logger(__name__)


# --- Initialize Services (cached: initialized once per process) ---
@st.cache_resource
def _init_project_manager() -> ProjectManager:
    repo = JsonProjectRepository(storage_dir=DEFAULT_STORAGE_DIR)
    pm = ProjectManager(repository=repo)
    logger.info("WorldBuilder application initialized")
    return pm


project_manager = _init_project_manager()


# --- Helper Functions ---
def create_new_project(template_id: Optional[str] = None) -> None:
    """
    Initialize a new project in session state.

    Args:
        template_id: Optional template ID to use (e.g., 'fantasy', 'scifi')
    """
    try:
        if template_id and template_id != "blank":
            logger.debug(f"Creating new project from template: {template_id}")
            st.session_state.current_project = (
                project_manager.create_project_from_template(template_id)
            )
            st.success(f"템플릿 '{template_id}'로 새 프로젝트가 생성되었습니다.")
            logger.info(f"New project created from template: {template_id}")
        else:
            logger.debug("Creating new blank project from UI")
            st.session_state.current_project = project_manager.create_new_project()
            st.success("새 프로젝트가 생성되었습니다.")
            logger.info("New blank project created successfully")

        st.session_state.project_saved = False

    except ProjectValidationError as e:
        error_msg = f"프로젝트 생성 실패: {str(e)}"
        st.error(error_msg)
        logger.error(error_msg)
    except ProjectLoadError as e:
        error_msg = f"템플릿 로드 실패: {str(e)}"
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


def get_available_templates() -> dict[str, dict[str, str]]:
    """
    Get all available project templates.

    Returns:
        Dictionary mapping template IDs to template metadata
    """
    logger.debug("Getting available templates from UI")
    return ProjectManager.list_templates()


def update_element(element_name: str, description: str) -> None:
    """
    Update a world element via the service layer.

    Args:
        element_name: Name of the element to update
        description: New description for the element
    """
    try:
        logger.debug(f"Updating element '{element_name}' from UI")
        project = st.session_state.current_project
        project_manager.update_project_element(project, element_name, description)
        st.session_state.project_saved = False
        logger.info(f"Element '{element_name}' updated successfully")
    except ProjectValidationError as e:
        error_msg = f"요소 업데이트 실패: {str(e)}"
        st.error(error_msg)
        logger.error(error_msg)


def update_rules(natural: list[str], social: list[str], religious: list[str]) -> None:
    """
    Update the rules element via the service layer.

    Args:
        natural: List of natural rules
        social: List of social rules
        religious: List of religious rules
    """
    try:
        logger.debug("Updating rules element from UI")
        project = st.session_state.current_project
        project_manager.update_project_rules(project, natural, social, religious)
        st.session_state.project_saved = False
        logger.info("Rules element updated successfully")
    except Exception as e:
        error_msg = f"규칙 업데이트 실패: {str(e)}"
        st.error(error_msg)
        logger.error(error_msg)


def update_concept_metadata(project_name: Optional[str], genre: Optional[str]) -> None:
    """
    Update project metadata (name and genre) via the service layer.

    Args:
        project_name: New project name
        genre: New genre
    """
    try:
        logger.debug("Updating project metadata from UI")
        project = st.session_state.current_project
        project_manager.update_project_metadata(project, project_name, genre)
        st.session_state.project_saved = False
        logger.info(f"Project metadata updated: name={project_name}, genre={genre}")
    except ProjectValidationError as e:
        error_msg = f"메타데이터 업데이트 실패: {str(e)}"
        st.error(error_msg)
        logger.error(error_msg)


def update_concept_logline(logline: str) -> None:
    """
    Update project logline via the service layer.

    Args:
        logline: New logline
    """
    try:
        logger.debug("Updating project logline from UI")
        project = st.session_state.current_project
        project_manager.update_project_logline(project, logline)
        st.session_state.project_saved = False
        logger.info("Project logline updated")
    except Exception as e:
        error_msg = f"로그라인 업데이트 실패: {str(e)}"
        st.error(error_msg)
        logger.error(error_msg)


def update_concept_keywords(keywords: list[str]) -> None:
    """
    Update project keywords via the service layer.

    Args:
        keywords: New keywords list
    """
    try:
        logger.debug("Updating project keywords from UI")
        project = st.session_state.current_project
        project_manager.update_project_keywords(project, keywords)
        st.session_state.project_saved = False
        logger.info(f"Project keywords updated: {len(keywords)} keywords")
    except Exception as e:
        error_msg = f"키워드 업데이트 실패: {str(e)}"
        st.error(error_msg)
        logger.error(error_msg)


def add_connection(connection: Connection) -> None:
    """
    Add a new connection between elements.

    Args:
        connection: Connection object with from_element, to_element,
                    connection_type, description
    """
    try:
        logger.debug(
            f"Adding connection: {connection.from_element} -> "
            f"{connection.to_element}"
        )
        project = st.session_state.current_project
        project.add_connection(connection)
        st.session_state.project_saved = False
        logger.info(f"Connection added successfully. Total: {len(project.connections)}")
    except Exception as e:
        error_msg = f"연결 추가 실패: {str(e)}"
        st.error(error_msg)
        logger.error(error_msg)


def delete_connection(index: int) -> None:
    """
    Delete a connection by index.

    Args:
        index: Index of connection to delete
    """
    try:
        logger.debug(f"Deleting connection at index {index}")
        project = st.session_state.current_project
        project.remove_connection(index)
        st.session_state.project_saved = False
        logger.info(f"Connection deleted. Remaining: {len(project.connections)}")
    except IndexError:
        error_msg = f"잘못된 연결 인덱스: {index}"
        st.error(error_msg)
        logger.error(error_msg)
    except Exception as e:
        error_msg = f"연결 삭제 실패: {str(e)}"
        st.error(error_msg)
        logger.error(error_msg)


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
available_templates = get_available_templates()
new_page = render_sidebar(
    on_new_project=create_new_project,
    on_load_project=load_project,
    on_save_project=save_project,
    available_projects=available_projects,
    available_templates=available_templates,
    is_project_saved=st.session_state.project_saved,
    current_page=st.session_state.current_page
)

if new_page:
    st.session_state.current_page = new_page
    st.rerun()

# --- Main Content Area ---
project = st.session_state.current_project

if not st.session_state.project_saved:
    st.warning("⚠️ 저장되지 않은 변경 사항이 있습니다.")

if st.session_state.current_page == 'dashboard':
    render_dashboard(
        project=project,
        on_edit_concept=lambda: st.session_state.update({'current_page': 'concept'}),
        on_goto_elements=lambda: st.session_state.update({'current_page': 'elements'}),
        on_goto_connections=lambda: st.session_state.update({'current_page': 'connections'})
    )
elif st.session_state.current_page == 'concept':
    render_concept_form(
        project=project,
        on_update_metadata=update_concept_metadata,
        on_update_logline=update_concept_logline,
        on_update_keywords=update_concept_keywords
    )
    st.markdown("---")
    if st.button("⬅️ 대시보드로 돌아가기", use_container_width=True):
        st.session_state.current_page = 'dashboard'
        st.rerun()
elif st.session_state.current_page == 'elements':
    render_element_form(
        project=project,
        on_update_element=update_element,
        on_update_rules=update_rules
    )
elif st.session_state.current_page == 'connections':
    render_connections_page(
        project=project,
        on_add_connection=add_connection,
        on_delete_connection=delete_connection
    )
elif st.session_state.current_page == 'export':
    render_export_page(project=project)
