import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


__version__ = "0.0.1"

REPO_NAME = "Text-Summzrization"
AUTHOR_NAME = "SaadBens"
SRC_REPO = "textSummarization"
AUTHOR_EMAIL = "saad.benslimann@gmail.com"



setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    description="Text Summarization Code app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github/{AUTHOR_NAME}/{REPO_NAME}",
    project_urls={
        "bug Tracker": f"https://github/{AUTHOR_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src")
)
     