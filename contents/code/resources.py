__name__ = 'resources'

import os

def get_current_code_directory():
  return os.path.dirname(os.path.abspath(__file__))


def get_current_working_directory():
  return os.getcwd()


def get_image_directory():
  return get_current_code_directory().replace("code", "images")


def get_image_path(filename):
  return os.path.join(get_image_directory(), filename)


