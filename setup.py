from setuptools import setup, find_packages

setup(
    name='thorn.py-remast',
    version='0.1.0',
    description='A Python module for web scraping and image scraping',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='ohioman02',
    author_email='gdnunuuwu@gmail.com',
    url='https://github.com/RoseInjector/Thorn-Remastered-',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
