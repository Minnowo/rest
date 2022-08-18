
from . import errors
from . import const
from typing import Union
import os 

def parse_int(x : Union[int, str], default=0):

    if not x: return default
    try     : return int(x)
    except (ValueError, TypeError): return default

def parse_float(x : Union[float, str], default=0):

    if not x: return default
    try     : return float(x)
    except (ValueError, TypeError): return default


def expand_path(path, default=None):
    """Expand environment variables and tildes (~)"""
    if not path:
        if not default:
            return path
        return default

    if not isinstance(path, str):
        path = os.path.join(*path)

    return os.path.expandvars(os.path.expanduser(path))


def read_sig(sig_path : str):
    
    with open(sig_path, "rb") as reader:

        data = reader.read(512)

    if not data.startswith(const.SIG_BYTE_HEADER) or len(data) != 512:

        try:

            os.rename(sig_path, sig_path + "~")

        except OSError:
            raise errors.Sig_File_Unwriteable

        return write_sig(sig_path)

    return data 


def write_sig(sig_path : str):
    
    data = const.SIG_BYTE_HEADER + os.urandom(512 - len(const.SIG_BYTE_HEADER))

    with open(sig_path, "wb") as writer:

        writer.write(data)

    return data 