"""
Service layer for project management business logic.
"""

import os
import json
from typing import Dict, Optional, List
from models.project import Project
from repositories.project_repository import ProjectRepository
from exceptions import ProjectNotFoundException, ProjectLoadError
from utils.logger import get_logger
from constants import (
    DEFAULT_PROJECT_NAME,
    DEFAULT_GENRE,
    ERROR_PROJECT_NOT_FOUND
)

logger = get_logger(__name__)

# Template directory
TEMPLATE_DIR = "templates"

# Available templates with metadata
TEMPLATES = {
    "blank": {
        "name": "📄 빈 템플릿",
        "description": "기본 구조만 있는 빈 프로젝트",
        "file": "blank.json"
    },
    "fantasy": {
        "name": "🏰 판타지",
        "description": "마법과 드래곤의 중세 판타지 세계",
        "file": "fantasy.json"
    },
    "scifi": {
        "name": "🚀 SF",
        "description": "우주 식민지와 미래 기술의 SF 세계",
        "file": "scifi.json"
    },
    "modern": {
        "name": "🏙️ 현대",
        "description": "기업 지배 디스토피아 현대 도시",
        "file": "modern.json"
    }
}


class ProjectManager:
    """
    Service class for managing project business logic.
    Follows Single Responsibility Principle by handling only business logic.
    Uses Dependency Inversion Principle by depending on ProjectRepository abstraction.
    """

    def __init__(self, repository: ProjectRepository) -> None:
        """
        Initialize the project manager with a repository.

        Args:
            repository: Repository implementation for project persistence.
        """
        self.repository = repository
        logger.info(f"ProjectManager initialized with {repository.__class__.__name__}")

    def create_new_project(
        self,
        project_name: str = DEFAULT_PROJECT_NAME,
        genre: str = DEFAULT_GENRE
    ) -> Project:
        """
        Create a new project with default or specified values.

        Args:
            project_name: Name of the new project (default: from constants)
            genre: Genre of the project (default: from constants)

        Returns:
            The newly created project

        Raises:
            ProjectValidationError: If validation fails
        """
        logger.info(f"Creating new project: '{project_name}' ({genre})")

        project = Project(project_name=project_name, genre=genre)
        project.validate()

        logger.debug(f"New project created with ID: {project.project_id}")
        return project

    def save_project(self, project: Project) -> bool:
        """
        Save a project after validating and updating completion rate.

        Args:
            project: The project to save

        Returns:
            True if successful

        Raises:
            ProjectValidationError: If validation fails
            ProjectSaveError: If save operation fails
        """
        logger.info(f"Saving project: {project.project_id}")

        project.validate()
        project.update_completion_rate()

        result = self.repository.save(project)
        logger.debug(f"Project save result: {result}")

        return result

    def load_project(self, project_id: str) -> Project:
        """
        Load a project by ID.

        Args:
            project_id: The unique identifier of the project

        Returns:
            The loaded project

        Raises:
            ProjectNotFoundException: If project doesn't exist
            ProjectLoadError: If load operation fails
        """
        logger.info(f"Loading project: {project_id}")

        project = self.repository.load(project_id)

        if project is None:
            error_msg = ERROR_PROJECT_NOT_FOUND.format(project_id)
            logger.error(error_msg)
            raise ProjectNotFoundException(error_msg)

        logger.debug(f"Project loaded successfully: {project.project_name}")
        return project

    def delete_project(self, project_id: str) -> bool:
        """
        Delete a project by ID.

        Args:
            project_id: The unique identifier of the project

        Returns:
            True if successful, False if project doesn't exist
        """
        logger.info(f"Deleting project: {project_id}")
        result = self.repository.delete(project_id)
        logger.debug(f"Project delete result: {result}")
        return result

    def list_all_projects(self) -> Dict[str, str]:
        """
        List all available projects.

        Returns:
            Dictionary mapping project IDs to project names
        """
        logger.debug("Listing all projects")
        projects = self.repository.list_all()
        logger.info(f"Found {len(projects)} projects")
        return projects

    def project_exists(self, project_id: str) -> bool:
        """
        Check if a project exists.

        Args:
            project_id: The unique identifier of the project

        Returns:
            True if the project exists, False otherwise
        """
        exists = self.repository.exists(project_id)
        logger.debug(f"Project exists check for {project_id}: {exists}")
        return exists

    def update_project_metadata(
        self,
        project: Project,
        project_name: Optional[str] = None,
        genre: Optional[str] = None
    ) -> Project:
        """
        Update project metadata.

        Args:
            project: The project to update
            project_name: New project name (optional)
            genre: New genre (optional)

        Returns:
            The updated project

        Raises:
            ProjectValidationError: If validation fails
        """
        logger.info(f"Updating metadata for project: {project.project_id}")

        project.update_metadata(project_name=project_name, genre=genre)
        project.validate()

        logger.debug("Project metadata updated and validated")
        return project

    def update_project_element(
        self,
        project: Project,
        element_name: str,
        description: str
    ) -> Project:
        """
        Update a specific world element in the project.

        Args:
            project: The project to update
            element_name: Name of the element to update
            description: New description for the element

        Returns:
            The updated project

        Raises:
            ProjectValidationError: If validation fails
        """
        logger.info(f"Updating element '{element_name}' for project: {project.project_id}")

        project.update_element(element_name, description)
        project.update_completion_rate()

        logger.debug(f"Element updated, new completion rate: {project.completion_rate:.1%}")
        return project

    def get_project_completion_rate(self, project: Project) -> float:
        """
        Get the current completion rate of a project.

        Args:
            project: The project to check

        Returns:
            Completion rate as a float between 0.0 and 1.0
        """
        project.update_completion_rate()
        logger.debug(f"Completion rate for {project.project_id}: {project.completion_rate:.1%}")
        return project.completion_rate

    @staticmethod
    def list_templates() -> Dict[str, Dict[str, str]]:
        """
        List all available project templates.

        Returns:
            Dictionary mapping template IDs to template metadata
        """
        logger.debug(f"Listing {len(TEMPLATES)} available templates")
        return TEMPLATES

    def create_project_from_template(self, template_id: str) -> Project:
        """
        Create a new project from a template.

        Args:
            template_id: ID of the template to use (e.g., 'fantasy', 'scifi')

        Returns:
            The newly created project based on the template

        Raises:
            ProjectLoadError: If template file cannot be loaded
        """
        logger.info(f"Creating project from template: {template_id}")

        if template_id not in TEMPLATES:
            error_msg = f"Template '{template_id}' not found. Available: {list(TEMPLATES.keys())}"
            logger.error(error_msg)
            raise ProjectLoadError(error_msg)

        template_file = TEMPLATES[template_id]["file"]
        template_path = os.path.join(TEMPLATE_DIR, template_file)

        if not os.path.exists(template_path):
            error_msg = f"Template file not found: {template_path}"
            logger.error(error_msg)
            raise ProjectLoadError(error_msg)

        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_data = json.load(f)

            # Create project from template data
            # Note: from_dict will generate a new project_id and timestamps
            project = Project.from_dict(template_data)

            logger.info(f"Project created from template '{template_id}': {project.project_name}")
            logger.debug(f"New project ID: {project.project_id}")

            return project

        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON in template file {template_path}: {str(e)}"
            logger.error(error_msg)
            raise ProjectLoadError(error_msg)
        except Exception as e:
            error_msg = f"Error loading template {template_id}: {str(e)}"
            logger.error(error_msg)
            raise ProjectLoadError(error_msg)
