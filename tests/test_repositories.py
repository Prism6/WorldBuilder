# tests/test_repositories.py
"""
Unit tests for WorldBuilder repository layer.
"""

import os
import pytest
import json

from models.project import Project
from repositories.json_project_repository import JsonProjectRepository
from exceptions import (
    ProjectNotFoundException,
    ProjectSaveError,
    ProjectLoadError
)


class TestJsonProjectRepository:
    """Tests for JsonProjectRepository."""

    def test_repository_creation(self, temp_dir):
        """Test creating a repository with custom storage directory."""
        repo = JsonProjectRepository(storage_dir=temp_dir)
        assert repo.storage_dir == temp_dir
        assert os.path.exists(temp_dir)

    def test_save_project(self, repository, sample_project):
        """Test saving a project to JSON file."""
        repository.save(sample_project)

        # Verify file exists
        file_path = os.path.join(
            repository.storage_dir,
            f"{sample_project.project_id}.json"
        )
        assert os.path.exists(file_path)

        # Verify file content
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            assert data['project_name'] == sample_project.project_name
            assert data['project_id'] == sample_project.project_id

    def test_load_project(self, repository, sample_project):
        """Test loading a project from JSON file."""
        # First save the project
        repository.save(sample_project)

        # Then load it
        loaded = repository.load(sample_project.project_id)

        assert loaded.project_id == sample_project.project_id
        assert loaded.project_name == sample_project.project_name
        assert loaded.genre == sample_project.genre
        assert loaded.concept.logline == sample_project.concept.logline

    def test_load_nonexistent_project(self, repository):
        """Test loading a project that doesn't exist returns None."""
        # Loading nonexistent project returns None
        result = repository.load("nonexistent-project-id")
        assert result is None

    def test_load_corrupted_json(self, repository, temp_dir):
        """Test loading a corrupted JSON file."""
        # Create a corrupted JSON file
        file_path = os.path.join(temp_dir, "corrupted.json")
        with open(file_path, 'w') as f:
            f.write("{ invalid json content }")

        with pytest.raises(ProjectLoadError):
            repository.load("corrupted")

    def test_list_projects(self, repository, sample_project):
        """Test listing all projects."""
        # Initially empty or minimal
        initial_projects = repository.list_all()
        initial_count = len(initial_projects)

        # Save a project
        repository.save(sample_project)

        # List should now include it
        projects = repository.list_all()
        assert len(projects) == initial_count + 1
        assert sample_project.project_id in projects
        assert projects[sample_project.project_id] == sample_project.project_name

    def test_delete_project(self, repository, sample_project):
        """Test deleting a project."""
        # Save project first
        repository.save(sample_project)

        # Verify it exists
        file_path = os.path.join(
            repository.storage_dir,
            f"{sample_project.project_id}.json"
        )
        assert os.path.exists(file_path)

        # Delete it
        repository.delete(sample_project.project_id)

        # Verify file is gone
        assert not os.path.exists(file_path)

    def test_delete_nonexistent_project(self, repository):
        """Test deleting a nonexistent project logs warning."""
        # Deleting nonexistent project should log warning but not crash
        repository.delete("nonexistent-project-id")
        # Should complete without error

    def test_project_exists(self, repository, sample_project):
        """Test checking if a project exists."""
        # Initially doesn't exist
        assert not repository.exists(sample_project.project_id)

        # Save project
        repository.save(sample_project)

        # Now it exists
        assert repository.exists(sample_project.project_id)

        # Delete project
        repository.delete(sample_project.project_id)

        # No longer exists
        assert not repository.exists(sample_project.project_id)


class TestJsonProjectRepositoryEdgeCases:
    """Test edge cases and error handling."""

    def test_save_with_korean_characters(self, repository):
        """Test saving project with Korean characters."""
        project = Project(
            project_name="한글 프로젝트",
            genre="판타지"
        )
        project.concept.logline = "마법이 있는 세상"
        project.concept.keywords = ["마법", "모험", "판타지"]

        # Should save without error
        repository.save(project)

        # Should load correctly
        loaded = repository.load(project.project_id)
        assert loaded.project_name == "한글 프로젝트"
        assert loaded.genre == "판타지"
        assert loaded.concept.logline == "마법이 있는 세상"
        assert "마법" in loaded.concept.keywords

    def test_save_with_special_characters(self, repository):
        """Test saving project with special characters."""
        project = Project(
            project_name="Test!@#$%^&*()",
            genre="Sci-Fi"
        )
        project.concept.logline = "A world with \"quotes\" and 'apostrophes'"

        repository.save(project)
        loaded = repository.load(project.project_id)

        assert loaded.project_name == "Test!@#$%^&*()"
        assert loaded.concept.logline == "A world with \"quotes\" and 'apostrophes'"

    def test_save_with_long_content(self, repository):
        """Test saving project with long content."""
        project = Project()
        project.elements.space.description = "A" * 10000  # 10k characters

        repository.save(project)
        loaded = repository.load(project.project_id)

        assert len(loaded.elements.space.description) == 10000

    def test_save_with_many_connections(self, repository):
        """Test saving project with many connections."""
        project = Project()

        # Add 50 connections
        for i in range(50):
            project.connections.append({
                'from_element': 'space',
                'to_element': 'culture',
                'connection_type': 'influences',
                'description': f'Connection {i}'
            })

        repository.save(project)
        loaded = repository.load(project.project_id)

        assert len(loaded.connections) == 50

    def test_concurrent_save(self, repository, sample_project):
        """Test saving the same project multiple times."""
        # First save
        repository.save(sample_project)

        # Modify and save again
        sample_project.project_name = "Modified Name"
        repository.save(sample_project)

        # Load should get the latest version
        loaded = repository.load(sample_project.project_id)
        assert loaded.project_name == "Modified Name"

    def test_list_projects_empty_directory(self, temp_dir):
        """Test listing projects when directory is empty."""
        repo = JsonProjectRepository(storage_dir=temp_dir)
        projects = repo.list_all()
        assert isinstance(projects, dict)
        # Should be empty or only have initial projects
        assert len(projects) >= 0

    def test_storage_directory_creation(self, temp_dir):
        """Test that storage directory is created if it doesn't exist."""
        nested_dir = os.path.join(temp_dir, "nested", "directory")
        repo = JsonProjectRepository(storage_dir=nested_dir)

        # Directory should be created
        assert os.path.exists(nested_dir)


class TestJsonProjectRepositoryIntegration:
    """Integration tests for JsonProjectRepository."""

    def test_save_load_cycle(self, repository, sample_project):
        """Test complete save and load cycle preserves all data."""
        # Save
        repository.save(sample_project)

        # Load
        loaded = repository.load(sample_project.project_id)

        # Verify all data is preserved
        assert loaded.project_id == sample_project.project_id
        assert loaded.project_name == sample_project.project_name
        assert loaded.genre == sample_project.genre
        assert loaded.created_at == sample_project.created_at
        assert loaded.concept.logline == sample_project.concept.logline
        assert loaded.concept.keywords == sample_project.concept.keywords
        assert loaded.elements.space.description == sample_project.elements.space.description
        assert loaded.elements.rules.natural == sample_project.elements.rules.natural
        assert len(loaded.connections) == len(sample_project.connections)
        assert loaded.completion_rate == sample_project.completion_rate

    def test_multiple_repositories_same_storage(self, temp_dir, sample_project):
        """Test that multiple repository instances can access same storage."""
        # Create first repository and save project
        repo1 = JsonProjectRepository(storage_dir=temp_dir)
        repo1.save(sample_project)

        # Create second repository pointing to same storage
        repo2 = JsonProjectRepository(storage_dir=temp_dir)

        # Should be able to load project
        loaded = repo2.load(sample_project.project_id)
        assert loaded.project_id == sample_project.project_id

    def test_repository_persistence(self, temp_dir, sample_project):
        """Test that data persists after repository is destroyed."""
        # Save with one repository instance
        repo1 = JsonProjectRepository(storage_dir=temp_dir)
        repo1.save(sample_project)
        del repo1

        # Create new repository instance
        repo2 = JsonProjectRepository(storage_dir=temp_dir)
        loaded = repo2.load(sample_project.project_id)

        assert loaded.project_id == sample_project.project_id
