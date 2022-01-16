import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flauncher",
    version="1.5.0",
    python_requires='>=3',
    author="yoarch",
    author_email="yo.managements@gmail.com",
    description="Universal CLI file launcher",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yoarch/flauncher",
    packages=setuptools.find_packages(),
    install_requires=["natsort"],
    data_files=[('/flauncher/conf', ['README.md', 'conf/open.json', 'conf/edit.json'])],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
	"console_scripts": [
	"flauncher = flauncher.__main__:main"
        ]
    })
