import streamlit as st
from models.project import Project
from utils import json_utils
import os

# --- Constants ---
PROJECT_DIR = "data/projects" # Directory to save/load projects

# Ensure project directory exists
os.makedirs(PROJECT_DIR, exist_ok=True)

# --- Helper Functions ---
def _get_project_filepath(project_id):
    """Helper to get the full path for a project file."""
    return os.path.join(PROJECT_DIR, f"{project_id}.json")

def create_new_project():
    """Initializes a new project in session state."""
    st.session_state.current_project = Project()
    st.session_state.project_saved = False # Track if current project is saved
    st.success("새 프로젝트가 생성되었습니다.")

def load_project(project_id):
    """Loads a project by ID from disk into session state."""
    filepath = _get_project_filepath(project_id)
    data = json_utils.load_json(filepath)
    if data:
        st.session_state.current_project = Project.from_dict(data)
        st.session_state.project_saved = True
        st.success(f"프로젝트 '{st.session_state.current_project.project_name}'을(를) 로드했습니다.")
    else:
        st.error("프로젝트 로드에 실패했습니다.")

def save_project():
    """Saves the current project from session state to disk."""
    if 'current_project' in st.session_state and st.session_state.current_project:
        project = st.session_state.current_project
        filepath = _get_project_filepath(project.project_id)
        
        # Update updated_at timestamp
        import datetime
        project.updated_at = datetime.datetime.now().isoformat()
        
        if json_utils.save_json(filepath, project.to_dict()):
            st.session_state.project_saved = True
            st.success(f"프로젝트 '{project.project_name}'이(가) 저장되었습니다.")
        else:
            st.error("프로젝트 저장에 실패했습니다.")
    else:
        st.warning("저장할 프로젝트가 없습니다.")

def get_available_projects():
    """Returns a dictionary of available project IDs and names."""
    projects = {}
    for filename in os.listdir(PROJECT_DIR):
        if filename.endswith(".json"):
            project_id = filename.replace(".json", "")
            filepath = os.path.join(PROJECT_DIR, filename)
            data = json_utils.load_json(filepath)
            if data and "project_name" in data:
                projects[project_id] = data["project_name"]
            else:
                projects[project_id] = f"Unknown Project ({project_id})"
    return projects

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
    if new_project_name != project.project_name:
        project.project_name = new_project_name
        st.session_state.project_saved = False # Mark as unsaved
        
    new_genre = st.text_input("장르", value=project.genre, key="project_genre_input")
    if new_genre != project.genre:
        project.genre = new_genre
        st.session_state.project_saved = False # Mark as unsaved

    st.write(f"**생성일:** {project.created_at}")
    st.write(f"**수정일:** {project.updated_at}")
    st.progress(project.completion_rate, text=f"완성도: {project.completion_rate*100:.0f}%")

st.write("월드 빌딩 작업을 시작하세요!")

# Placeholder for main content components
st.subheader("프로젝트 개요 (향후 대시보드)")
st.write("여기에 프로젝트 대시보드가 표시됩니다.")

st.subheader("12요소 상세 설정 (향후)")
st.write("여기에 12요소별 상세 설정 UI가 표시됩니다.")

st.subheader("기타 기능 (향후)")
st.write("여기에 다른 기능들이 표시됩니다.")
