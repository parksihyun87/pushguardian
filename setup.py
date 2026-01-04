from setuptools import setup, find_packages

setup(
    name="pushguardian",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0",
        "rich>=13.0.0",
        "langgraph>=0.2.0",
        "langchain-core>=0.3.0",
        "langchain-openai>=0.2.0",
        "tavily-python>=0.5.0",
        "requests>=2.31.0",
        "fastapi>=0.115.0",
        "uvicorn[standard]>=0.30.0",
        "python-multipart>=0.0.9",
        "streamlit>=1.39.0",
    ],
    entry_points={
        "console_scripts": [
            "pushguardian=pushguardian.cli:main",
        ],
    },
    python_requires=">=3.10",
)
