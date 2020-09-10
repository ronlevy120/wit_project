# wit_project - VCS Repository Management for Go
Manage repos to control changes with ease through a command-line interface.
This Program will create a Wit folder inside the folder you would like to backup. inside this folder, you will find the Staging area folder, which contains all the files the user specifically asked to backup. In addition, an Image folder will be created, which contains an "image", a copy of the commited files.
The code was written in Python 3.7.4, on Windows OS.

## Quick usage
Quick usage:
open existing directory which you would like to track on CMD using the following command:

``` cd YOUR_PATH ```

 please notice that the attached wit files notation is ```WIT_FILE_LOCATION```

# Type the follwing command on CMD

## Add files to the staging area

```python "WIT_FILE_LOCATION" add "FILE_TO_ADD_PATH"```

## Commit
This command will create a folder name with a length of 40 characters, using only digits 0-9 and letters a-f.
```MESSAGE``` is the message you would like to add to the commit.

```python "WIT_FILE_LOCATION" commit MESSAGE```

## Status
check your repository status

```python "WIT_FILE_LOCATION" status```

## remove files from the staging area 
python "WIT_FILE_LOCATION" rm "FILES_TO_REMOVE"

## Checkout
Copy all files from ```COMMIT``` to parent folder.
```python "WIT_FILE_LOCATION" checkout COMMIT```

## Graph
Show a graph of the relations between commits. at ```--all``` to see all relations in the repository.
```python "WIT_FILE_LOCATION" graph```

## Create a branch
To test and add specific qualities to the code.
```python "WIT_FILE_LOCATION" branch BRANCH_NAME```

## Merge branches
```python "WIT_FILE_LOCATION" merge BRANCH_NAME```
