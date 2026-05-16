from setuptools import setup, find_packages

setup(
    name="task-manager-cli",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "task=task_manager.cli:main",
        ],
    },
    python_requires=">=3.10",
)
