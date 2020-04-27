from setuptools import setup, find_packages

long_description = open('./README.md').read()

setup(
    name='mail-analysis',
    version='0.1.0',

    description='mailbox file analysis',
    long_description=long_description,
    author='Jacopo Farina',
    packages=find_packages(),
    python_requires='>=3',
    install_requires=[
        'plotly',
        'tqdm',
    ],
    entry_points={
        'console_scripts': [
            'mbox-analyze = mailanalysis.__main__:main',
        ]
    },
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov'
        ]
    }
)
