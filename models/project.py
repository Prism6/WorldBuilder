# models/project.py
"""
Data models for WorldBuilder projects.
"""

import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Dict, Any, Optional
from exceptions import ProjectValidationError
from constants import (
    DEFAULT_PROJECT_NAME,
    DEFAULT_GENRE,
    UNNAMED_PROJECT,
    TOTAL_ELEMENTS,
    ELEMENT_NAMES,
    MIN_COMPLETION_RATE,
    MAX_COMPLETION_RATE,
    ERROR_EMPTY_PROJECT_NAME,
    ERROR_EMPTY_PROJECT_ID,
    ERROR_EMPTY_GENRE,
    ERROR_INVALID_COMPLETION_RATE,
    ERROR_INVALID_ELEMENT_NAME,
    ERROR_EMPTY_DATA,
    ERROR_FAILED_TO_CREATE
)
from utils.logger import get_logger

logger = get_logger(__name__)


# 각 12요소에 대한 데이터 구조
@dataclass
class Element:
    description: str = ""
    # 필요에 따라 각 요소별로 필드를 추가할 수 있음
    # 예: space 요소의 landmarks
    # landmarks: List[str] = field(default_factory=list)


# 9. 규칙
@dataclass
class Rules:
    natural: List[str] = field(default_factory=list)
    social: List[str] = field(default_factory=list)
    religious: List[str] = field(default_factory=list)


# 프로젝트의 모든 요소를 담는 컨테이너
@dataclass
class WorldElements:
    space: Element = field(default_factory=Element)
    time: Element = field(default_factory=Element)
    creatures: Element = field(default_factory=Element)
    nature: Element = field(default_factory=Element)
    culture: Element = field(default_factory=Element)
    language: Element = field(default_factory=Element)
    mythology: Element = field(default_factory=Element)
    philosophy: Element = field(default_factory=Element)
    rules: Rules = field(default_factory=Rules)  # Rules는 별도 dataclass
    economy: Element = field(default_factory=Element)
    politics: Element = field(default_factory=Element)
    energy: Element = field(default_factory=Element)


# 세계관 컨셉
@dataclass
class Concept:
    logline: str = ""
    keywords: List[str] = field(default_factory=list)


# 메인 프로젝트 데이터 클래스
@dataclass
class Project:
    """
    Main project data model representing a worldbuilding project.
    """
    project_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    project_name: str = DEFAULT_PROJECT_NAME
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    genre: str = DEFAULT_GENRE

    concept: Concept = field(default_factory=Concept)
    elements: WorldElements = field(default_factory=WorldElements)

    # 그 외 메타 데이터
    connections: List[Dict[str, Any]] = field(default_factory=list)
    notes: str = ""
    completion_rate: float = 0.0

    def _validate_string_field(self, value: Optional[str], field_name: str, error_msg: str) -> None:
        """
        Validate a string field is not empty.

        Args:
            value: The value to validate
            field_name: Name of the field being validated
            error_msg: Error message to raise if validation fails

        Raises:
            ProjectValidationError: If validation fails
        """
        if not value or not value.strip():
            logger.warning(f"Validation failed for {field_name}: empty value")
            raise ProjectValidationError(error_msg)

    def _validate_range(self, value: float, min_val: float, max_val: float, error_msg: str) -> None:
        """
        Validate a numeric value is within range.

        Args:
            value: The value to validate
            min_val: Minimum allowed value
            max_val: Maximum allowed value
            error_msg: Error message to raise if validation fails

        Raises:
            ProjectValidationError: If validation fails
        """
        if value < min_val or value > max_val:
            logger.warning(f"Validation failed: {value} not in range [{min_val}, {max_val}]")
            raise ProjectValidationError(error_msg)

    def validate(self) -> None:
        """
        Validate all project data fields.

        Raises:
            ProjectValidationError: If any validation check fails.
        """
        logger.debug(f"Validating project: {self.project_id}")

        self._validate_string_field(self.project_name, "project_name", ERROR_EMPTY_PROJECT_NAME)
        self._validate_string_field(self.project_id, "project_id", ERROR_EMPTY_PROJECT_ID)
        self._validate_string_field(self.genre, "genre", ERROR_EMPTY_GENRE)
        self._validate_range(
            self.completion_rate,
            MIN_COMPLETION_RATE,
            MAX_COMPLETION_RATE,
            ERROR_INVALID_COMPLETION_RATE
        )

        logger.debug(f"Project validation passed: {self.project_id}")

    def _update_timestamp(self) -> None:
        """Update the project's last updated timestamp."""
        self.updated_at = datetime.now().isoformat()

    def update_metadata(
        self,
        project_name: Optional[str] = None,
        genre: Optional[str] = None
    ) -> None:
        """
        Update project metadata fields.

        Args:
            project_name: New project name (optional)
            genre: New genre (optional)

        Raises:
            ProjectValidationError: If validation fails.
        """
        logger.debug(f"Updating metadata for project: {self.project_id}")

        if project_name is not None:
            self._validate_string_field(project_name, "project_name", ERROR_EMPTY_PROJECT_NAME)
            self.project_name = project_name
            logger.info(f"Project name updated to: {project_name}")

        if genre is not None:
            self._validate_string_field(genre, "genre", ERROR_EMPTY_GENRE)
            self.genre = genre
            logger.info(f"Genre updated to: {genre}")

        self._update_timestamp()

    def update_logline(self, logline: str) -> None:
        """Update project logline."""
        self.concept.logline = logline
        self._update_timestamp()

    def update_keywords(self, keywords: List[str]) -> None:
        """Update project keywords."""
        self.concept.keywords = keywords
        self._update_timestamp()

    def update_rules(
        self,
        natural: List[str],
        social: List[str],
        religious: List[str]
    ) -> None:
        """Update rules element."""
        self.elements.rules.natural = natural
        self.elements.rules.social = social
        self.elements.rules.religious = religious
        self._update_timestamp()

    def add_connection(self, connection: Dict[str, Any]) -> None:
        """Append a new connection and update timestamp."""
        self.connections.append(connection)
        self._update_timestamp()

    def remove_connection(self, index: int) -> None:
        """Remove a connection by index and update timestamp."""
        self.connections.pop(index)
        self._update_timestamp()

    def update_element(self, element_name: str, description: str) -> None:
        """
        Update a specific world element.

        Args:
            element_name: Name of the element to update (e.g., 'space', 'time')
            description: New description for the element

        Raises:
            ProjectValidationError: If element name is invalid.
        """
        logger.debug(f"Updating element '{element_name}' for project: {self.project_id}")

        if not hasattr(self.elements, element_name):
            error_msg = ERROR_INVALID_ELEMENT_NAME.format(element_name)
            logger.warning(error_msg)
            raise ProjectValidationError(error_msg)

        element = getattr(self.elements, element_name)
        if isinstance(element, Element):
            element.description = description
            logger.info(f"Element '{element_name}' updated")
        elif isinstance(element, Rules):
            # For Rules, you might want a different update method
            logger.warning(f"Rules element requires special handling, skipping: {element_name}")

        self._update_timestamp()

    def _count_filled_elements(self) -> int:
        """
        Count the number of filled world elements.

        Returns:
            Number of elements with content
        """
        filled_count = 0

        # Check regular elements
        for element_name in ELEMENT_NAMES:
            element = getattr(self.elements, element_name)
            if element.description and element.description.strip():
                filled_count += 1

        # Check rules separately
        if (self.elements.rules.natural or
                self.elements.rules.social or
                self.elements.rules.religious):
            filled_count += 1

        return filled_count

    def update_completion_rate(self) -> None:
        """
        Calculate and update completion rate based on filled elements.
        Completion rate is a value between 0.0 and 1.0.
        """
        filled_elements = self._count_filled_elements()
        self.completion_rate = filled_elements / TOTAL_ELEMENTS

        logger.debug(
            f"Completion rate updated: {filled_elements}/{TOTAL_ELEMENTS} "
            f"({self.completion_rate:.1%})"
        )

        self._update_timestamp()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert dataclass to dictionary (for JSON storage).
        Uses dataclasses.asdict for automatic conversion.

        Returns:
            Dictionary representation of the project.
        """
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Project':
        """
        Create a Project instance from a dictionary (for JSON loading).

        Args:
            data: Dictionary containing project data

        Returns:
            Project instance

        Raises:
            ProjectValidationError: If data is invalid or missing required fields
        """
        if not data:
            logger.error("Attempted to create project from empty data")
            raise ProjectValidationError(ERROR_EMPTY_DATA)

        try:
            logger.debug("Creating project from dictionary data")

            concept_data = data.get("concept", {})
            elements_data = data.get("elements", {})

            # Load each element dynamically
            element_kwargs: Dict[str, Any] = {}
            for element_name in ELEMENT_NAMES:
                element_kwargs[element_name] = Element(**elements_data.get(element_name, {}))

            # Load rules separately
            element_kwargs['rules'] = Rules(**elements_data.get("rules", {}))

            elements = WorldElements(**element_kwargs)

            project = cls(
                project_id=data.get("project_id", str(uuid.uuid4())),
                project_name=data.get("project_name", UNNAMED_PROJECT),
                created_at=data.get("created_at", datetime.now().isoformat()),
                updated_at=data.get("updated_at", datetime.now().isoformat()),
                genre=data.get("genre", DEFAULT_GENRE),
                concept=Concept(**concept_data),
                elements=elements,
                connections=data.get("connections", []),
                notes=data.get("notes", ""),
                completion_rate=data.get("completion_rate", 0.0)
            )

            # Validate the created project
            project.validate()

            logger.info(f"Successfully created project from data: {project.project_id}")
            return project

        except ProjectValidationError:
            raise
        except Exception as e:
            error_msg = ERROR_FAILED_TO_CREATE.format(str(e))
            logger.error(error_msg)
            raise ProjectValidationError(error_msg) from e
