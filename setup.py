from setuptools import setup, find_packages

#
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='MultiSourceToMarkdown',
    version='1.0.0',
    author='kenny_anoano',
    author_email='129825517+kennyanoano@users.noreply.github.com',
    description='A tool to convert various source formats into Markdown',
    packages=find_packages(),
    install_requires=requirements,
)
