#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

from setuptools import setup, find_packages
from setuptools.command.install import install


def git_version(version):
    """Return version with local version identifier."""
    import git
    repo = git.Repo('.git')
    repo.git.status()
    sha = repo.head.commit.hexsha
    if repo.is_dirty():
        return '{v}.dev0+{sha}.dirty'.format(
            v=version, sha=sha)
    # commit is clean
    # is it release of `version` ?
    try:
        tag = repo.git.describe(
            match='v[0-9]*', exact_match=True,
            tags=True, dirty=True)
    except git.GitCommandError:
        return '{v}.dev0+{sha}'.format(
            v=version, sha=sha)
    assert tag == 'v' + version, (tag, version)

    return version


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != version:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, version
            )
            sys.exit(info)


# this will be overwritten by bumpversion
version = '0.6.19'
# append git commit hash if version is not tagged
version = git_version(version)

requirements = [
    "pyyaml",
    "future",
    "numpy",
    "pandas>=0.21.0",
    "tqdm",
    "attrs>=17.4.0",
    "related>=0.6.0",
    "colorlog",
    "jinja2",
    "cookiecutter>=1.6.0",
    # sometimes required
    "h5py",
    "urllib3>=1.21.1",  # ,<1.23",
    "tinydb",
    "kipoi-utils>=0.3.8",
    "kipoi-conda>=0.1.6",
    "deprecation>=2.0.6"
]

test_requirements = [
    "bump2version",
    "wheel",
    "jedi",
    "epc",
    "pytest>=3.3.1",
    "pytest-xdist",  # running tests in parallel
    "pytest-pep8",  # see https://github.com/kipoi/kipoi/issues/91
    "pytest-cov",
    "coveralls",
    "scikit-learn",
    "cython",
    "keras",
    "tensorflow",
    # "genomelake>=0.1.4",     # test_10_KipoiModel.py (fails on circle-ci)
    "zarr>=2.2.0",  # test_161_writers.py
    # "cyvcf2>=0.10.0",        # test_20_cli_examples.py (and others) (fails on circle-ci)
    "kipoi-interpret>=0.1.2",  # test_42_kipoi_interpret.py
    "concise>=0.6.6"
]

setup(
    name='kipoi',
    version=version,
    description="Kipoi: model zoo for genomics",
    author="Kipoi team",
    author_email='avsec@in.tum.de',
    url='https://github.com/kipoi/kipoi',
    long_description="Kipoi: model zoo for genomics. http://kipoi.org/",
    packages=find_packages(),
    install_requires=requirements,
    extras_require={
        "develop": test_requirements,
        "vep": ["kipoi_veff"],  # backcompatibily
    },
    entry_points={'console_scripts': ['kipoi = kipoi.__main__:main']},
    license="MIT license",
    zip_safe=False,
    keywords=["model zoo", "deep learning",
              "computational biology", "bioinformatics", "genomics"],
    test_suite='tests',
    include_package_data=True,
    tests_require=test_requirements,
    cmdclass={
        'verify': VerifyVersionCommand,
    }
)
