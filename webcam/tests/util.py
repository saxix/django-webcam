import os
from PIL import Image

HERE = os.path.dirname(__file__)
PICTURE_NAME = 'colosseo.jpg'
PICTURE_PATH = os.path.join(HERE, 'data', PICTURE_NAME)
PICTURE = file(PICTURE_PATH).read()


def mktree(newdir):
    """works the way a good mkdir should :)
        - already exists, silently complete
        - regular file in the way, raise an exception
        - parent directory(ies) does not exist, make them as well
    """
    if os.path.isdir(newdir):
        pass
    elif os.path.isfile(newdir):
        raise OSError("a file with the same name as the desired "
                      "dir, '%s', already exists." % newdir)
    else:
        os.makedirs(newdir)


def is_jpg(filename):
    try:
        i = Image.open(filename)
        return i.format == 'JPEG'
    except IOError:
        return False
