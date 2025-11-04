from setuptools import setup, find_packages
from sapyautomation import __version__

requirements = []
version = __version__

with open("requirements.txt", "r") as fh:
    for line in fh.readlines():
        requirements.append(line)

with open("README.md", "r") as fh:
    long_description = fh.read()


if __name__ == '__main__':
    setup(
        name='sapyautomation',
        version=version,
        author='Albano Pena Torres',
        author_email='albano.pena@mx.ey.com',
        description='Python library to automate the Microsoft Windows GUI, '
                    'SAP flows and browser ',
        include_package_data=True,
        install_requires=requirements,
        long_description=long_description,
        long_description_content_type="text/markdown",
        url='https://www.sapyautomation.com',
        packages=find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: Other/Proprietary License",
            "Operating System :: Microsoft :: Windows",
        ],
        python_requires='>=3.7',
        entry_points={
            "console_scripts": [
                'sapy = sapyautomation.__main__:main',
                ]
            }
    )
