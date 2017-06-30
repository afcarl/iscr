from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='iscr',
      version='0.1',
      description='Interactive Spoken Content Retrieval',
      url='http://github.com/iammrhelo/ISCR',
      author='Antonie Lin',
      author_email='iammrhelo@gmail.om',
      license='MIT',
      packages=['iscr'],
	  install_requires=required,
      zip_safe=False)
