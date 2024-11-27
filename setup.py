from setuptools import setup, find_packages
import pathlib
 
HERE = pathlib.Path(__file__).parent

 
README = (HERE / "README.md").read_text()
 
setup(
    name="morgan_course_data",
    version="0.1",
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
    install_requires=["pymongo"]
)