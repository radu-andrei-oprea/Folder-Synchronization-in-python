# Folder Synchronization

This is a lightweight Python script that allows you to synchronize the contents of a source folder with a destination folder at any desired time interval. It compares and updates the files and directories between the source and destination, adds any missing files to the destination and removes any foreign files from the destination that are not present in the source.

## Prerequisites
- Python 3.x

## Usage
The script takes a **source directory**, a **destination directory**, a text file to use as a **log** and a **time interval** in seconds. If no time interval is set, the script will update the directories every 30 seconds.

In your terminal, run the following :
  
### Windows
In your command block, run the following:

   ``python3 sync.py <source_dir> <destination_dir> <log_file> <sync_interval> (optional)``
  
  ### Unix
  On Unix based platforms, you can also run the following:

  ``./sync.py <source_dir> <destination_dir> <log_file> <sync_interval> (optional)``

## Functions
The script contains the following functions:

### `main()`
The entry point of the script. It checks the command-line arguments and runs the `synchronization()` function at the given interval `DELAY`.
### `log_update(msg)`
It is called whenever a change in the directories is made. It will show the current date, time and time zone, followed by the given message `msg`, which represents the changes made. Each time it is called, it will show the message at command line and append it into the `LOG` file.
### `check_file(f_src, f_dest)`
It is called in order to check whether the source `f_src` has been modified. It computes the MD5 hash values of the files, and if they are not equal, the destination `f_dest` is updated.
### `synchronize(f_src, f_dest)`
Performs the synchronization process by removing any files or directories from `f_dest` that are not present in the `f_src`, adding any missing files or directories to `f_dest`, updating the files by comparing them with `check_file()` and recursively synchronizing the sub directories. Every change will be recorded by calling the `log_update()` function.

## Testing
A Makefile and an archived source directory are also provided for testing purposes.

- **build**: unzips the source and creates a destination directory and a log text file
- **run &lt;DELAY&gt;**: runs the script at specified delay interval; if none is provided, the default time is 30 seconds
- **clean**: removes the files



