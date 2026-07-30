# tests/test_services.py
"""
Unit tests for WorldBuilder service layer.
"""

import pytest
from typing import Optional

from models.project import Project
from services.project_manager import ProjectManager
from repositories.json_project_repository import JsonProjectRepository
from exceptions import (
    ProjectNotFoundException,
    ProjectValidationError,
    ProjectSaveError
)


class TestProjectManager:
    """Tests for ProjectManager service."""

    def test_create_new_project(self, project_manager):
        """Test creating a new project."""
        project = project_manager.create_new_project()

        assert project is not None
        assert isinstance(project, Project)
        assert project.project_name == "새로운 세계"
        assert project.genre == "SF/판타지"
        assert project.completion_rate == 0.0

    def test_create_new_project_with_name(self, project_manager):
        """Test creating a new project with custom name."""
        project = project_manager.create_new_project(
            project_name="My Fantasy World"
        )

        assert project.project_name == "My Fantasy World"
        assert project.genre == "SF/판타지"

    def test_create_new_project_with_genre(self, project_manager):
        """Test creating a new project with custom genre."""
        project = project_manager.create_new_project(
            project_name="Sci-Fi Adventure",
            genre="Science Fiction"
        )

        assert project.project_name == "Sci-Fi Adventure"
        assert project.genre == "Science Fiction"

    def test_save_project(self, project_manager, sample_project):
        """Test saving a project."""
        # Save should not raise error
        project_manager.save_project(sample_project)

        # Verify project was saved
        loaded = project_manager.load_project(sample_project.project_id)
        assert loaded.project_name == sample_project.project_name

    def test_save_invalid_project(self, project_manager):
        """Test saving an invalid project raises error."""
        invalid_project = Project()
        invalid_project.project_id = ""  # Invalid

        with pytest.raises(ProjectValidationError):
            project_manager.save_project(invalid_project)

    def test_load_project(self, project_manager, sample_project):
        """Test loading a saved project."""
        # First save the project
        project_manager.save_project(sample_project)

        # Then load it
        loaded = project_manager.load_project(sample_project.project_id)

        assert loaded.project_id == sample_project.project_id
        assert loaded.project_name == sample_project.project_name
        assert loaded.genre == sample_project.genre

    def test_load_nonexistent_project(self, project_manager):
        """Test loading a project that doesn't exist."""
        with pytest.raises(ProjectNotFoundException):
            project_manager.load_project("nonexistent-id")

    def test_list_projects(self, project_manager, sample_project):
        """Test listing all projects."""
        # Initially empty
        projects = project_manager.list_all_projects()
        initial_count = len(projects)

        # Save a project
        project_manager.save_project(sample_project)

        # List should now include it
        projects = project_manager.list_all_projects()
        assert len(projects) == initial_count + 1
        assert sample_project.project_id in projects

    def test_delete_project(self, project_manager, sample_project):
        """Test deleting a project."""
        # Save project first
        project_manager.save_project(sample_project)

        # Verify it exists
        projects = project_manager.list_all_projects()
        assert sample_project.project_id in projects

        # Delete it
        project_manager.delete_project(sample_project.project_id)

        # Verify it's gone
        projects = project_manager.list_all_projects()
        assert sample_project.project_id not in projects

    def test_delete_nonexistent_project(self, project_manager):
        """Test deleting a nonexistent project logs warning but doesn't crash."""
        # Deleting nonexistent project should not raise, just log warning
        project_manager.delete_project("nonexistent-id")
        # Should complete without error

    def test_update_project_metadata(self, project_manager, sample_project):
        """Test updating project metadata."""
        project_manager.update_project_metadata(
            sample_project,
            project_name="Updated Name",
            genre="Updated Genre"
        )

        assert sample_project.project_name == "Updated Name"
        assert sample_project.genre == "Updated Genre"

    def test_update_project_metadata_name_only(self, project_manager, sample_project):
        """Test updating only project name."""
        original_genre = sample_project.genre

        project_manager.update_project_metadata(
            sample_project,
            project_name="New Name",
            genre=None
        )

        assert sample_project.project_name == "New Name"
        assert sample_project.genre == original_genre

    def test_update_project_metadata_genre_only(self, project_manager, sample_project):
        """Test updating only project genre."""
        original_name = sample_project.project_name

        project_manager.update_project_metadata(
            sample_project,
            project_name=None,
            genre="New Genre"
        )

        assert sample_project.project_name == original_name
        assert sample_project.genre == "New Genre"

    def test_update_project_metadata_empty_values(self, project_manager, sample_project):
        """Test that empty strings are rejected."""
        with pytest.raises(ProjectValidationError):
            project_manager.update_project_metadata(
                sample_project,
                project_name="",
                genre=None
            )

        with pytest.raises(ProjectValidationError):
            project_manager.update_project_metadata(
                sample_project,
                project_name=None,
                genre=""
            )


class TestProjectManagerNewMethods:
    """Tests for service methods added in WB05 and caching added in WB06."""

    def test_update_project_logline(self, project_manager, sample_project):
        """Test update_project_logline delegates to model and returns project."""
        result = project_manager.update_project_logline(
            sample_project, "A new logline"
        )

        assert result is sample_project
        assert sample_project.concept.logline == "A new logline"

    def test_update_project_logline_empty(self, project_manager, sample_project):
        """Test update_project_logline accepts empty string."""
        result = project_manager.update_project_logline(sample_project, "")
        assert result.concept.logline == ""

    def test_update_project_keywords(self, project_manager, sample_project):
        """Test update_project_keywords delegates to model and returns project."""
        new_kws = ["dragon", "crystal", "sky"]
        result = project_manager.update_project_keywords(sample_project, new_kws)

        assert result is sample_project
        assert sample_project.concept.keywords == new_kws

    def test_update_project_keywords_empty(self, project_manager, sample_project):
        """Test update_project_keywords accepts empty list."""
        result = project_manager.update_project_keywords(sample_project, [])
        assert result.concept.keywords == []

    def test_update_project_rules_method(self, project_manager, sample_project):
        """Test update_project_rules delegates + recalculates completion rate."""
        initial_rate = sample_project.completion_rate
        # Clear rules so completion rate changes
        sample_project.elements.rules.natural = []
        sample_project.elements.rules.social = []
        sample_project.elements.rules.religious = []
        sample_project.update_completion_rate()
        rate_without_rules = sample_project.completion_rate

        result = project_manager.update_project_rules(
            sample_project,
            natural=["Gravity"],
            social=["Elders rule"],
            religious=["Sun worship"]
        )

        assert result is sample_project
        assert sample_project.elements.rules.natural == ["Gravity"]
        assert sample_project.elements.rules.social == ["Elders rule"]
        assert sample_project.elements.rules.religious == ["Sun worship"]
        # Completion rate should increase after rules are filled
        assert sample_project.completion_rate > rate_without_rules
        _ = initial_rate  # referenced to suppress unused warning

    def test_project_list_cache_hit(self, project_manager, sample_project):
        """Test list_all_projects returns cached result on second call."""
        project_manager.save_project(sample_project)

        first = project_manager.list_all_projects()
        # Force cache hit by setting timestamp to recent value
        import time
        project_manager._cache_timestamp = time.time()
        second = project_manager.list_all_projects()

        assert first == second
        assert sample_project.project_id in second

    def test_project_list_cache_invalidated_on_save(self, project_manager):
        """Test that saving a project invalidates the cache."""
        import time
        # Prime the cache
        project_manager.list_all_projects()
        project_manager._cache_timestamp = time.time()  # force cache fresh

        new_project = project_manager.create_new_project("Cache Test")
        project_manager.save_project(new_project)

        # Cache timestamp should be zeroed out
        assert project_manager._cache_timestamp == 0.0

    def test_project_list_cache_invalidated_on_delete(self, project_manager, sample_project):
        """Test that deleting a project invalidates the cache."""
        import time
        project_manager.save_project(sample_project)
        project_manager.list_all_projects()
        project_manager._cache_timestamp = time.time()

        project_manager.delete_project(sample_project.project_id)

        assert project_manager._cache_timestamp == 0.0


class TestProjectManagerIntegration:
    """Integration tests for ProjectManager."""

    def test_full_project_lifecycle(self, project_manager):
        """Test complete project lifecycle: create, save, load, update, delete."""
        # 1. Create project
        project = project_manager.create_new_project(
            project_name="Lifecycle Test",
            genre="Test Genre"
        )
        project_id = project.project_id

        # 2. Modify project
        project.concept.logline = "Test logline"
        project.concept.keywords = ["test", "lifecycle"]
        project.update_element("space", "Test space description")
        project.update_completion_rate()

        # 3. Save project
        project_manager.save_project(project)

        # 4. Load project
        loaded = project_manager.load_project(project_id)
        assert loaded.project_name == "Lifecycle Test"
        assert loaded.concept.logline == "Test logline"
        assert len(loaded.concept.keywords) == 2

        # 5. Update metadata
        project_manager.update_project_metadata(
            loaded,
            project_name="Updated Name",
            genre="Updated Genre"
        )

        # 6. Save again
        project_manager.save_project(loaded)

        # 7. Reload and verify
        reloaded = project_manager.load_project(project_id)
        assert reloaded.project_name == "Updated Name"
        assert reloaded.genre == "Updated Genre"

        # 8. Delete project
        project_manager.delete_project(project_id)

        # 9. Verify deletion
        with pytest.raises(ProjectNotFoundException):
            project_manager.load_project(project_id)

    def test_multiple_projects(self, project_manager):
        """Test managing multiple projects simultaneously."""
        # Create multiple projects
        projects = []
        for i in range(3):
            project = project_manager.create_new_project(
                project_name=f"Project {i}",
                genre=f"Genre {i}"
            )
            project_manager.save_project(project)
            projects.append(project)

        # List should contain all projects
        project_list = project_manager.list_all_projects()
        assert len(project_list) >= 3

        for project in projects:
            assert project.project_id in project_list

        # Load each project and verify
        for i, project in enumerate(projects):
            loaded = project_manager.load_project(project.project_id)
            assert loaded.project_name == f"Project {i}"
            assert loaded.genre == f"Genre {i}"

        # Clean up
        for project in projects:
            project_manager.delete_project(project.project_id)
