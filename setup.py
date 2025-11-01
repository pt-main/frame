from setuptools import setup, find_packages


setup(
    name='frame-fwl', # frame-framework-lib
    version='0.2.6.2',
    description='The Frame - multitool module for programming with advanced framing capabilities',
    author='pt',
    author_email='kvantorium73.int@gmail.com',
    packages=find_packages(),
    install_requires=[],
    python_requires='>=3.9',
    
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Operating System :: OS Independent',
    ],
    keywords='frame, framing, code generation, execution',
    url='https://github.com/pt-main/frame'
)
