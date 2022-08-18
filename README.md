## rest
A simple backup manager for [restic](https://github.com/restic/restic)

## Usage:

First create a 'backup' 
```ps
python ./main.py -b 'backup_name_here' -c 
```

Then use restic to create a repository, and add it to rest
```ps
restic init -r 'path_to_repo'
Repo password...

python ./main.py -b 'backup_name_here' --add-repo 'path_to_repo'
```

Next add files and folders which you want to sync. <br>
NOTE - any repos added to the backup will have all files and folders synced to them
```ps
python ./main.py -b 'backup_name_here' --add-dir 'path_to_a_directory'
python ./main.py -b 'backup_name_here' --add-dir 'another_path_to_a_directory'
python ./main.py -b 'backup_name_here' --add-file 'path_to_a_file'
```
Now you can have all the added files and folders synced to any repo added to the backup. <br>
```ps
python ./main.py -b 'backup_name_here' --sync
Enter password...
```

## Config:

You can config the very minimal settings by editing [const.py](./rest/const.py)


If you want to change the arguments passed into restic when syncing you can find that in [__init__.py](./rest/__init__.py) in the `def sync_db(backup_id, cursor):` function.