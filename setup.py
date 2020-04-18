# see https://github.com/karlicoss/pymplate for up-to-date reference


from setuptools import setup, find_packages # type: ignore


def main():
    pkgs = find_packages('src')
    [pkg] = pkgs
    setup(
        name=pkg,
        use_scm_version={
            'version_scheme': 'python-simplified-semver',
            'local_scheme': 'dirty-tag',
        },
        setup_requires=['setuptools_scm'],

        zip_safe=False,

        packages=[pkg],
        package_dir={'': 'src'},
        package_data={pkg: ['py.typed']},

        ## ^^^ this should be mostly automatic and not requiring any changes

        url='https://github.com/karlicoss/orger',
        author='Dima Gerasimov',
        author_email='karlicoss@gmail.com',
        description='Converts data into org-mode',

        install_requires=['atomicwrites'],
        extras_require={
            'testing': ['pytest'],
            'linting': ['pytest', 'mypy', 'pylint'],
        },
    )


if __name__ == '__main__':
    main()
