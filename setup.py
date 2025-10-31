from setuptools import setup, find_packages

setup(
    name='frame',
    version='0.2.3',
    description='the frame lib',
    author='pt',
    author_email='kvantorium73.int@gmail.com',
    packages=find_packages(),
    install_requires=[
        'Cython',
        'setuptools',
    ],
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
