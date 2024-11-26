# Morgan Course Data API

A Python package for interacting with Morgan State University's course data. This package enables developers to query courses, retrieve instructor information, and perform various operations on course data efficiently.

Note: Data is updated at the beginning of each semester.

---

## Features

- **Get All Courses**: Find all courses and their course sections.
- **Get Courses by Subject Abbrevation**: Retrieve all courses under a specified subject.
- **Get Course Sections by Instructor**: Retrieve all course sections taught by a specific instructor.
- **Get All Instructors**: List all instructors and the courses they teach.

---

## Installation

To install this package, simply install the package from PyPi

```bash
pip install morgan_course_data
```

## Usage

### Initialize the Data Handler

Start by creating an instance of the MorganCourseData class

(Specify either FALL_2024 or SPRING_2025 as the term)

```python
from morgan_course_data.api import MorganCourseData

morgan_data = MorganCourseData(term="FALL_2024")
```

### Get all Courses

Retrieve all courses from the specified term

```python
fall_courses = morgan_data.get_all_courses()

for course in fall_courses:
    print(course)
```

### Get Courses by Subject Abbrevation

Retrieve all courses under a specified subject

```python
cosc_courses = morgan_data.get_courses_by_subject("COSC")

for course in cosc_courses:
    print(course)
```

### Get Course Sections by Instructor

Retrieve all course sections taught by a instructor

The instructor argument should be formatted as: 'lastName, firstName'

```python
naja_mack_course_sections = morgan_data.get_course_sections_by_instructor("Mack, Naja")

for section in naja_mack_course_sections:
    print(section)
```

### Get All Instructors

Retrieve a list of all instructors and the courses they teach:

```python
instructors = morgan_data.get_all_instructors()

for instructor in instructors:
    print(instructor)
```

## Data Models

`Course`
Represents a course with its metadata and sections.

```python
class Course:
    signature: str
    subject: str
    name: str
    number: str
    full_name: str
    sections: List[CourseSection]
```

`CourseSection`
Represents an individual section of a course.

```python
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
```

`Instructor`
Represents an instructor and the courses they teach.

```python
class Instructor:
    name: str
    course_titles: list[str]
```

## Inquires

For any recommendations, questions, etc email me at `cltandjong@gmail.com`
