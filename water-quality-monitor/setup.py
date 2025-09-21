from setuptools import setup, find_packages
setup(
    name="water-quality-monitor",
    description="Backend and frontend for data collection.",
    version="0.1",
    packages=find_packages(),
    # Future dependencies will be updated
    install_requires=[
        'openpyxl',
        'pandas',
    ],
)