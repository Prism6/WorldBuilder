"""
Repository layer for data access abstraction.
"""

from .project_repository import ProjectRepository
from .json_project_repository import JsonProjectRepository

__all__ = ['ProjectRepository', 'JsonProjectRepository']
