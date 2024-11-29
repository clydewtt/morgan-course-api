import sys
import os

# Add the project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from unittest.mock import MagicMock
from morgan_course_data.api import MorganCourseData

# Sample data for testing
SAMPLE_COURSE = {
    "_id": "23087hdwgd72392391ndsd",
    "signature": "COSC101",
    "subject_abbreviation": "COSC",
    "subject": "Computer Science",
    "credit_hours": 3,
    "name": "Introduction to Programming",
    "number": "101",
    "full_name": "COSC 101 - Introduction to Programming",
    "prerequisites": {},
    "sections": [
        {
            "title": "Intro to Programming - Section 1",
            "section": "001",
            "type": "Lecture",
            "crn": 12345,
            "instructional_method": "In-Person",
            "instructor": "Dr. Smith",
            "enrollment_actual": 25,
            "enrollment_max": 30,
            "enrollment_available": 5,
            "meetings": [
                {
                    "start_time": "10:00 AM",
                    "end_time": "11:30 AM",
                    "days": ["Monday", "Wednesday"],
                    "building": "Science Hall",
                    "campus": "Main",
                    "room": "101",
                    "start_date": "2024-01-10",
                    "end_date": "2024-05-05",
                }
            ],
        }
    ],
}


@pytest.fixture
def mock_morgan_course_data():
    """Fixture to initialize the MorganCourseData instance with a mocked database."""
    morgan_data = MorganCourseData(term="FALL_2024")
    morgan_data.course_db = MagicMock()
    morgan_data.other_db = MagicMock()
    return morgan_data


def test_get_courses_paginated(mock_morgan_course_data):
    """Test get_courses_paginated method."""
    # Mock database return
    mock_morgan_course_data.course_db.find.return_value.sort.return_value.limit.return_value = [
        SAMPLE_COURSE
    ]

    # Call the method
    result = mock_morgan_course_data.get_courses_paginated(page_size=1)

    # Assertions
    assert len(result["courses"]) == 1
    assert result["courses"][0].signature == "COSC101"
    assert result["pagination"]["page_size"] == 1


def test_get_all_courses(mock_morgan_course_data):
    """Test get_all_courses method."""
    # Mock database return
    mock_morgan_course_data.course_db.find.return_value = [SAMPLE_COURSE]

    # Call the method
    result = mock_morgan_course_data.get_all_courses()

    # Assertions
    assert len(result) == 1
    assert result[0].signature == "COSC101"


def test_get_course_by_signature(mock_morgan_course_data):
    """Test get_course_by_signature method."""
    # Mock database return
    mock_morgan_course_data.course_db.find_one.return_value = SAMPLE_COURSE

    # Call the method
    result = mock_morgan_course_data.get_course_by_signature("COSC101")

    # Assertions
    assert result is not None
    assert result.signature == "COSC101"


def test_get_courses_by_subject_abbreviation(mock_morgan_course_data):
    """Test get_courses_by_subject_abbreviation method."""
    # Mock database return
    mock_morgan_course_data.course_db.find.return_value = [SAMPLE_COURSE]

    # Call the method
    result = mock_morgan_course_data.get_courses_by_subject_abbreviation("COSC")

    # Assertions
    assert len(result) == 1
    assert result[0].subject_abbreviation == "COSC"


def test_get_course_sections_by_instructor(mock_morgan_course_data):
    """Test get_course_sections_by_instructor method."""
    # Mock database return
    mock_morgan_course_data.course_db.find.return_value = [SAMPLE_COURSE]

    # Call the method
    result = mock_morgan_course_data.get_course_sections_by_instructor("Dr. Smith")

    # Assertions
    assert len(result) == 1
    assert result[0].instructor == "Dr. Smith"


def test_get_all_instructors(mock_morgan_course_data):
    """Test get_all_instructors method."""
    # Mock database return
    mock_morgan_course_data.course_db.find.return_value = [
        {"signature": "COSC101", "sections": SAMPLE_COURSE["sections"]}
    ]

    # Call the method
    result = mock_morgan_course_data.get_all_instructors()

    # Assertions
    assert len(result) == 1
    assert result[0].name == "Dr. Smith"
    assert "COSC101" in result[0].course_signatures


def test_get_subject_abbreviation_map(mock_morgan_course_data):
    """Test get_subject_abbreviation_map method."""
    # Mock database return
    mock_morgan_course_data.other_db.find_one.return_value = {
        "subject_to_abbreviations_map": {"COSC": "Computer Science"}
    }

    # Call the method
    result = mock_morgan_course_data.get_subject_abbreviation_map()

    # Assertions
    assert "COSC" in result
    assert result["COSC"] == "Computer Science"
