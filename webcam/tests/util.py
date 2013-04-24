import os
import shutil
import stat


HERE = os.path.dirname(__file__)
PICTURE_NAME = 'colosseo.jpg'
PICTURE_PATH = os.path.join(HERE, 'data', PICTURE_NAME)
PICTURE = open(PICTURE_PATH, 'rb').read()


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


def rmtree(path):
    def _osrem(*args):
        func, path, __ = args  # onerror returns a tuple containing function, path and exception info
        os.chmod(path, stat.S_IWRITE)
        os.remove(path)

    if os.path.exists(path):
        shutil.rmtree(path, onerror=_osrem)


try:
    from PIL import Image

    def is_jpg(filename):
        try:
            i = Image.open(filename)
            return i.format == 'JPEG'
        except IOError:
            return False
except ImportError:

    def is_jpg(filename):
        data = open(filename, 'rb').read(11)
        if data[:4] != '\xff\xd8\xff\xe0': return False
        if data[6:] != 'JFIF\0': return False
        return True
