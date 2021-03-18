import setuptools
from os import path

this_directory = path.abspath(path.dirname(__file__))


with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


with open(path.join(this_directory, "cdk-requirements.txt"), encoding="utf-8") as f:
    install_requires = f.readlines()

setuptools.setup(
    name="airflow-fargate-cdk",
    version="0.0.1",
    description="A Deployment of Airflow on ECS Fargate using AWS CDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="author",
    package_dir={"": "cdk"},
    packages=setuptools.find_packages(where="cdk"),
    install_requires=install_requires,
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
)
