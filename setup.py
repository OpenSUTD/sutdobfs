from setuptools import find_packages, setup

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name="sutdobfs",
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    entry_points={"console_scripts": ["sutdobfs = sutdobfs.__main__:main"]},
    version="1.0.4",
    description="SUTD Obfuscator – Establish your variable names in collaboration with MIT",
    long_description=long_descr,
    long_description_content_type="text/markdown",
    author="Chester Koh",
    author_email="chester8991@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    url="https://github.com/OpenSUTD/sutdobfs",
)
