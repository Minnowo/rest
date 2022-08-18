
class B_Exception(Exception):
    """Base exception class"""


class Backup_Exists_Exception(B_Exception):
    """Raised when a backup with the same name is present in the db"""


class Backup_Not_Found_Exception(B_Exception):
    """Raised when a backup does not exist"""

class Repo_Not_Found_Exception(B_Exception):
    """Raised when a repo is not found on the file system"""


class Repo_Exists_Exception(B_Exception):
    """Raised when a repo already exists"""

class Sig_File_Unwriteable(B_Exception):
    """Raised when a sig file cannot be written"""

    