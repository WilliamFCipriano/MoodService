from distutils.core import setup

setup(name='MoodService',
      version='0.0',
      description='Registers and reports the users mood',
      author='Will Cipriano',
      author_email='will@willcipriano.com',
      packages=['MoodService', 'MoodService.objects', 'MoodService.repositories', 'MoodService.services'],
      include_package_data=True,
      install_requires=['flask'])