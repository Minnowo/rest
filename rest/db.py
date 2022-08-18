import sqlite3
from . import errors

def get_connection(database_path : str, foreign_key_checks=True):
    
    conn = sqlite3.connect(database_path)

    if foreign_key_checks:
    
        conn.execute('pragma foreign_keys = ON')

    return conn


def create_tables(cursor, connection=None):

    cursor.execute("""CREATE TABLE IF NOT EXISTS "tbl_backups" (
        "backup_id" INTEGER PRIMARY KEY NOT NULL,
        "backup_name" VARCHAR UNIQUE
    );
    """)
    
    # repositories to sync 
    cursor.execute("""CREATE TABLE IF NOT EXISTS "tbl_backup_repo" (
        "backup_id" INTEGER,
        "repo_path" VARCHAR,
        "repo_name" VARCHAR,
        "repo_sig" BLOB,
        FOREIGN KEY(backup_id) REFERENCES tbl_backups(backup_id) ON DELETE CASCADE
    );""")

    # folders to backup everytime 
    cursor.execute("""CREATE TABLE IF NOT EXISTS "tbl_backup_folders" (
        "backup_id" INTEGER,
        "folder_path" VARCHAR,
        FOREIGN KEY(backup_id) REFERENCES tbl_backups(backup_id) ON DELETE CASCADE
    );""")

    # files to backup everytime 
    cursor.execute("""CREATE TABLE IF NOT EXISTS "tbl_backup_files" (
        "backup_id" INTEGER,
        "file_path" VARCHAR,
        FOREIGN KEY(backup_id) REFERENCES tbl_backups(backup_id) ON DELETE CASCADE
    );""")

    if connection:
        connection.commit()
    


def add_backup(backup_name : str, *, cursor):

    backup_name = backup_name.lower()

    cursor.execute("SELECT backup_id FROM tbl_backups WHERE backup_name=?", (backup_name,))
    rows = cursor.fetchone()

    if rows:    

        raise errors.Backup_Exists_Exception("A backup with the name '{}' already exists.".format(backup_name))

    cursor.execute("INSERT INTO tbl_backups values(NULL, ?)", (backup_name,))


def get_backup_id(backup_name : str, *, cursor):

    backup_name = backup_name.lower()

    cursor.execute("SELECT backup_id FROM tbl_backups WHERE backup_name=?", (backup_name,))
    rows = cursor.fetchone()

    if not rows:

        raise errors.Backup_Not_Found_Exception("Could not find backup with name '{}', if you meant to create this backup use the -c or --create argument.".format(backup_name))

    return rows[0]


def add_repo(repo_name : str, repo_path : str, repo_sig : bytes, backup_id : int, *, cursor):

    repo_name = repo_name.upper()

    cursor.execute("SELECT * FROM tbl_backup_repo WHERE repo_name=? AND backup_id=?", (repo_name, backup_id))
    rows = cursor.fetchone()

    if rows:

        raise errors.Repo_Exists_Exception("A repo with the name '{}' already exists.".format(repo_name))

    cursor.execute("INSERT INTO tbl_backup_repo VALUES (?, ?, ?, ?)", (backup_id, repo_path, repo_name, repo_sig))


def remove_repo_from_name(repo_name : str, backup_id : int, *, cursor):

    repo_name = repo_name.upper()
    
    cursor.execute("SELECT * FROM tbl_backup_repo WHERE repo_name=? AND backup_id=?", (repo_name, backup_id))
    rows = cursor.fetchone()

    if not rows:

        return 

    cursor.execute("DELETE FROM tbl_backup_repo WHERE repo_name=? AND backup_id=?", (repo_name, backup_id))


def get_repo_number(backup_id : int, * , cursor):

    cursor.execute("SELECT backup_id FROM tbl_backup_repo WHERE backup_id=?", (backup_id,))
    rows = cursor.fetchall()
    
    if not rows:

        return 0
        # raise errors.Backup_Not_Found_Exception("Could not find backup with id '{}'.".format(backup_id))

    return len(rows)


def add_directory(backup_id : int, dir_path : str, *, cursor):

    dir_path = dir_path.rstrip("\\")

    cursor.execute("INSERT INTO tbl_backup_folders VALUES (?, ?)", (backup_id, dir_path))

def add_file(backup_id : int, file_path : str, *, cursor):

    cursor.execute("INSERT INTO tbl_backup_files VALUES (?, ?)", (backup_id, file_path))


def remove_directory(backup_id : int, dir_path : str, *, cursor):

    dir_path = dir_path.rstrip("\\")
    
    cursor.execute("DELETE FROM tbl_backup_folders WHERE backup_id=? AND folder_path=?", (backup_id, dir_path))

def remove_file(backup_id : int, file_path : str, *, cursor):

    cursor.execute("DELETE FROM tbl_backup_files WHERE backup_id=? AND file_path=?", (backup_id, file_path))

