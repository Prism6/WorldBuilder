# tests/test_models.py
"""
Unit tests for WorldBuilder data models.
"""

import pytest
from datetime import datetime

from models.project import (
    Project,
    Concept,
    WorldElements,
    Element,
    Rules
)
from exceptions import ProjectValidationError


class TestElement:
    """Tests for Element class."""

    def test_element_creation(self):
        """Test creating an empty element."""
        element = Element()
        assert element.description == ""

    def test_element_with_description(self):
        """Test creating an element with description."""
        element = Element(description="A vast desert landscape")
        assert element.description == "A vast desert landscape"


class TestRules:
    """Tests for Rules class."""

    def test_rules_creation(self):
        """Test creating empty rules."""
        rules = Rules()
        assert rules.natural == []
        assert rules.social == []
        assert rules.religious == []

    def test_rules_with_data(self, sample_rules):
        """Test creating rules with data."""
        assert len(sample_rules.natural) == 2
        assert len(sample_rules.social) == 2
        assert len(sample_rules.religious) == 2
        assert "Dreams manifest as physical objects" in sample_rules.natural


class TestConcept:
    """Tests for Concept class."""

    def test_concept_creation(self):
        """Test creating an empty concept."""
        concept = Concept()
        assert concept.logline == ""
        assert concept.keywords == []

    def test_concept_with_data(self, sample_concept):
        """Test creating concept with data."""
        assert sample_concept.logline == "A world where magic is powered by dreams"
        assert len(sample_concept.keywords) == 4
        assert "magic" in sample_concept.keywords


class TestWorldElements:
    """Tests for WorldElements class."""

    def test_world_elements_creation(self):
        """Test creating empty world elements."""
        elements = WorldElements()
        assert isinstance(elements.space, Element)
        assert isinstance(elements.time, Element)
        assert isinstance(elements.creatures, Element)
        assert isinstance(elements.rules, Rules)

    def test_world_elements_with_data(self, sample_elements):
        """Test world elements with descriptions."""
        assert sample_elements.space.description == "Floating islands in the sky"
        assert sample_elements.time.description == "Eternal twilight"
        assert sample_elements.creatures.description == "Dream beings and humans"


class TestProject:
    """Tests for Project class."""

    def test_project_creation(self):
        """Test creating a new project with defaults."""
        project = Project()
        assert project.project_name == "새로운 세계"
        assert project.genre == "SF/판타지"
        assert project.completion_rate == 0.0
        assert project.connections == []
        assert project.notes == ""

    def test_project_with_custom_data(self):
        """Test creating project with custom data."""
        project = Project(
            project_name="My World",
            genre="Sci-Fi"
        )
        assert project.project_name == "My World"
        assert project.genre == "Sci-Fi"

    def test_project_id_generation(self):
        """Test that project_id is automatically generated."""
        project1 = Project()
        project2 = Project()
        assert project1.project_id != project2.project_id
        assert len(project1.project_id) > 0

    def test_project_timestamps(self):
        """Test that timestamps are created."""
        project = Project()
        assert project.created_at is not None
        assert project.updated_at is not None
        # Timestamps should be valid ISO format
        datetime.fromisoformat(project.created_at)
        datetime.fromisoformat(project.updated_at)

    def test_update_timestamp(self):
        """Test updating project timestamp."""
        project = Project()
        old_timestamp = project.updated_at
        # Small delay to ensure timestamp changes
        import time
        time.sleep(0.01)
        project._update_timestamp()
        assert project.updated_at != old_timestamp

    def test_update_element(self):
        """Test updating an element."""
        project = Project()
        project.update_element("space", "A vast ocean world")
        assert project.elements.space.description == "A vast ocean world"

    def test_update_element_invalid_name(self):
        """Test updating element with invalid name raises error."""
        project = Project()
        with pytest.raises(ProjectValidationError):
            project.update_element("invalid_element", "description")

    def test_completion_rate_calculation(self):
        """Test completion rate calculation."""
        project = Project()
        assert project.completion_rate == 0.0

        # Add one element
        project.update_element("space", "description")
        project.update_completion_rate()
        assert project.completion_rate == pytest.approx(1/12, rel=0.01)

        # Add more elements
        project.update_element("time", "time description")
        project.update_element("creatures", "creatures description")
        project.update_completion_rate()
        assert project.completion_rate == pytest.approx(3/12, rel=0.01)

    def test_rules_element_completion(self):
        """Test that rules element counts as complete if any category has data."""
        project = Project()

        # Empty rules - not complete
        project.update_completion_rate()
        initial_rate = project.completion_rate

        # Add natural rules
        project.elements.rules.natural = ["Gravity exists"]
        project.update_completion_rate()
        assert project.completion_rate > initial_rate

    def test_to_dict(self, sample_project):
        """Test converting project to dictionary."""
        data = sample_project.to_dict()

        assert data['project_name'] == "Test World"
        assert data['genre'] == "Fantasy"
        assert 'project_id' in data
        assert 'created_at' in data
        assert 'updated_at' in data
        assert 'concept' in data
        assert 'elements' in data
        assert 'connections' in data

    def test_from_dict(self, sample_project):
        """Test creating project from dictionary."""
        data = sample_project.to_dict()
        restored_project = Project.from_dict(data)

        assert restored_project.project_name == sample_project.project_name
        assert restored_project.genre == sample_project.genre
        assert restored_project.project_id == sample_project.project_id
        assert restored_project.concept.logline == sample_project.concept.logline
        assert len(restored_project.connections) == len(sample_project.connections)

    def test_from_dict_with_empty_data(self):
        """Test creating project from empty dictionary."""
        with pytest.raises(ProjectValidationError):
            Project.from_dict({})

    def test_from_dict_with_invalid_data(self):
        """Test creating project from invalid dictionary uses defaults."""
        # from_dict with missing required fields should use UNNAMED_PROJECT
        project = Project.from_dict({'invalid_key': 'value'})
        # Should create project with unnamed defaults
        assert project.project_name == "이름 없는 세계"

    def test_validate_method(self):
        """Test project validation."""
        project = Project()
        # Should not raise error
        project.validate()

        # Test with empty project_id
        project.project_id = ""
        with pytest.raises(ProjectValidationError):
            project.validate()

    def test_connections_management(self):
        """Test adding and managing connections."""
        project = Project()
        assert len(project.connections) == 0

        # Add a connection
        project.connections.append({
            'from_element': 'space',
            'to_element': 'culture',
            'connection_type': 'influences',
            'description': 'Test connection'
        })
        assert len(project.connections) == 1

        # Add another connection
        project.connections.append({
            'from_element': 'economy',
            'to_element': 'politics',
            'connection_type': 'depends_on',
            'description': 'Another connection'
        })
        assert len(project.connections) == 2

    def test_sample_project_fixture(self, sample_project):
        """Test that sample_project fixture is properly configured."""
        assert sample_project.project_name == "Test World"
        assert sample_project.genre == "Fantasy"
        assert len(sample_project.concept.keywords) == 3
        assert sample_project.elements.space.description != ""
        assert len(sample_project.connections) == 2
        assert sample_project.completion_rate > 0


class TestProjectIntegration:
    """Integration tests for Project class."""

    def test_full_project_workflow(self):
        """Test complete project creation and modification workflow."""
        # Create project
        project = Project(project_name="Integration Test", genre="Sci-Fi")

        # Add concept
        project.concept.logline = "A future where AI rules"
        project.concept.keywords = ["AI", "future", "technology"]

        # Add elements
        project.update_element("space", "Megacities on Mars")
        project.update_element("time", "Year 2200")
        project.update_element("creatures", "Humans and AI")
        project.update_element("energy", "Fusion power")

        # Add rules
        project.elements.rules.natural = ["Physics still apply"]
        project.elements.rules.social = ["AI have rights"]

        # Add connections
        project.connections.append({
            'from_element': 'energy',
            'to_element': 'economy',
            'connection_type': 'enables',
            'description': 'Fusion power drives economy'
        })

        # Update completion
        project.update_completion_rate()

        # Validate
        project.validate()

        # Convert to dict and back
        data = project.to_dict()
        restored = Project.from_dict(data)

        # Verify all data preserved
        assert restored.project_name == project.project_name
        assert restored.concept.logline == project.concept.logline
        assert restored.elements.space.description == project.elements.space.description
        assert len(restored.connections) == len(project.connections)
        assert restored.completion_rate == project.completion_rate
