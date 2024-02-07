import setuptools
import os


PACKAGE_NAME = 'pyakamai'
PACKAGE_KEYWORDS = [
    'Akamai',
    'Python',
    'CDN',
    'SDK',
    'Edge',
]

project_root = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the project's README.rst file
with open(os.path.join(project_root, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
     name=PACKAGE_NAME,
     version='2.32',
     author="Achuthananda M P",
     author_email="achuthadivine@gmail.com",
     description="A Boto3 like SDK for Akamai",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/Achuthananda/pyakamai",
     packages=['pyakamai'],
     install_requires=['edgegrid-python','requests'],
     python_requires=">= 3.7",
     keywords=" ".join(PACKAGE_KEYWORDS),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
         'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
     ],
     project_urls={
        'Source': 'https://github.com/Achuthananda/pyakamai',
    },
 )
