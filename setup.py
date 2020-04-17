from setuptools import setup, find_packages


if __name__ == '__main__':
    [pkg] = find_packages('src')
    setup(
        name=pkg,
        use_scm_version=True,
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
