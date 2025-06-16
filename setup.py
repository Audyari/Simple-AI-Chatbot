from setuptools import setup, find_packages

setup(
    name="simple-ai-chatbot",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "google-generativeai>=0.3.0",
        "python-dotenv>=0.19.0",
        "colorama>=0.4.4",
        "fpdf2>=2.7.0",
    ],
    python_requires=">=3.8",
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple AI chatbot using Google's Gemini API",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/simple-ai-chatbot",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
