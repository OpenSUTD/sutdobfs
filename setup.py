from setuptools import setup

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name="sutdobfs",
    packages=["sutdobfs"],
    entry_points={"console_scripts": ["sutdobfs = sutdobfs.__main__:main"]},
    version="1.0.0",
    description="Establish your variable names in collaboration with MIT",
    long_description=long_descr,
    author="Chester Koh",
    author_email="chester8991@gmail.com",
    url="https://github.com/OpenSUTD/sutdobfs",
)
