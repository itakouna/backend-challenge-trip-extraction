import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='trip-extraction',
    version='0.1',
    scripts=['trip-extraction'],
    author="Ibrahim Takouna",
    description="Extract trips from list or stream of waypoints",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/itakouna/backend-challenge-trip-extraction/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
