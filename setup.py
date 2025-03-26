from setuptools import setup, find_packages

setup(
  name='Guia de Acomodações para Moradia Estudantil',
  version='1.1',
  author='Robson Cicero da Silva',
  author_email='rcs9@proton.me',
  description='Backend service for https://proaes-game.deno.dev',
  long_description=open('README.md').read(),
  long_description_content_type='text/markdown',
  url='https://github.com/robcs9/proaes-game-be',
  packages=find_packages(),
  install_requires=[
    # List your project's dependencies here.
    # Example: 'requests>=2.23.0'
    'fastapi[standard]>=0.113.0,<0.114.0',
    'pydantic>=2.7.0,<3.0.0',
    'curl_cffi',
    'beautifulsoup4',
    'lxml',
    'numpy',
    'requests',
    'urllib3',
    'python-dotenv',
    'pandas',
    'boto3',
    'supabase',
  ],
  classifiers=[
      'Programming Language :: Python :: 3',
      'License :: OSI Approved :: MIT License',
      'Operating System :: OS Independent',
  ],
  python_requires='>=3.6',
)
