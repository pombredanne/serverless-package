from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

install_requires = [
    "docker",
    "requirements-parser",
]

setup(
    name="lambda-packaging",
    version="0.3.0",
    description=(
        "Pulumi-based python solution for Packaging an AWS Lambda and its Layer."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nuage-studio/python-lambda-packaging",
    packages=find_packages(exclude=("tests", "example")),
    zip_safe=True,
    install_requires=install_requires,
)
