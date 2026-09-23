import configparser
import inspect
import os

config = None

class MyError():

  def __init__(self, et):
    self.config = configparser.RawConfigParser()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    error_files = [
        'GlobalErrorMessages.properties',
        'tpplexer/LexerErrorMessages.properties',
        'tppparser/ParserErrorMessages.properties',
        'tppparser/ParserMessages.properties',
        'tppsema/SemaErrorMessages.properties',
        'tppcodegen/CodeGenErrorMessages.properties'
    ]

    for file_path in error_files:
        if os.path.exists(file_path):
            self.config.read(file_path, encoding='utf-8')
        else:
            abs_path = os.path.join(base_dir, file_path)
            if os.path.exists(abs_path):
                self.config.read(abs_path, encoding='utf-8')

    self.errorType = et

  def newError(self, koption, key, line=None, column=None, *args, **data):
    message = ''
  
    if(koption):
      return key
    else:
      try:
        has_pos = line is not None and column is not None and int(line) > 0 and int(column) > 0
      except (ValueError, TypeError):
        has_pos = False

      if has_pos:
        message = message + f"Erro[{line}][{column}]: "

      if key:
        if self.config.has_section(self.errorType) and self.config.has_option(self.errorType, key):
          template = self.config.get(self.errorType, key)
        else:
          template = key

        msg = template
        if args or data:
          try:
            msg = template.format(*args, **data)
          except Exception:
            if args:
              try:
                temp_msg = template
                for arg in args:
                  temp_msg = temp_msg.replace('{}', str(arg), 1)
                msg = temp_msg
              except Exception:
                pass

        message = message + msg

        if data:
          unused_data = [f"{k}: {v}" for k, v in data.items() if f"{{{k}}}" not in template]
          if unused_data:
            message = message + " " + ", ".join(unused_data)

      return message

