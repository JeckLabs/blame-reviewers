# Blame Reviewers
Small CLI tool for finding appropriate reviewers by searching authors of changed code in git blame.

## Requirements
* python >= 3.7
* [sh](https://pypi.org/project/sh/) >= 1.12.13

## Installation

```bash
pip3 install blame-reviewers
```

## Usage
In the branch of your repo run:
```
➜ ~ git:(awesome-branch) blame-reviewers
Blaming src/filename.py 19,+10...
Blaming src/another_filename.py 1,+132...
Blaming src/and_one_more_file.py 69,+14...

  Birdie Weissnat      Birdie.Weissnat@example.org    35.1093
   Alfreda Klocko       Alfreda.Klocko@example.org    22.141
     Erwin Rempel         Erwin.Rempel@example.org    20.259
    Myah Schmeler        Myah.Schmeler@example.org    19.201
Frederik Schimmel    Frederik.Schimmel@example.org    17.71
   Amalia Gleason       Amalia.Gleason@example.org     3.18
  Raymond Wuckert      Raymond.Wuckert@example.org     3.9
```