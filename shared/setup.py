# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

import setuptools

setuptools.setup(
    name="shared",
    version="0.1.0",
    author="Higor Grigorio",
    author_email="higorgrigorio@gmail.com",
    description="A shared package for all services",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.9',
)
