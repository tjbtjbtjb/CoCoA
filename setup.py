from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='CoCoA',
    url='https://github.com/tjbtjbtjb/CoCoA',
    author='Olivier Dadoun, Julien Browaeys, Tristan Beau',
    author_email='odadoun@gmail.com,browaeys@gmail.com,tristan.beau@gmail.com',
    # Needed to actually package something
    packages=['cocoa','cocoaplot'],
    # Needed for dependencies
    install_requires=['numpy','requests','pandas','matplotlib'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='MIT',
    description='CoCoA stands for COvid COlab Analysis project, which is an open source project initially designed to run in the Google colab environment.',
    # We will also need a readme eventually (there will be a warning)
    long_description=open('README.md').read(),
)
