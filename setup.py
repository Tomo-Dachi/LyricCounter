from setuptools import setup

setup(
    name='yourscript',
    version='0.1.0',
    py_modules=['lyricscounter', 'musicranx', 'test_musicranx'],
    install_requires=[
        'Click',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'lyricscounter = lyricscounter:cli',
        ],
    },
)