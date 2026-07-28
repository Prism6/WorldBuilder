# tests/conftest.py
"""
Pytest configuration and fixtures for WorldBuilder tests.
"""

import os
import tempfile
import shutil
from typing import Generator
import pytest

from models.project import Project, Concept, WorldElements, Element, Rules, Connection
from services.project_manager import ProjectManager
from repositories.json_project_repository import JsonProjectRepository


@pytest.fixture
def temp_dir() -> Generator[str, None, None]:
    """Create a temporary directory for testing."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    # Cleanup
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def sample_project() -> Project:
    """Create a sample project for testing."""
    project = Project(
        project_name="Test World",
        genre="Fantasy"
    )

    # Add some sample data
    project.concept.logline = "A world of magic and mystery"
    project.concept.keywords = ["magic", "fantasy", "adventure"]

    # Add some element descriptions
    project.elements.space.description = "A vast continent with mountains and seas"
    project.elements.time.description = "Medieval era with magic"
    project.elements.creatures.description = "Humans, elves, and dragons"

    # Add rules
    project.elements.rules.natural = ["Magic follows the law of conservation"]
    project.elements.rules.social = ["Kings rule by divine right"]
    project.elements.rules.religious = ["The old gods still watch"]

    # Add connections
    project.connections = [
        Connection(
            from_element='space',
            to_element='culture',
            connection_type='influences',
            description='Mountain terrain shapes isolated cultures'
        ),
        Connection(
            from_element='economy',
            to_element='politics',
            connection_type='depends_on',
            description='Economic power determines political influence'
        ),
    ]

    # Update completion rate
    project.update_completion_rate()

    return project


@pytest.fixture
def empty_project() -> Project:
    """Create an empty project for testing."""
    return Project()


@pytest.fixture
def repository(temp_dir: str) -> JsonProjectRepository:
    """Create a repository with temporary storage."""
    return JsonProjectRepository(storage_dir=temp_dir)


@pytest.fixture
def project_manager(repository: JsonProjectRepository) -> ProjectManager:
    """Create a project manager with temporary repository."""
    return ProjectManager(repository=repository)


@pytest.fixture
def sample_concept() -> Concept:
    """Create a sample concept for testing."""
    return Concept(
        logline="A world where magic is powered by dreams",
        keywords=["dreams", "magic", "fantasy", "surreal"]
    )


@pytest.fixture
def sample_elements() -> WorldElements:
    """Create sample world elements for testing."""
    elements = WorldElements()
    elements.space.description = "Floating islands in the sky"
    elements.time.description = "Eternal twilight"
    elements.creatures.description = "Dream beings and humans"
    return elements


@pytest.fixture
def sample_rules() -> Rules:
    """Create sample rules for testing."""
    return Rules(
        natural=["Dreams manifest as physical objects", "Time flows differently in dream realm"],
        social=["Dreamers are honored in society", "Nightmare magic is forbidden"],
        religious=["The Dream God created the world", "Sleep is sacred"]
    )
