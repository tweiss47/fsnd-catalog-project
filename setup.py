from setuptools import find_packages, setup


with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name='songcat',
    version='0.1.1',
    author='Taylor Weiss',
    author_emai='taylor.weiss@comcast.net',
    description='Udacity FSND catalog project',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask_sqlalchemy',
        'google-auth',
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ]
)
