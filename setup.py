from setuptools import setup, find_packages
from io import open
from os import path
import pathlib

# The directory containing this file

HERE = pathlib.Path(__file__).parent  # The text of the README file
README = (HERE / 'README.md').read_text()  # automatically captured required modules for install_requires in requirements.txt and as well as configure dependency links
with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if 'git+' not in x
                    and not x.startswith('#') and not x.startswith('-')]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs
                    if 'git+' not in x]

setup(  # list of all packages
        # any python greater than 2.7
    name='idt',
    description='A cli tool that quickly generates ready-to-use image datasets'
        ,
    version='0.0.5',
    packages=find_packages(),
    install_requires=install_requires,
    python_requires='>=2.7',
    entry_points='''
        [console_scripts]
        idt=idt.__main__:main
    ''',
    author='Deliton Junior',
    keyword='idt, image datasets, generators, dataset generator, image scraper'
        ,
    long_description=README,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/deliton/idt',
    download_url='https://github.com/deliton/idt/archive/master.zip',
    dependency_links=dependency_links,
    author_email='deliton.m@hotmail.com',
    classifiers=['License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.7'],
    )
