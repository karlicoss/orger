from setuptools import setup, find_packages


if __name__ == '__main__':
    # from setuptools_scm import get_version
    # https://github.com/pypa/setuptools_scm#default-versioning-scheme
    # get_version(version_scheme='python-simplified-semver', local_scheme='no-local-version')
   
    [pkg] = find_packages('src')
    setup(
        name=pkg,
        use_scm_version={
            'version_scheme': 'python-simplified-semver',
            'local_scheme': 'dirty-tag',
        },
        setup_requires=['setuptools_scm'],

        url='https://github.com/karlicoss/orger',
        author='Dima Gerasimov',
        author_email='karlicoss@gmail.com',
        description='Converts data into org-mode',
        packages=[pkg],
        package_dir={'': 'src'},
        install_requires=['atomicwrites'],
        extras_require={
            'testing': ['pytest'],
            'linting': ['pytest', 'mypy', 'pylint'],
        },
        package_data={pkg: ['py.typed']},
    )
