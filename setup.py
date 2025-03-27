from setuptools import setup, find_packages

setup(
    name="cable_tracer",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=3.2,<4.0",
        "djangorestframework>=3.12,<3.15",
        "netbox>=4.2.2,<4.3.0",
        "vis-network==9.1.0"
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
