from typing import TypedDict, Optional, List
from dataclasses import dataclass, field


class PaginationMetadata(TypedDict):
    next_cursor: Optional[str]
    page_size: int
    has_more: bool


class GetCoursesPaginatedResponse(TypedDict):
    courses: List['Course']
    pagination: PaginationMetadata


@dataclass(frozen=True)
class Course:
    signature: str
    subject_abbreviation: str
    subject: str
    credit_hours: int
    name: str
    number: str
    full_name: str
    prerequisites: dict
    sections: List["CourseSection"] = field(default_factory=list)


@dataclass(frozen=True)
class CourseSection:
    title: str
    section: str
    type: str
    crn: int
    instructional_method: str
    instructor: str
    enrollment_actual: str
    enrollment_max: str
    enrollment_available: str
    meetings: List["Meeting"] = field(default_factory=list)


@dataclass(frozen=True)
class Meeting:
    start_time: str
    end_time: str
    days: list[str]
    building: str
    campus: str
    room: str
    start_date: str
    end_date: str


@dataclass(frozen=True)
class Instructor:
    name: str
    course_signatures: list[str]
