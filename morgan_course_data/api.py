from .db import get_db_connection
from typing import List
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Course:
    signature: str
    subject: str
    name: str
    number: str
    full_name: str
    sections: List["CourseSection"] = field(default_factory=list)

@dataclass(frozen=True)
class CourseSection:
    title: str
    section: str
    type: str
    instructional_method: str
    instructor: str
    building: str
    campus: str
    room: str
    enrollment_actual: str
    enrollment_max: str
    enrollment_available: str
    start_time: str
    end_time: str
    days: List[str]
    start_date: str
    end_date: str

@dataclass(frozen=True)
class Instructor:
    name: str
    course_titles: list[str]

class MorganCourseData:
    ALLOWED_TERMS = {"FALL_2024", "SPRING_2025"}  # Define the allowed terms as a set

    def __init__(self, term: str):
        """
        Initialize the MorganCourseData object with a MongoDB connection.

        Args:
            term (str): The term for which the course data should be retrieved.

            TERMS: `FALL_2024, SPRING_2025`

        Raises:
            ValueError: If the term is not one of the allowed choices.
        """
        if term not in self.ALLOWED_TERMS:
            raise ValueError(f"Invalid term '{term}'. Allowed terms are: {', '.join(self.ALLOWED_TERMS)}")
        
        self.db = get_db_connection()[f"{term}_COURSES"]

    def get_all_courses(self) -> List[Course]:
        """
        Fetch all courses from the database and return them as a list of `Course` dataclass objects.
        """
        # Fetch raw data from the database
        raw_courses = self.db.find()
        
        courses = []
        for raw_course in raw_courses:
            # Transform sections into `CourseSection` dataclass objects
            sections = [
                CourseSection(
                    title=section.get("title", ""),
                    section=section.get("section", ""),
                    type=section.get("type", ""),
                    instructional_method=section.get("instructional_method", ""),
                    instructor=section.get("instructor", ""),
                    building=section.get("building", ""),
                    campus=section.get("campus", ""),
                    room=section.get("room", ""),
                    enrollment_actual=section.get("enrollment_actual", ""),
                    enrollment_max=section.get("enrollment_max", ""),
                    enrollment_available=section.get("enrollment_available", ""),
                    start_time=section.get("start_time", ""),
                    end_time=section.get("end_time", ""),
                    days=section.get("days", []),
                    start_date=section.get("start_date", ""),
                    end_date=section.get("end_date", ""),
                )
                for section in raw_course.get("sections", [])
            ]
            
            # Create the `Course` dataclass object
            course = Course(
                signature=raw_course.get("signature", ""),
                subject=raw_course.get("subject", ""),
                name=raw_course.get("name", ""),
                number=raw_course.get("number", ""),
                full_name=raw_course.get("full_name", ""),
                sections=sections,
            )
        
            # Add the `Course` object to the list
            courses.append(course)
        
        return courses

    def get_course_by_subject(self, subject_abbrevation: str) -> list[Course]:
        """
        Fetch courses for a specific subject.

        Args:
            subject_abbrevation (str): The subject abbrevation for which the course data should be retrieved. 
            
            Example: COSC for Computer Science

        Returns:
            A list of `Course` objects with all their sections.

        """

        data = self.db.find({"course.subject": subject_abbrevation})

        courses = []
        for doc in data:
            sections = [CourseSection(**section) for section in doc.get("sections", [])]
            course = Course(
                signature=doc["course"]["signature"],
                subject=doc["course"]["subject"],
                name=doc["course"]["name"],
                number=doc["course"]["number"],
                full_name=doc["course"]["full_name"],
                sections=sections,
            )
            courses.append(course)
        return courses

    def get_course_sections_by_instructor(self, instructor_name: str) -> List[CourseSection]:
        """
        Fetch course sections taught by the specified instructor.

        Args:
            instructor_name (str): The instructor name for which the course data should be retrieved. Follows `lastName, firstName`
            
            Example: 'Naja, Mack'

        Returns:
            A list of `CourseSection` objects taught by the given instructor

        """
         
        data = self.db.find({"sections.instructor": instructor_name})

        sections = []
        for doc in data:
            # Filter sections for the specified instructor
            filtered_sections = [
                CourseSection(**section)
                for section in doc["sections"]
                if section["instructor"] == instructor_name
            ]
            # Add the filtered sections to the list
            sections.extend(filtered_sections)

        return sections

    def get_all_instructors(self) -> list[Instructor]:
        """
        Fetch all unique instructors and the courses they teach.

        Returns:
            A list of Instructor objects.

        """

        data = self.db.find({}, {"sections.instructor": 1, "sections.title": 1, "sections.section": 1})

        instructor_dict = {}

        for doc in data:
            for section in doc.get("sections", []):
                instructor_name = section.get("instructor")
                if instructor_name:
                    if instructor_name not in instructor_dict:
                        instructor_dict[instructor_name] = {
                            "course_titles": [],
                            "sections": [],
                        }
                    instructor_dict[instructor_name]["course_titles"].append(section["title"])

        # Convert the dictionary to a list of Instructor objects
        instructors = [
            Instructor(name=name, course_titles=info["course_titles"])
            for name, info in instructor_dict.items()
        ]

        return instructors