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

        packages=[pkg, 'orger.modules'],
        # TODO ugh, it's weird. If it's editable install, python3 -m 'orger.modules.module' doesn't work. But it does if installed without editable??
        # for not solved with a symlink...
        package_dir={
            '': 'src',
            'orger.modules': 'modules',
        },
        package_data={pkg: ['py.typed']},

        ## ^^^ this should be mostly automatic and not requiring any changes

        url='https://github.com/karlicoss/orger',
        author='Dima Gerasimov',
        author_email='karlicoss@gmail.com',
        description='Converts data into org-mode',

        install_requires=[
            'appdirs'     , # to keep state files
            'atomicwrites', # to safely append data to a file
        ],
        extras_require={
            'testing': ['pytest'],
            'linting': [
                'pytest',
                'mypy', 'lxml', # lxml for cov report
            ],
        },
    )


if __name__ == '__main__':
    main()
