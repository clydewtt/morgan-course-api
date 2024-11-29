
# Morgan Course Data API
![PyPI](https://img.shields.io/pypi/v/morgan-course-data) ![Downloads](https://img.shields.io/pypi/dm/morgan-course-data) ![Morgan State University](https://img.shields.io/badge/Morgan%20State%20University-🐻-blue) 

![FALL_2024_Refresh_Date](https://img.shields.io/badge/FALL%202024%20Data%20Refresh-11/29/24-orange) ![WINTER_2025_Refresh_Date](https://img.shields.io/badge/WINTER%202025%20Data%20Refresh-11/29/24-blue) ![SPRING_2025_Refresh_Date](https://img.shields.io/badge/SPRING%202025%20Data%20Refresh-11/29/24-orange)

A Python package for interacting with Morgan State University's course data. This package enables developers to query courses, retrieve instructor information, and perform various operations on course data efficiently.

**Note**: Data is updated at the beginning of each semester.

---

## Features

- **Get All Courses**: Fetch all courses and their sections.
- **Get Paginated Courses**: Retrieve courses with pagination using cursors for better performance.
- **Get Course by Signature**: Retrieve a specific course using its unique signature.
- **Get Courses by Subject Abbreviation**: Retrieve all courses for a specific subject.
- **Get Course Sections by Instructor**: Fetch all sections taught by a specific instructor.
- **Get All Instructors**: List all instructors and their associated courses.
- **Get Subject to Abbreviation Mappings**: Retrieve a dictionary mapping subjects to abbreviations.

---

## Installation

To install this package, simply install the package from PyPi:

```bash
pip install morgan_course_data
```

---

## Usage

### Initialize the Data Handler

Start by creating an instance of the `MorganCourseData` class, specifying one of the allowed terms (`FALL_2024`, `WINTER_MINIMESTER_2025`, `SPRING_2025`):

```python
from morgan_course_data.api import MorganCourseData

morgan_data = MorganCourseData(term="FALL_2024")
```

### Get All Courses

Retrieve all courses for the specified term.

> **Warning**: This method can return over 1,000 elements. Use `get_courses_paginated()` for production use.

#### Returns:
- **`courses`**: A list of all `Course` objects available in the specified term.

#### Example Usage:
```python
fall_courses = morgan_data.get_all_courses() # List[Course]

for course in fall_courses:
    print(course)
```

### Get Paginated Courses

Fetch courses in a paginated manner using `cursor` and `page_size`. Pagination ensures efficient fetching of large datasets.

#### Parameters:
- **`cursor`**: Reference to last retrieved course, used for pagination (optional).
- **`page_size`**: The number of items per page (default: 20, max: 50).

#### Returns:
- **[`GetCoursesPaginatedResponse`](#getcoursespaginatedresponse)**: Response object

#### Example Usage:
```python
# Fetch the first page
paginated_courses = morgan_data.get_courses_paginated(page_size=10)

for course in paginated_courses["courses"]:
    print(course)

# Retrieve pagination metadata
pagination_info = paginated_courses["pagination"]
print(f"Next Cursor: {pagination_info['next_cursor']}")
print(f"Page Size: {pagination_info['page_size']}")
print(f"Has More: {pagination_info['has_more']}")

# Fetch the next page using the cursor
if pagination_info['has_more']:
    next_cursor = pagination_info["next_cursor"]
    next_page = morgan_data.get_courses_paginated(cursor=next_cursor, page_size=10)

    for course in next_page["courses"]:
        print(course)
```

---

### Get Courses by Subject Abbreviation

Retrieve all courses under a specific subject (e.g., `COSC` for Computer Science):

#### Returns:
- **`courses`**: A list of all [`Course`](#course) objects with the specified subject abbreviation

#### Example Usage
```python
cosc_courses = morgan_data.get_courses_by_subject_abbreviation("COSC") # List[Course]

for course in cosc_courses:
    print(course)
```

---

### Get Course by Signature

Retrieve a specific course using its unique signature:

#### Returns:
- **`course`**: A [`Course`](#course) object with the specified course signature

#### Example Usage
```python
course = morgan_data.get_course_by_signature("COSC 111") # Course

if course:
    print(course)
else:
    print("Course not found.")
```

---

### Get Course Sections by Instructor

Retrieve all sections taught by a specific instructor. Format the instructor name as `'LastName, FirstName'`:

#### Returns:
- **`course_sections`**: A list of all [`CourseSection`](#coursesection) objects with the specified instructor

#### Example Usage
```python
mack_sections = morgan_data.get_course_sections_by_instructor("Mack, Naja")

for section in mack_sections: # List[CourseSection]
    print(section)
```

---

### Get All Instructors

Fetch a list of all instructors and the courses they teach:

#### Returns:
- **`instructors`**: A list of all [`Instructor`](#instructor) objects

#### Example Usage
```python
instructors = morgan_data.get_all_instructors() # List[Instructor]

for instructor in instructors:
    print(f'{instructor.name} teaches {instructor.course_signatures}')

```

---

### Get Subject to Abbreviation Mappings

Retrieve a dictionary of subjects and their abbreviations:

#### Returns:
- **`dict`**: A dictionary/map of subjects and their abbreviation. `Dict[key=subject: str, value=abbreviation: str]`

#### Example Usage
```python
subject_mappings = morgan_data.get_subject_abbreviation_map() # Dict[subject: str, abbreviation: str]

for subject, abbreviation in subject_mappings.items():
    print(f"{subject}: {abbreviation}")
```

## Data Models

### `Course`
Represents a course with its metadata and sections.

```python
class Course:
    signature: str
    subject_abbreviation: str
    subject: str
    credit_hours: int
    name: str
    number: str
    full_name: str
    prerequisites: dict
    sections: List["CourseSection"]
```

### `CourseSection`
Represents an individual section of a course.

```python
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
    meetings: List["Meeting"]
```

### `Meeting`
Represents a scheduled meeting for a course section.

```python
class Meeting:
    start_time: str
    end_time: str
    days: List[str]
    building: str
    campus: str
    room: str
    start_date: str
    end_date: str
```

### `Instructor`
Represents an instructor and the courses they teach.

```python
class Instructor:
    name: str
    course_signatures: list[str]
```

---

## Response Objects
### `GetCoursesPaginatedResponse`
Represents a response object to the `get_courses_pagination` method.

```python
class PaginationMetadata(TypedDict):
    next_cursor: Optional[str]  # The cursor for fetching the next page of results
    page_size: int              # The number of courses per page
    has_more: bool              # Indicates if more pages are available

class GetCoursesPaginatedResponse(TypedDict):
    courses: List['Course']      # List of Course objects
    pagination: PaginationMetadata  # Metadata for pagination
```

## Contact

For any questions, suggestions, or issues, please contact: `cltandjong@gmail.com`
