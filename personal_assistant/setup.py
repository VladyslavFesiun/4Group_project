from setuptools import setup

setup(name='personal_assistant',
      version='0.0.1',
      description='This app can create addressbook and notebook',
      author='Vladyslav Fesiun',
      license='MIT',
      packages=['personal_assistant'],
      entry_points={'console_scripts': ['personal-assistant = personal_assistant.adress_book:main']
                    },
)