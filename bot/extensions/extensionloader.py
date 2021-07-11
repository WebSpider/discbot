import os
from bot.config import settings


def find_extensions():
    extensions_list = []
    python_list = [os.path.join(dirpath, f) for dirpath, dirname, filenames in os.walk(settings.extensions_dir) for f in
                   filenames if os.path.splitext(f)[1] == '.py']
    for py in python_list:
        if __file__ not in py:
            with open(py, mode='r') as f:
                for line in f:
                    if "def setup(" in line:
                        extensions_list.append(py)
                        f.close()
                    else:
                        f.close()

    return extensions_list

def setup(bot):
    for extension in find_extensions():
        bot.load_extension(extension)