"""
Abstract repository interface for project persistence.
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional
from models.project import Project


class ProjectRepository(ABC):
    """Abstract base class for project data persistence."""

    @abstractmethod
    def save(self, project: Project) -> bool:
        """
        Save a project.

        Args:
            project: The project to save.

        Returns:
            True if successful, False otherwise.

        Raises:
            ProjectSaveError: If the project cannot be saved.
        """
        pass

    @abstractmethod
    def load(self, project_id: str) -> Optional[Project]:
        """
        Load a project by ID.

        Args:
            project_id: The unique identifier of the project.

        Returns:
            The loaded project, or None if not found.

        Raises:
            ProjectLoadError: If the project cannot be loaded.
        """
        pass

    @abstractmethod
    def delete(self, project_id: str) -> bool:
        """
        Delete a project by ID.

        Args:
            project_id: The unique identifier of the project.

        Returns:
            True if successful, False otherwise.
        """
        pass

    @abstractmethod
    def list_all(self) -> Dict[str, str]:
        """
        List all available projects.

        Returns:
            Dictionary mapping project IDs to project names.
        """
        pass

    @abstractmethod
    def exists(self, project_id: str) -> bool:
        """
        Check if a project exists.

        Args:
            project_id: The unique identifier of the project.

        Returns:
            True if the project exists, False otherwise.
        """
        pass
