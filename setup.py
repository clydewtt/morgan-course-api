from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent

# Explicitly specify UTF-8 encoding when reading the README
README = (HERE / "README.md").read_text(encoding="utf-8")

setup(
    name="morgan_course_data",
    version="0.1.2",
    packages=find_packages(),
    description="Python package for querying Morgan State University course data.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Clyde Tandjong",
    author_email="cltandjong@gmail.com",
    url="https://github.com/clydewtt/morgan-course-api",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=["pymongo", "bson"],
    extras_require={"dev": ["pytest>=6.0.0"]},
)
