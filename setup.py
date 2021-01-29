import setuptools

with open('README.md') as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requirements = [line for line in f]

setuptools.setup(
    name='SNR',
    version='0.4.0',
    author='Spencer Shaw',
    author_email='calpolyroboticsclub@gmail.com',
    packages=setuptools.find_packages(include=["snr"]),
    url='http://github.com/sfshaw-calpoly/SNR',
    license='LICENSE.txt',
    description='Soft-realtime robotics framework for education',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    python_requires='>=3.6'
)
