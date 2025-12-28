# models/project.py
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any

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
    rules: Rules = field(default_factory=Rules) # Rules는 별도 dataclass
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
    project_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    project_name: str = "새로운 세계"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    genre: str = "SF/판타지"
    
    concept: Concept = field(default_factory=Concept)
    elements: WorldElements = field(default_factory=WorldElements)
    
    # 그 외 메타 데이터
    connections: List[Dict[str, Any]] = field(default_factory=list)
    notes: str = ""
    completion_rate: float = 0.0

    def to_dict(self):
        """데이터 클래스를 딕셔너리로 변환 (JSON 저장을 위해)"""
        # dataclasses.asdict를 사용하면 좋지만, 커스텀 로직이 필요할 경우 직접 구현
        return {
            "project_id": self.project_id,
            "project_name": self.project_name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "genre": self.genre,
            "concept": self.concept.__dict__,
            "elements": {
                "space": self.elements.space.__dict__,
                "time": self.elements.time.__dict__,
                "creatures": self.elements.creatures.__dict__,
                "nature": self.elements.nature.__dict__,
                "culture": self.elements.culture.__dict__,
                "language": self.elements.language.__dict__,
                "mythology": self.elements.mythology.__dict__,
                "philosophy": self.elements.philosophy.__dict__,
                "rules": self.elements.rules.__dict__,
                "economy": self.elements.economy.__dict__,
                "politics": self.elements.politics.__dict__,
                "energy": self.elements.energy.__dict__,
            },
            "connections": self.connections,
            "notes": self.notes,
            "completion_rate": self.completion_rate
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """딕셔너리에서 데이터 클래스로 변환 (JSON 불러오기를 위해)"""
        concept_data = data.get("concept", {})
        elements_data = data.get("elements", {})
        
        # 각 요소별 데이터 로드
        elements = WorldElements(
            space=Element(**elements_data.get("space", {})),
            time=Element(**elements_data.get("time", {})),
            creatures=Element(**elements_data.get("creatures", {})),
            nature=Element(**elements_data.get("nature", {})),
            culture=Element(**elements_data.get("culture", {})),
            language=Element(**elements_data.get("language", {})),
            mythology=Element(**elements_data.get("mythology", {})),
            philosophy=Element(**elements_data.get("philosophy", {})),
            rules=Rules(**elements_data.get("rules", {})),
            economy=Element(**elements_data.get("economy", {})),
            politics=Element(**elements_data.get("politics", {})),
            energy=Element(**elements_data.get("energy", {}))
        )
        
        return cls(
            project_id=data.get("project_id", str(uuid.uuid4())),
            project_name=data.get("project_name", "이름 없는 세계"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            genre=data.get("genre"),
            concept=Concept(**concept_data),
            elements=elements,
            connections=data.get("connections", []),
            notes=data.get("notes", ""),
            completion_rate=data.get("completion_rate", 0.0)
        )
