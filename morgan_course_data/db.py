from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://read:xtUxRpHUrVMhNI8T@courses.oqzo0.mongodb.net/?retryWrites=true&w=majority&appName=courses"


def get_db_connection(uri=uri, db_name="course_info"):
    """
    Connect to MongoDB and return the database instance.
    """
    client = MongoClient(uri, server_api=ServerApi("1"))
    return client[db_name]


def write_unique_courses_to_db():
    db = get_db_connection().course_sections

    course_list = list(db.find())

    unique_courses = {}
    for course in course_list:
        # Use a unique identifier for the course, such as `course.signature`
        signature = course['course']['signature']
        if signature not in unique_courses:
            unique_courses[signature] = course['course']

            
        course.pop("course")
        unique_courses[signature]["sections"].append(course)

    # Return the values of the unique_courses dictionary
    unique_courses = list(unique_courses.values())

    print(len(unique_courses))

    print(unique_courses)

    get_db_connection()["FALL_2024_COURSES"].insert_many(unique_courses)

    return True

# write_unique_courses_to_db()