from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="bot-assist",
    version=1.0,
    description="Personal assistent made by Team 14 GoIT Neo",
    long_description=long_description,
    author="Oleksandr Kryvosheyin, Olha Hanziienko, Oleh Petryshyn, Sergii Kryvko",
    license="MIT",
    url="https://github.com/kryvosheyin/goitneo-python-final-project-group14",
    include_package_data=True,
    install_requires=["rich"],
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['bot-assist=src.main:main']}
)
