"""
JSON-based implementation of ProjectRepository.
"""

import os
from typing import Dict, Optional
from datetime import datetime

from .project_repository import ProjectRepository
from models.project import Project
from utils import json_utils
from utils.logger import get_logger
from exceptions import ProjectSaveError, ProjectLoadError
from constants import (
    JSON_EXTENSION,
    ERROR_SAVE_NONE_PROJECT,
    ERROR_EMPTY_PROJECT_ID_LOAD,
    ERROR_EMPTY_OR_INVALID_DATA,
    ERROR_FAILED_TO_SAVE,
    ERROR_SAVING_PROJECT,
    ERROR_LOADING_PROJECT,
    UNKNOWN_PROJECT_LABEL,
    CORRUPTED_PROJECT_LABEL
)

logger = get_logger(__name__)


class JsonProjectRepository(ProjectRepository):
    """Repository implementation using JSON files for storage."""

    def __init__(self, storage_dir: str = "data/projects"):
        """
        Initialize the repository.

        Args:
            storage_dir: Directory where project JSON files are stored.
        """
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)

    def _get_filepath(self, project_id: str) -> str:
        """
        Get the full file path for a project.

        Args:
            project_id: The project ID

        Returns:
            Full path to the project JSON file
        """
        return os.path.join(self.storage_dir, f"{project_id}{JSON_EXTENSION}")

    def save(self, project: Project) -> bool:
        """
        Save a project to a JSON file.

        Args:
            project: The project to save.

        Returns:
            True if successful.

        Raises:
            ProjectSaveError: If the project cannot be saved.
        """
        if not project:
            logger.error("Attempted to save None project")
            raise ProjectSaveError(ERROR_SAVE_NONE_PROJECT)

        try:
            logger.debug(f"Saving project: {project.project_id}")

            # Update timestamp
            project.updated_at = datetime.now().isoformat()

            filepath = self._get_filepath(project.project_id)
            success = json_utils.save_json(filepath, project.to_dict())

            if not success:
                error_msg = ERROR_FAILED_TO_SAVE.format(project.project_id)
                logger.error(error_msg)
                raise ProjectSaveError(error_msg)

            logger.info(f"Successfully saved project: {project.project_id}")
            return True

        except ProjectSaveError:
            raise
        except Exception as e:
            error_msg = ERROR_SAVING_PROJECT.format(str(e))
            logger.error(error_msg)
            raise ProjectSaveError(error_msg) from e

    def load(self, project_id: str) -> Optional[Project]:
        """
        Load a project from a JSON file.

        Args:
            project_id: The unique identifier of the project.

        Returns:
            The loaded project, or None if not found.

        Raises:
            ProjectLoadError: If the project cannot be loaded.
        """
        if not project_id:
            logger.error("Attempted to load project with empty ID")
            raise ProjectLoadError(ERROR_EMPTY_PROJECT_ID_LOAD)

        try:
            logger.debug(f"Loading project: {project_id}")

            filepath = self._get_filepath(project_id)

            if not os.path.exists(filepath):
                logger.warning(f"Project file not found: {project_id}")
                return None

            data = json_utils.load_json(filepath)

            if not data:
                error_msg = ERROR_EMPTY_OR_INVALID_DATA.format(project_id)
                logger.error(error_msg)
                raise ProjectLoadError(error_msg)

            project = Project.from_dict(data)
            logger.info(f"Successfully loaded project: {project_id}")
            return project

        except ProjectLoadError:
            raise
        except Exception as e:
            error_msg = ERROR_LOADING_PROJECT.format(project_id, str(e))
            logger.error(error_msg)
            raise ProjectLoadError(error_msg) from e

    def delete(self, project_id: str) -> bool:
        """
        Delete a project file.

        Args:
            project_id: The unique identifier of the project.

        Returns:
            True if successful, False if project doesn't exist.
        """
        logger.debug(f"Attempting to delete project: {project_id}")

        filepath = self._get_filepath(project_id)

        if not os.path.exists(filepath):
            logger.warning(f"Cannot delete non-existent project: {project_id}")
            return False

        try:
            os.remove(filepath)
            logger.info(f"Successfully deleted project: {project_id}")
            return True
        except OSError as e:
            logger.error(f"Failed to delete project {project_id}: {str(e)}")
            return False

    def list_all(self) -> Dict[str, str]:
        """
        List all available projects.

        Returns:
            Dictionary mapping project IDs to project names.
        """
        logger.debug(f"Listing all projects in: {self.storage_dir}")

        projects: Dict[str, str] = {}

        if not os.path.exists(self.storage_dir):
            logger.warning(f"Storage directory does not exist: {self.storage_dir}")
            return projects

        for filename in os.listdir(self.storage_dir):
            if filename.endswith(JSON_EXTENSION):
                project_id = filename.replace(JSON_EXTENSION, "")
                filepath = os.path.join(self.storage_dir, filename)

                try:
                    data = json_utils.load_json(filepath)
                    if data and "project_name" in data:
                        projects[project_id] = data["project_name"]
                    else:
                        projects[project_id] = UNKNOWN_PROJECT_LABEL.format(project_id)
                        logger.warning(f"Project missing name field: {project_id}")
                except Exception as e:
                    # Skip corrupted files
                    projects[project_id] = CORRUPTED_PROJECT_LABEL.format(project_id)
                    logger.error(f"Corrupted project file {project_id}: {str(e)}")

        logger.info(f"Found {len(projects)} projects")
        return projects

    def exists(self, project_id: str) -> bool:
        """
        Check if a project exists.

        Args:
            project_id: The unique identifier of the project.

        Returns:
            True if the project exists, False otherwise.
        """
        filepath = self._get_filepath(project_id)
        return os.path.exists(filepath)
