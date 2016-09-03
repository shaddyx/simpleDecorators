from distutils.core import setup
setup(
  name = 'simpleDecorators',
  packages = ['simpledecorators'],
  version = '0.1',
  description = 'a collection of simple decorators',
  author = 'Anatolii Yakushko',
  author_email = 'shaddyx@gmail.com',
  url = 'https://github.com/shaddyx/simpleDecorators', # use the URL to the github repo
  download_url = 'https://github.com/shaddyx/simpleDecorators/tarball/0.1',
  keywords = ['testing', 'logging', 'example'], # arbitrary keywords
  classifiers = [],
  install_requires=[
          'expiringdict',
      ]
)
