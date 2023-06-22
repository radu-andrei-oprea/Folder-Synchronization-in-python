#!/usr/bin/env python3

"""
os: Module providing functions for path operations and listing

the contents of a directory

sys: Module providing command line arguments and exit

time: Module used for displaying real time and delaying program by
inverval

hashlib: Module used for md5 calculations

shutil: Module used for file and folder copying and removing operations
"""
import os
import sys
import time
import hashlib
import shutil


# source
SRC_DIR = sys.argv[1]

# destination
DEST_DIR = sys.argv[2]

# log file
LOG = sys.argv[3]


def main():
    """
    A message will be shown whenever the user gives the wrong inputs,
    or the '-h' or '--help' argument is given

    We must provide at least a source, destination and a log file,
    while the delay interval is optional.
    The interval is in seconds.

    Synchronization will be performed every <DELAY> seconds. At each
    synchronization step, the foreign files will be removed, the 
    modified files will be updated and the missing files/directories
    will be added.
    """
    if len(sys.argv) < 4 or sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print('please give the following arguments:',
            '<source file>',
            '<destination file>',
            '<log file>',
            '<synchronization interval>[seconds] (optional)')
        sys.exit()

    # default delay - 30 seconds
    delay = 30

    # delay if set
    if len(sys.argv) == 5:
        delay = int(sys.argv[4])

    # main synchronization loop
    while True:
        # syncronization function
        synchronize(SRC_DIR, DEST_DIR)
        # wait DELAY seconds after every synchronization
        time.sleep(delay)


def log_update(msg):
    """
    Function called every time a change is made in the folders.

    It shows the real time at the moment of the change, followed
    by the parsed message.

    Every change will be shown in the console/terminal and added
    to the log
    """
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime())
    update = timestamp + ' - ' + msg

    with open(LOG, 'a', encoding='utf-8') as log:
        print(update)
        log.write(update + '\n')


def check_file(f_src, f_dest):
    """
    This function will be called inside the main synchronization
    function. It takes a file from the source and a file from the
    destination folders.

    The MD5s of the files will be compared, and if they are not equal,
    that means a change has been made in one of them.

    The file from destination will be updated and the change will be
    logged.
    """
    with open(f_src, 'rb') as src:
        with open(f_dest, 'r+b') as dest:
            # md5 sums of source and destination file
            s_sum = hashlib.md5(src.read()).hexdigest()
            d_sum = hashlib.md5(dest.read()).hexdigest()

            # compare and update
            if s_sum != d_sum:
                shutil.copy2(f_src, f_dest)

                msg = 'COPIED file ' + f_dest
                log_update(msg)


def synchronize(f_src, f_dest):
    """
    This function is to be called inside a loop, followed by a delay
    of the specified interval. It takes a source and a destination and
    performs syncrhonization.

    First step is the removal of all foreign files. Every item that is
    present in the destination but not in the source shall be removed.
    It performs different operations depending if the item is a
    regular file or a directory.

    The next steps are the addition of missing files and the
    modification of any changed file. These stept are performed at the
    same time.

    It performs different operations for files and directories.
    If the item in question is a regular file, it checks if it is
    missing from the destination list. If the file is missing, it adds
    a copy. Else, it callls the check_file function, which will
    update the file if necessary.

    If the item in question is instead a (sub)directory, it performs
    the same steps. It checks if the directory is missing from the
    destination. If it is missing, creates a copy. If not, it will
    instead update the directory recursively, by calling the function
    with the current path as arguments.
    """
    # list of present items in the source and destination folders
    src_list = os.listdir(f_src)
    dest_list = os.listdir(f_dest)

    # remove foreign files in current directory
    for file in dest_list:
        if file not in src_list:
            # path of current foreign file
            foreigh_path = os.path.join(f_dest, file)

            # if the file in question is not a directory
            if os.path.isfile(foreigh_path):
                # perform a simple file removal operation
                os.remove(foreigh_path)

                # notify that a file has been removed
                msg = 'REMOVED file ' + foreigh_path
                log_update(msg)

            # if the file in question is a directory
            elif os.path.isdir(foreigh_path):
                #recursively remove
                shutil.rmtree(foreigh_path)

                # notify that a subdirectory has been removed
                msg = 'REMOVED subdirecory ' + foreigh_path
                log_update(msg)

    # check if files from the source are modified or missing from dest
    for file in src_list:
        # source and destination paths for current file
        src_path = os.path.join(f_src, file)
        dest_path = os.path.join(f_dest, file)

        # if current file is not a directory
        if os.path.isfile(src_path):
            # if file is missing
            if file not in dest_list:
                # add a copy
                shutil.copy2(src_path, dest_path)

                # notify that a file has been added
                msg = 'ADDED file ' + dest_path
                log_update(msg)

            # if the file is not missing, compare and update
            else:
                check_file(src_path, dest_path)

        # if instead the current file is a directory
        elif os.path.isdir(src_path):
            # if directory is missing
            if file not in dest_list:
                # add a copy
                shutil.copytree(src_path, dest_path)

                msg = 'ADDED subdirecory ' + dest_path
                log_update(msg)

            # if directory is not missing, recursively synchronize
            else:
                synchronize(src_path, dest_path)


if __name__ == '__main__':
    main()
