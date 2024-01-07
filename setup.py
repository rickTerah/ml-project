from setuptools import find_packages, setup
from typing import List


HYPHEN_E_DO = '-e .'


def get_requirements(file_path: str) -> List[str]:
    '''
    Returns the list of required packages
    '''
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        if HYPHEN_E_DO in requirements:
            requirements.remove(HYPHEN_E_DO)


setup(
    name='ml-project',
    version='0.0.1',
    author='rickTerah',
    author_email='patrickmwangi554@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)
