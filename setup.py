from setuptools import setup, find_packages
from maiden import __version__

setup(
    name='maiden',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'pyyaml',
        'jinja2',
    ],
    entry_points={
        'console_scripts': [
            'maiden=maiden.main:generate_md',
        ],
    },
    package_data={
        '': ['templates/*.md', '*.yaml'],
    },
    author='Huseyin Gomleksizoglu',
    author_email='huseyim@gmail.com',
    description='A tool to generate Markdown files from templates populated with data from YAML or JSON files.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/gomleksiz/maiden',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
