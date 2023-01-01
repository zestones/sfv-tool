# sfv-validator

This tool enable you to check the integrity of files.

## How to use it ?

```bash
# clone the repo
git clone git@github.com:zestones/sfv-tool.git

# move to the folder
cd ./sfv-tool/sfv-validator/
```

You can see how to use the program by executing this command:

```bash
# clone the repo
python3 sfv-validator.py -h
```

You have two possibility to check the integrity of files you can give the hash and a file to the program or give an .SFV file in parameter.

### **Options**

| Option | Description |
| :------------- | :------------- |
| ``--help`` (``-h``)  | Show help  |
| ``--file`` (``-f``)  |  Provide a file |
| ``--crc`` (``-c``)  |  Provide a file hash |
| ``--sfv`` (``-s``)  |  Provide a SFV file |
| ``--depth`` (``-d``)  |  Specify the search depth |

Let's see in details how to use these options.

#

## Hash and Source file

If you have the hash of a given file you can check if your file is corrupted or not in the following way : 

```bash
# check the integrity of a file
python3 sfv-validator.py -f myfile.txt -c the_hash
```

You can also give multiple files and hash in parameter by adding before each file the ``-f`` option and before each hash the ``-c`` option.

```bash
# check the integrity of a multiple file
python3 sfv-validator.py -f myfile1.txt -c hash1 -f myfile2.zip -c hash2
```

> **NOTE**
> 
> The order is important when you write multiple files and hash, don't mix the hashes and the files.

## SFV file

Checking each file by writing it's name and hash is long. Let's see how to use the .SFV file to check the integrity of lots of files.

The ``--sfv`` (``-s``) option enable you to give an .SFV file in parameter.
The program will read the file and check the integrity of each file inside it.

```bash
# check the integrity of files
python3 sfv-validator.py -s ./auto-generated.sfv
```

You can also provide multiple .SFV file.

```bash
# check the integrity of files
python3 sfv-validator.py -s ./auto-generated.sfv -s ./folder/auto-generated.sfv
```

> **NOTE**
> 
> The files you are trying to check should be with the SFV file in the same folder.

If you used the [sfv-generator](https://github.com/zestones/sfv-tool/tree/main/sfv-generator) tool, you have seen that you can give a ``--level`` of search.
If you used this option, the files listed inside the .SFV are also located in subfolders. To check the integrity of files located in subfolders too, you should use the ``--depth`` option (``-d``).

```bash
# check the integrity of files
python3 sfv-validator.py -d -s ./folder/auto-generated.sfv
```

> **NOTE**
> 
> If you don't use the ``--depth`` option (``-d``) only the files inside the parent folder of the .SFV will be checked.

## Usage advice
* Use the ``--help`` option (``-h``) to show how to use the program.
* Don't mix the ``-f`` and ``-s`` options