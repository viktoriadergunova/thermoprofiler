from setuptools import setup, find_packages

setup(
    name="thermoprofiler",
    version="1.1.0",
    url="https://github.com/viktoriadergunova/thermoprofiler.git",
    author="Hamid Reza Mousavi, Viktoria Dergunova",
    license="IUST",
    packages=find_packages(),  # Automatically find valid package directories
    include_package_data=True,
    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn"
    ]
)
