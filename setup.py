from setuptools import setup, find_packages

setup(
    name='python-immoscraper',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # 'requests>=2.24.0',
        # List your project's dependencies here
    ],
    scripts=[
       'modules/app.py'
    ],
    author='Jean-Louis HERVE',
    author_email='jeanlouis.herve@hotmail.fr',
    description='This is a webscraper script to find the goods to be sold in a city for training purpose.',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
