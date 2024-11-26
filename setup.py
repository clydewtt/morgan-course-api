from setuptools import setup, find_packages

setup(
    name="morgan_course_data",
    version="0.1.3",
    packages=find_packages(),
    install_requires=["pymongo"],
    description="Python package for querying Morgan State University course data.",
    author="Clyde Tandjong",
    author_email="cltandjong@gmail.com",
    url="https://github.com/clydewtt/morgan-course-api",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)