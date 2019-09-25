from setuptools import setup, find_packages

name = 'orger'

if __name__ == '__main__':
    setup(
        name=name,
        version='0.0.1',
        url='https://github.com/karlicoss/orger',
        author='Dima Gerasimov',
        author_email='karlicoss@gmail.com',
        description='Converts data into org-mode',
        packages=find_packages(),
        extras_require={
            'testing':  ['pytest', 'mypy', 'pylint'],
        },
        package_data={name: ['py.typed']},
    )
