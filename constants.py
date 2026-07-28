"""
Application constants and configuration values.
"""

from typing import Final, Dict, List

# Project defaults
DEFAULT_PROJECT_NAME: Final[str] = "새로운 세계"
DEFAULT_GENRE: Final[str] = "SF/판타지"
UNNAMED_PROJECT: Final[str] = "이름 없는 세계"

# World building elements
TOTAL_ELEMENTS: Final[int] = 12

# Element names - single source of truth
ELEMENT_NAMES: Final[List[str]] = [
    'space',
    'time',
    'creatures',
    'nature',
    'culture',
    'language',
    'mythology',
    'philosophy',
    'economy',
    'politics',
    'energy'
]

# Special element (Rules is handled separately)
RULES_ELEMENT: Final[str] = 'rules'

# All element names including rules
ALL_ELEMENT_NAMES: Final[List[str]] = ELEMENT_NAMES + [RULES_ELEMENT]

# Validation constraints
MIN_COMPLETION_RATE: Final[float] = 0.0
MAX_COMPLETION_RATE: Final[float] = 1.0

# File extensions
JSON_EXTENSION: Final[str] = ".json"

# Storage
DEFAULT_STORAGE_DIR: Final[str] = "data/projects"

# Error messages
ERROR_EMPTY_PROJECT_NAME: Final[str] = "Project name cannot be empty"
ERROR_EMPTY_PROJECT_ID: Final[str] = "Project ID cannot be empty"
ERROR_EMPTY_GENRE: Final[str] = "Genre cannot be empty"
ERROR_INVALID_COMPLETION_RATE: Final[str] = "Completion rate must be between 0.0 and 1.0"
ERROR_INVALID_ELEMENT_NAME: Final[str] = "Invalid element name: {}"
ERROR_EMPTY_DATA: Final[str] = "Cannot create project from empty data"
ERROR_SAVE_NONE_PROJECT: Final[str] = "Cannot save None project"
ERROR_EMPTY_PROJECT_ID_LOAD: Final[str] = "Project ID cannot be empty"
ERROR_EMPTY_OR_INVALID_DATA: Final[str] = "Empty or invalid data for project {}"
ERROR_FAILED_TO_SAVE: Final[str] = "Failed to save project {}"
ERROR_SAVING_PROJECT: Final[str] = "Error saving project: {}"
ERROR_LOADING_PROJECT: Final[str] = "Error loading project {}: {}"
ERROR_PROJECT_NOT_FOUND: Final[str] = "Project with ID {} not found"
ERROR_FAILED_TO_CREATE: Final[str] = "Failed to create project from data: {}"

# Project status labels
UNKNOWN_PROJECT_LABEL: Final[str] = "Unknown Project ({})"
CORRUPTED_PROJECT_LABEL: Final[str] = "Corrupted Project ({})"

# Element labels — single source of truth for all UI components
ELEMENT_LABELS: Final[Dict[str, str]] = {
    'space': '🌌 공간',
    'time': '⏰ 시간',
    'creatures': '👥 생물',
    'nature': '🌿 자연',
    'culture': '🎭 문화',
    'language': '🗣️ 언어',
    'mythology': '⚡ 신화',
    'philosophy': '💭 철학',
    'rules': '⚖️ 규칙',
    'economy': '💰 경제',
    'politics': '🏛️ 정치',
    'energy': '✨ 에너지',
}
