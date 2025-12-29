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
    create_new_project() # Start with a new project

if 'project_saved' not in st.session_state:
    st.session_state.project_saved = True # Assume new project is unsaved

# --- Sidebar ---
with st.sidebar:
    st.title("WorldBuilder 메뉴")
    st.markdown("---")

    st.header("프로젝트 관리")
    if st.button("새 프로젝트", help="새로운 월드 빌딩 프로젝트를 시작합니다."):
        if not st.session_state.project_saved:
            st.warning("현재 프로젝트가 저장되지 않았습니다. 계속 진행하면 변경 사항이 손실될 수 있습니다.")
            if st.button("강제로 새 프로젝트 생성"):
                create_new_project()
        else:
            create_new_project()

    available_projects = get_available_projects()
    if available_projects:
        project_names = list(available_projects.values())
        selected_project_name = st.selectbox("프로젝트 로드", project_names, help="기존 프로젝트를 선택하여 로드합니다.")
        
        # Get the ID of the selected project
        selected_project_id = next((pid for pid, name in available_projects.items() if name == selected_project_name), None)

        if selected_project_id and st.button("로드", help=f"'{selected_project_name}' 프로젝트를 로드합니다."):
            if not st.session_state.project_saved:
                st.warning("현재 프로젝트가 저장되지 않았습니다. 계속 진행하면 변경 사항이 손실될 수 있습니다.")
                if st.button("강제로 프로젝트 로드"):
                    load_project(selected_project_id)
            else:
                load_project(selected_project_id)
    else:
        st.info("저장된 프로젝트가 없습니다.")

    if st.button("프로젝트 저장", help="현재 프로젝트를 파일로 저장합니다."):
        save_project()
    
    st.markdown("---")
    st.write("사이드바 내용 (향후 컴포넌트)")

# --- Main Content Area ---
st.title(f"WorldBuilder: {st.session_state.current_project.project_name}")

if not st.session_state.project_saved:
    st.warning("⚠️ 저장되지 않은 변경 사항이 있습니다.")

# Project details expander
with st.expander("프로젝트 정보"):
    project = st.session_state.current_project
    st.write(f"**프로젝트 ID:** `{project.project_id}`")

    new_project_name = st.text_input("프로젝트 이름", value=project.project_name, key="project_name_input")
    new_genre = st.text_input("장르", value=project.genre, key="project_genre_input")

    # Check if metadata has changed
    if new_project_name != project.project_name or new_genre != project.genre:
        try:
            project_manager.update_project_metadata(
                project,
                project_name=new_project_name if new_project_name != project.project_name else None,
                genre=new_genre if new_genre != project.genre else None
            )
            st.session_state.project_saved = False
        except ProjectValidationError as e:
            st.error(f"유효성 검증 실패: {str(e)}")

    st.write(f"**생성일:** {project.created_at}")
    st.write(f"**수정일:** {project.updated_at}")

    # Update and display completion rate
    completion_rate = project_manager.get_project_completion_rate(project)
    st.progress(completion_rate, text=f"완성도: {completion_rate*100:.0f}%")

st.write("월드 빌딩 작업을 시작하세요!")

# Placeholder for main content components
st.subheader("프로젝트 개요 (향후 대시보드)")
st.write("여기에 프로젝트 대시보드가 표시됩니다.")

st.subheader("12요소 상세 설정 (향후)")
st.write("여기에 12요소별 상세 설정 UI가 표시됩니다.")

st.subheader("기타 기능 (향후)")
st.write("여기에 다른 기능들이 표시됩니다.")
