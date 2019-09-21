from setuptools import setup, find_packages

if __name__ == '__main__':
    setup(
        name='orger',
        version='0.0.1',
        url='https://github.com/karlicoss/orger',
        author='Dima Geerasimov',
        author_email='karlicoss@gmail.com',
        description='Converts data int org-mode',
        packages=find_packages(),
        extras_require={
            'testing':  ['pytest', 'mypy', 'pylint'],
        },
    )
