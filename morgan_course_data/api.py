from .db import get_db_connection
from bson import ObjectId
from .types import Course, CourseSection, Meeting, Instructor, GetCoursesPaginatedResponse, PaginationMetadata
from typing import List, Optional, Dict, Union

class MorganCourseData:
    ALLOWED_TERMS = {"FALL_2024", "WINTER_MINIMESTER_2025", "SPRING_2025"}
    PAGE_SIZE_MAX = 50

    def __init__(self, term: str):
        """
        Initialize the MorganCourseData object with a MongoDB connection.

        Args:
            term (str): The term for which the course data should be retrieved.

            TERMS: `FALL_2024, WINTER_MINIMESTER_2025, SPRING_2025`

        Raises:
            ValueError: If the term is not one of the allowed choices.
        """
        if term not in self.ALLOWED_TERMS:
            raise ValueError(f"Invalid term '{term}'. Allowed terms are: {', '.join(self.ALLOWED_TERMS)}")

        self.course_db = get_db_connection(term)['COURSES']
        self.other_db = get_db_connection("SPRING_2025")['OTHER_DATA']

    def get_courses_paginated(
        self, cursor: Optional[str] = None, page_size: int = 20
    ) -> GetCoursesPaginatedResponse:
        """
        Fetch a paginated list of courses using a cursor-based approach.

        Args:
            cursor (str): The `_id` of the last item from the previous page.
            page_size (int): The number of courses per page. (MAX is 50)

        Returns:
            Dict[str, Any]: A dictionary containing paginated results and metadata.
        """
        page_size = min(page_size, self.PAGE_SIZE_MAX)

        query = {}
        if cursor:
            query["_id"] = {"$gt": ObjectId(cursor)}  # Fetch items after the cursor

        # Fetch courses sorted by `_id` for a stable order
        raw_courses = self.course_db.find(query).sort("_id", 1).limit(page_size)

        courses: list[Course] = []
        last_id = None
        for raw_course in raw_courses:
            # Transform sections into `CourseSection` dataclass objects
            sections = [
                CourseSection(
                    title=section.get("title", ""),
                    section=section.get("section", ""),
                    type=section.get("type", ""),
                    crn=section.get("crn", -1),
                    instructional_method=section.get("instructional_method", ""),
                    instructor=section.get("instructor", ""),
                    enrollment_actual=section.get("enrollment_actual", ""),
                    enrollment_max=section.get("enrollment_max", ""),
                    enrollment_available=section.get("enrollment_available", ""),
                    meetings=[
                        Meeting(
                            start_time=meeting.get("start_time", ""),
                            end_time=meeting.get("end_time", ""),
                            days=meeting.get("days", []),
                            building=meeting.get("building", ""),
                            campus=meeting.get("campus", ""),
                            room=meeting.get("room", ""),
                            start_date=meeting.get("start_date", ""),
                            end_date=meeting.get("end_date", ""),
                        )
                        for meeting in section.get("meetings", [])
                    ],
                )
                for section in raw_course.get("sections", [])
            ]

            # Create the `Course` dataclass object
            course = Course(
                signature=raw_course.get("signature", ""),
                subject_abbreviation=raw_course.get("subject_abbreviation", ""),
                subject=raw_course.get("subject", ""),
                credit_hours=raw_course.get("credit_hours", 0),
                name=raw_course.get("name", ""),
                number=raw_course.get("number", ""),
                full_name=raw_course.get("full_name", ""),
                prerequisites=raw_course.get("prerequisites", {}),
                sections=sections,
            )

            # Add the `Course` object to the list
            courses.append(course)

            last_id = raw_course["_id"]

        # Return results with metadata
        return {
            "courses": courses,  # List[Course]
            "pagination": {      # PaginationMetadata
                "next_cursor": str(last_id) if last_id else None,
                "page_size": page_size,
                "has_more": bool(last_id),
            },
        }

    def get_all_courses(self) -> List[Course]:
        """
        DISCOURAGED USE, DON'T USE IN PRODUCTION - Please use `get_courses_paginated()` for better efficiency

        Fetch all courses from the database and return them as a list of `Course` dataclass objects.
        """
        # Fetch raw data from the database
        raw_courses = self.course_db.find()

        courses = []
        for raw_course in raw_courses:
            # Transform sections into `CourseSection` dataclass objects
            sections = [
                CourseSection(
                    title=section.get("title", ""),
                    section=section.get("section", ""),
                    type=section.get("type", ""),
                    crn=section.get("crn", -1),
                    instructional_method=section.get("instructional_method", ""),
                    instructor=section.get("instructor", ""),
                    enrollment_actual=section.get("enrollment_actual", ""),
                    enrollment_max=section.get("enrollment_max", ""),
                    enrollment_available=section.get("enrollment_available", ""),
                    meetings=[
                        Meeting(
                            start_time=meeting.get("start_time", ""),
                            end_time=meeting.get("end_time", ""),
                            days=meeting.get("days", []),
                            building=meeting.get("building", ""),
                            campus=meeting.get("campus", ""),
                            room=meeting.get("room", ""),
                            start_date=meeting.get("start_date", ""),
                            end_date=meeting.get("end_date", ""),
                        )
                    for meeting in section.get("meetings", [])
                ],
                )
                for section in raw_course.get("sections", [])
            ]

            # Create the `Course` dataclass object
            course = Course(
                signature=raw_course.get("signature", ""),
                subject_abbreviation=raw_course.get("subject_abbreviation", ""),
                subject=raw_course.get("subject", ""),
                credit_hours=raw_course.get("credit_hours", 0),
                name=raw_course.get("name", ""),
                number=raw_course.get("number", ""),
                full_name=raw_course.get("full_name", ""),
                prerequisites=raw_course.get("prerequisites", {}),
                sections=sections,
            )

            # Add the `Course` object to the list
            courses.append(course)

        return courses

    def get_course_by_signature(self, course_signature: str) -> Union[Course, None]:
        """
        Retrieve a specific course by its signature.

        Args:
            course_signature (str): The unique signature of the course to be retrieved.

        Returns:
            Course: A `Course` object with all its sections, or None if the course is not found.
        """
        # Fetch the course document from the database
        doc = self.course_db.find_one({"signature": course_signature})

        if not doc:
            return None

        # Transform sections into `CourseSection` dataclass objects
        sections = [
                CourseSection(**{k: v for k, v in section.items() if k != '_id'})
                for section in doc.get("sections", [])]

        # Create and return the `Course` dataclass object
        return Course(
                signature=doc["signature"],
                subject_abbreviation=doc["subject_abbreviation"],
                subject=doc["subject"],
                credit_hours=doc["credit_hours"],
                name=doc["name"],
                number=doc["number"],
                full_name=doc["full_name"],
                prerequisites=doc["prerequisites"],
                sections=sections
            )

    def get_courses_by_subject_abbreviation(self, subject_abbreviation: str) -> List[Course]:
        """
        Fetch courses for a specific subject.

        Args:
            subject_abbreviation (str): The subject abbreviation for which the course data should be retrieved. 
            
            Example: COSC for Computer Science

        Returns:
            A list of `Course` objects with all their sections.

        """

        data = self.course_db.find({"subject_abbreviation": subject_abbreviation})

        courses = []
        for doc in data:
            sections = [
                CourseSection(**{k: v for k, v in section.items() if k != '_id'})
                for section in doc.get("sections", [])]
            course = Course(
                signature=doc["signature"],
                subject_abbreviation=doc["subject_abbreviation"],
                subject=doc["subject"],
                credit_hours=doc["credit_hours"],
                name=doc["name"],
                number=doc["number"],
                full_name=doc["full_name"],
                prerequisites=doc["prerequisites"],
                sections=sections
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

        data = self.course_db.find({"sections.instructor": instructor_name})

        sections = []
        for doc in data:
            # Filter sections for the specified instructor
            filtered_sections = [
                CourseSection(**{k: v for k, v in section.items() if k != "_id"})
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
        data = self.course_db.find({}, {"signature": 1, "sections.instructor": 1})

        instructor_dict = {}

        for doc in data:
            course_signature = doc.get("signature", "")
            for section in doc.get("sections", []):
                instructor_name = section.get("instructor")
                if instructor_name:
                    if instructor_name not in instructor_dict:
                        instructor_dict[instructor_name] = {
                            "course_signatures": [],
                        }

                    # Add the course signature to the instructor's list, avoiding duplicates
                    if (
                        course_signature
                        and course_signature
                        not in instructor_dict[instructor_name]["course_signatures"]
                    ):
                        instructor_dict[instructor_name]["course_signatures"].append(
                            course_signature
                        )

        # Convert the dictionary to a list of Instructor objects
        instructors = [
            Instructor(name=name, course_signatures=info["course_signatures"])
            for name, info in instructor_dict.items()
        ]

        return instructors

    def get_subject_abbreviation_map(self) -> Dict[str, str]:
        """
        Retrieve the latest subject-to-abbreviation map

        Returns:
            Dict[str, str]: A dictionary mapping subjects to their abbreviations.
        """
        # Fetch the latest document by time
        latest_doc = self.other_db.find_one(
            {},
            sort=[("time", -1)],
        )

        if not latest_doc:
            return {}

        return latest_doc.get("subject_to_abbreviations_map", {})
