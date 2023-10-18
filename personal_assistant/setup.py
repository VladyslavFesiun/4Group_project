from setuptools import setup

setup(name='personal_assistant',
      version='1.0.0',
      description='This package can create addressbook and notebook, '
                  'sort your files and generate temp folder with random files',
      author='4Group',
      license='MIT',
      packages=['personal_assistant'],
      include_package_data=True,
      install_requires=['numpy', 'Pillow', 'prompt_toolkit'],
      entry_points={'console_scripts': ['create-books = personal_assistant.adress_book:main',
                                        'clean-folder = personal_assistant.sorter:sort_files',
                                        'fill-files = personal_assistant.generator:file_generator', ]
                    },
)