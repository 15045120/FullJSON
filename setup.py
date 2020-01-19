import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fulljson",
    version="0.0.52",
    author="15045120",
    author_email="1337078409@qq.com",
    description="simple json conversion implements using stack structure and recursive method",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/15045120/FullJSON",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)
