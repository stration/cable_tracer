from setuptools import setup, find_packages

setup(
    name="cable_tracer",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        Django>=5.0,<6.0
        djangorestframework>=3.15,<4.0

    ],
    author="Igor Mentoyan",
    author_email="your.email@example.com",
    description="NetBox plugin for full cable path tracing",
    url="https://github.com/stration/cable_tracer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
        python_requires=">=3.8",
)
