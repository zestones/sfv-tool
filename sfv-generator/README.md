# sfv-generator

This tool enable you to generate SFV easily for your files. Let's see how to use this script.

## **How to use it ?**

First of all clone this repository.

```bash
# clone the repo
git clone git@github.com:zestones/sfv-tool.git
```

You can see how to use the program by executing this command: 

```bash
# see how to use the script
python3 sfv-generator.py -h 
```

### **Options**

| Option | Description |
| :------------- | :------------- |
| ``--help`` (``-h``)  | Show help  |
| ``--file`` (``-f``)  |  Provide a file |
| ``--directory`` (``-d``)  |  Provide a folder |
| ``--output`` (``-o``)  |  Specify an output |
| ``--separated`` (``-s``)  |  Merge the output |
| ``--level`` (``-l``)  |  Specify the search depth |

Let's see in details how to use these options.

### **Providing files**

You can provide a file like below :

```
python3 sfv-generator.py -f myfile.ext
```

The SFV will be created in the folder of the provided file, if you want to redirect the output in a new or different folder add the option ``--output``.


```
python3 sfv-generator.py -f myfile.ext -o ./myfolder/
```

You can also give a list of file :

```
python3 sfv-generator.py -f myfile-1.ext -f myfile-2.ext -o ./myfolder/
```
Then, you should have the following folder structure :

```
myfolder
│   myfile-1.sfv
│   myfile-2.sfv 
```

If you want to merge the the output you can add the ``--separated`` option :

```
python3 sfv-generator.py -s -f myfile-1.ext -f myfile-2.ext -o ./myfolder/
```
This way the output will be redirected inside an unique file, your folder structure will be :

```
myfolder
│   auto-generated.sfv
```


### **Providing Folders**

If you want to generate SFV for all files inside a folder you can use the ``--directory`` option to provide a folder to the program.

The usage is the same as for the files, you can provide a unique folder or a list of folder. And merge the output if you want only one SFV file.

```bash
# generate SFV file for each file inside "./folder"
python3 sfv-generator.py -d ./folder

# generate SFV file for each file inside "./folder" and redirect the output to "./newFolder"
python3 sfv-generator.py -d ./folder -o ./newFolder

# generate SFV file for each file inside "./folder" and redirect the output to "./newFolder" (the output is merged in a single file)
python3 sfv-generator.py -s -d ./folder-1/ -d ./folder-2/ -o ./newfolder/
```

> **NOTE**  
>
> When you don't give an output the SFV files are created in the directory of the source file. 
> 

> **WARNING**
> 
> If you provide multiple folders without an ouput directory there is two possibility : 
>
> **1.** You use the ``--separated`` option (``-s``) to merge the output, then the SFV will be created inside the parent folder.
>
> **2.** You dont use the -s option, then each SFV will be created were the source file is located.
>
> This **warning** apply only if you set the ``--level`` of search, otherwise the SFV will be generated inside the parent directory given in parameter.   

By default the program search inside the folder provided but do not check the content of subfolders. If you have subfolders and want to generate SFV file for them you can provide the search depth with the ``--level`` option. 

In the example below, the program will search to a depth of 2. 
```
python3 sfv-generator.py -l 2 -d ./folder
```

Sometimes you may want to generate SFV files by providing a folder but not on all the files. You can filter the files by their extension, for that just use the ``--extension`` option.

As for the --file or the --directory option you can provide a list of extensions. This way you will generate SFV file for all the files inside the directory that has the extension specified.

```bash
# specify a file extension
python3 sfv-generator.py -e .zip -d ./folder

# specify a list of extension
python3 sfv-generator.py -e .zip -e .rar -e .tar -d ./folder
```
> **WARNING**  
>
> This option should be used only with the ``--directory`` option (there is no use to use it with the ``--file`` option).


## **Usage advice**
* Use the ``--help`` (``-h``) option to show how to use the program.  
* Note that the ``--level`` (``-l``) option should not be used with the option ``--file`` (``-f``). 
> **WARNING**  
>
> You should not mix ``-f`` and ``-d`` options.
>
>  When providing a list of files or folders, be sure to add the ``-f`` or ``-d`` option before each file or folder.
