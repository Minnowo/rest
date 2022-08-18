

import subprocess
import os 

from . import db
from . import opts 
from . import util
from . import const 
from . import errors


def finish(cursor, connection):
    connection.commit()
    cursor.close()
    connection.close()



def add_repo(BACKUP_ID, repo_path, name=None, *, cursor):

    repo_path = os.path.abspath(util.expand_path(repo_path))
        
    if not os.path.isdir(repo_path):

        raise errors.Repo_Not_Found_Exception("Repo with the path '{}' was not found.".format(repo_path)) 

    if not name:

        name = "{0}-{1}".format(BACKUP_ID, db.get_repo_number(BACKUP_ID, cursor=cursor))

    # the sig does nothing  currently, i was gonna use them to identify the repository before trying to sync
    sig_path = os.path.join(repo_path, ".rest.sig")

    if os.path.isfile(sig_path):
        
        sig = util.read_sig(sig_path)

    else:

        sig = util.write_sig(sig_path)

    db.add_repo(name, repo_path, sig, BACKUP_ID, cursor=cursor)


def remove_repo(BACKUP_ID, repo_name, cursor):

    db.remove_repo_from_name(repo_name, BACKUP_ID, cursor=cursor)


def list_db(bid, backup_name, cursor):
    
    BACKUP_ID = 0
    BACKUP_NAME = 1

    REPO_ID   = 0
    REPO_PATH = 1
    REPO_NAME = 2
    REPO_SIG  = 3

    FOLDER_PATH = 1
    FILE_PATH   = 1

    def ls_backup(back_id, name):

        print("Backup {} {}".format(back_id, name))

        cursor.execute("SELECT * FROM tbl_backup_repo WHERE backup_id=?", (back_id,))
        _ = cursor.fetchall()

        print("   Added repos: {}".format(len(_)))
        print("      Name, Path")
        for row in _:

            print("      {} {}".format(row[REPO_NAME], row[REPO_PATH]))


        cursor.execute("SELECT * FROM tbl_backup_folders WHERE backup_id=?", (back_id,))
        _ = cursor.fetchall()

        print("\n   Added directories: {}".format(len(_)))
        for row in _:

            print("      {}".format(row[FOLDER_PATH]))

        cursor.execute("SELECT * FROM tbl_backup_files WHERE backup_id=?", (back_id,))
        _ = cursor.fetchall()

        print("\n   Added files: {}".format(len(_)))
        for row in _:

            print("      {}".format(row[FOLDER_PATH]))

    if bid:
        
        ls_backup(bid, backup_name)
        return 


    cursor.execute("SELECT * FROM tbl_backups")
    for row in cursor.fetchall():

        ls_backup(row[BACKUP_ID], row[BACKUP_NAME])



def sync_db(backup_id, cursor):

    print("syncing")

    cursor.execute("SELECT * FROM tbl_backup_repo WHERE backup_id=?", (backup_id,))
    repos = (x[1] for x in cursor.fetchall())

    cursor.execute("SELECT * FROM tbl_backup_folders WHERE backup_id=?", (backup_id,))
    folders = [x[1] for x in cursor.fetchall()]

    cursor.execute("SELECT * FROM tbl_backup_files WHERE backup_id=?", (backup_id,))
    files = [x[1] for x in cursor.fetchall()]

    for repo in repos:

        args = [const.RESTIC_PATH, "-r", repo, "backup"]
        args.extend(folders)
        args.extend(files)

        # print("Running restic with args {}".format(args))
        subprocess.run(args, shell=True)


def main():

    parser = opts.get_parser()
    args   = parser.parse_args()

    connection = db.get_connection(const.DATABASE_PATH)
    cursor = connection.cursor()

    db.create_tables(cursor, connection)

    BACKUP_NAME = args.backup
    
    if not BACKUP_NAME:
        
        if args.list:
            list_db(None, None, cursor) 
            finish(cursor, connection)
            return 0

        parser.error("The backup name is required. Use -b or --backup to specify the name.")

    if args.create:
        print("Creating backup with name {}".format(BACKUP_NAME))
        db.add_backup(BACKUP_NAME, cursor=cursor)
        finish(cursor, connection)
        return 0
        
    BACKUP_ID = db.get_backup_id(BACKUP_NAME, cursor=cursor)

    ADD    = args.add 
    REMOVE = args.remove 
    DIR    = os.path.abspath(util.expand_path(args.dir   , "."))
    FILE   = os.path.abspath(util.expand_path(args.file  , "."))
    RDIR   = os.path.abspath(util.expand_path(args.rfile , "."))
    RFILE  = os.path.abspath(util.expand_path(args.rdir  , "."))

    if args.list:

        list_db(BACKUP_ID, BACKUP_NAME, cursor) 
        finish(cursor, connection)
        return 0

    if args.sync:
        sync_db(BACKUP_ID, cursor)
        finish(cursor, connection)
        return 0

    if args.add:
        
        add_repo(BACKUP_ID, ADD, cursor=cursor)
        finish(cursor, connection)
        return 0

    if args.remove:
        
        remove_repo(BACKUP_ID, REMOVE, cursor=cursor)
        finish(cursor, connection)
        return 0

    if args.dir:
        
        if os.path.isfile(DIR):
            db.add_file(BACKUP_ID, DIR, cursor=cursor)
            finish(cursor, connection)
            return 0

        db.add_directory(BACKUP_ID, DIR, cursor=cursor)
        finish(cursor, connection)
        return 0

    if args.file:

        if os.path.isdir(FILE):
            db.add_directory(BACKUP_ID, FILE, cursor=cursor)
            finish(cursor, connection)
            return 0

        db.add_file(BACKUP_ID, FILE, cursor=cursor)
        finish(cursor, connection)
        return 0

    if args.rdir:

        db.remove_directory(BACKUP_ID, RDIR, cursor=cursor)
        finish(cursor, connection)
        return 0 

    if args.rfile:

        db.remove_file(BACKUP_ID, RFILE, cursor=cursor)
        finish(cursor, connection)
        return 0 

    return 0 
