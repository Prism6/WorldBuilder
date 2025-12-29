"""
Custom exceptions for WorldBuilder application.
"""


class WorldBuilderException(Exception):
    """Base exception for all WorldBuilder errors."""
    pass


class ProjectNotFoundException(WorldBuilderException):
    """Raised when a project cannot be found."""
    pass


class ProjectValidationError(WorldBuilderException):
    """Raised when project data validation fails."""
    pass


class ProjectSaveError(WorldBuilderException):
    """Raised when a project cannot be saved."""
    pass


class ProjectLoadError(WorldBuilderException):
    """Raised when a project cannot be loaded."""
    pass
