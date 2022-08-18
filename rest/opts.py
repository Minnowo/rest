
import argparse


def get_parser():
    
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION]... URL...",
        add_help=False,
    )

    general = parser.add_argument_group("General Options")
    general.add_argument(
        "-h", "--help",
        action="help",
        help="Print this help message and exit",
    )
    general.add_argument(
        "-b", "--backup",
        dest="backup", metavar="NAME", 
        help="The name of the backup",
    )
    general.add_argument(
        "-c", "--create",
        dest="create", action="store_true", 
        help="Create the backup",
    )
    general.add_argument(
        "-a", "--add-repo",
        dest="add", metavar="PATH",
        help="Adds a repo to the backup.",
    )
    general.add_argument(
        "-r", "--remove",
        dest="remove", metavar=" NAME",
        help="Remove a repo with the given name from the backup.",
    )
    general.add_argument(
        "-l", "--list",
        dest="list", action="store_true",
        help="List the db.",
    )
    general.add_argument(
        "-d", "--add-dir",
        dest="dir", metavar="PATH",
        help="Add path to the directory.",
    )
    general.add_argument(
        "-f", "--add-file",
        dest="file", metavar="PATH",
        help="Add path to the file.",
    )
    general.add_argument(
        "-rd", "--remove-dir",
        dest="rdir", metavar="PATH",
        help="Remove directory path.",
    )
    general.add_argument(
        "-rf", "--remove-file",
        dest="rfile", metavar="PATH",
        help="Remove file path.",
    )
    general.add_argument(
        "-S", "--sync",
        dest="sync", action="store_true",
        help="Sync all files and folders to their repo for selected backup.",
    )
    return parser