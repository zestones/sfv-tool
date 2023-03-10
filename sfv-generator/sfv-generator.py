#!/usr/bin/python

# import
import getopt
import time
import zlib
import sys
import os

# colors 
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
POSITIVE_ANSWER = 'y'
OUTPUT_FILENAME = 'auto-generated'

# usage message
def usage(program):
    print(bcolors.HEADER + 'Usage : ' + program + bcolors.ENDC)
    print(bcolors.BOLD + 'Provide a file : \n' + bcolors.ENDC)
        
    print('\t-f <filename> | specify the targeted file')
    print('\t--file=<filename> | specify the targeted file')
    
    print('\n\t--- Or provide a list of files : ---\n')
    
    print('\t-f <filename1> -f<filename2> ...')
    print('\t--file=<filename1> --file=<filename2> ...')
    
    print(bcolors.BOLD + '\nProvide a directory : \n' + bcolors.ENDC)
    print('\t-d <directory>')
    print('\t--directory=<directory>')
    
    print('\n\t--- Or provide a list of directories : ---\n')
    
    print('\t-d <directory1> -d <directory2> ...')
    print('\t--directory=<directory1> --directory=<directory2> ...')
    
    print(bcolors.BOLD + '\n\tLevel of search : \n' + bcolors.ENDC)
    print('\t-l <integer> | The files will be searched in the depth <integer>')
    print('\tIf you dont provide a level, it will be set to 0 by default')
    
    print(bcolors.BOLD + '\nProvide an output directory : \n' + bcolors.ENDC)
    print('\t-o <outputfolder> | the generated files will be created in <directory>')
    
    print(bcolors.BOLD + '\nProvide an output file : \n' + bcolors.ENDC)
    print('\t-o <outputfile> | the content will be writed inside the file')
    
    print(bcolors.BOLD + '\nOutput files : \n' + bcolors.ENDC)
    print('\t-s | Adding this option will generate one sfv file for all provided files')
    print('\tIf you want to have one sfv file for each provided file don\'t add this option')
    
    sys.exit()

# os walk re-definition with level
def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]

# Compute and return the hash of the file
def crc(filename):
    prev = 0
    # Open and read binary file
    for line in open(filename, "rb"):
        prev = zlib.crc32(line, prev)
    
    crc32 = "%X" % (prev & 0xFFFFFFFF)
    zero = ''.join('0' for _ in range (8 - len(crc32)))
    return (zero + crc32)
     
def error_file_exist(file, source_file):
    print(bcolors.WARNING + 'The file \"' + bcolors.BOLD + file + '\" already exist.' + bcolors.ENDC)
    if source_file != '': print(bcolors.BOLD + 'The source file is : ' + bcolors.FAIL + source_file + bcolors.ENDC)
    
    response = input(bcolors.BOLD + '> Do you want overwrite it ? Y/N ' + bcolors.ENDC)
    return response.lower()

# write/create the the content of the sfv file 
def write_sfv(dir_to_file, content):
        
    os.makedirs(os.path.dirname(dir_to_file), exist_ok=True)
    
    f = open(dir_to_file, 'w+')
    f.write(content)
    f.close()

# processs the files passed in parameter
def process_files(arr_files, separated, output_dir):
    header = '; author : zestones -- open source code : https://github.com/zestones/sfv-tool\n\n'
    content, ext = '', '.sfv'
    
    if(not separated): 
        content = header
        print(bcolors.OKCYAN + '-------------------------------------------------------------' + bcolors.BOLD)
        print(bcolors.OKCYAN + '---( Creating : ' +  (OUTPUT_FILENAME + ext) + ' )---' + bcolors.ENDC)
        print(bcolors.OKCYAN + '-------------------------------------------------------------' + bcolors.BOLD)
        
    for file in arr_files:
        if (os.path.isdir(file)):
            print(bcolors.WARNING + "> " +  file + " : " + bcolors.FAIL + "Folders can't be processed !" + bcolors.ENDC)
            continue
        elif not os.path.isfile(file):
            print(bcolors.FAIL + '> File ' + bcolors.WARNING + bcolors.BOLD + '\"' + file + '\"' + bcolors.ENDC + bcolors.FAIL + ' not found !' + bcolors.ENDC)
            continue
        
        crc_value = crc(file)
        filename = os.path.basename(file)
       
        if (not separated): 
            content += filename + ' ' + crc_value + '\n'
            print(bcolors.OKBLUE + '> Adding : ' + filename + bcolors.ENDC)
        else:
            if output_dir == './': path = file
            else : path = filename          
            # extract the name and the extension of the file
            name, _ = os.path.splitext(path)
            # set the content of the file
            content = header + filename + ' ' + crc_value + '\n'
            # the sfv file path
            dir_to_file = output_dir + '/' + name + ext
            if (os.path.isfile(dir_to_file) and error_file_exist(dir_to_file, file) != POSITIVE_ANSWER): continue
            print()
            print(bcolors.OKCYAN + '-------------------------------------------------------------' + bcolors.BOLD)
            print(bcolors.OKCYAN + '---( Creating : ' +  (name + ext) + ' )---' + bcolors.ENDC)
            print(bcolors.OKCYAN + '-------------------------------------------------------------' + bcolors.BOLD)

            print(bcolors.OKBLUE + '> Adding : ' + filename + bcolors.ENDC)
            
            # write the file content
            write_sfv(dir_to_file, content)
   
    if(not separated):    
        name = OUTPUT_FILENAME
        dir_to_file = output_dir + '/' + name + ext
        if (os.path.isfile(dir_to_file) and error_file_exist(dir_to_file, "") != POSITIVE_ANSWER): return
        
        write_sfv(dir_to_file, content)

# processs the directory passed in parameter
def process_directory(arr_dir, arr_ext, separated, output_dir, level):
    arr_files = []
    # retrieve the files inside the directories
    for dir in arr_dir:
        if not os.path.isdir(dir):
            print(bcolors.FAIL + '> Folder ' + bcolors.WARNING + bcolors.BOLD + '\"' + dir + '\"' + bcolors.ENDC + bcolors.FAIL + ' not found !' + bcolors.ENDC)
            continue
        
        # retrieve the files in the directory
        for path, _, files in walklevel(dir, level):
            for file in files:      
                _, ext = os.path.splitext(file)
                if arr_ext != []:
                    if ext in arr_ext: arr_files.append(os.path.join(path, file))
                else: arr_files.append(os.path.join(path, file))
        
        # if there is no files inside the folder continue
        if (arr_files == []): continue
        # if there is no output provided, create SFV file inside each given folder
        if (output_dir == './'):
            if separated: process_files(arr_files, separated, output_dir)
            else : process_files(arr_files, separated, dir)
            arr_files = []
   
   # if an output file is given, redirect output to that directory
    if (output_dir != './'):
        if (arr_files == []): return
        process_files(arr_files, separated, output_dir)

# main function
def main(argv):
    # get the option 
    try:
        opts, _ = getopt.getopt(argv[1:], 'hsd:f:o:l:e:O:', ['help', 'file=', 'directory=', 'outputfolder=', 'separated=', 'level=', 'extension=', 'outputfile='])
    except getopt.GetoptError: usage(argv[0])
    
    if (len(argv) < 2): usage(argv[0])
    
    global OUTPUT_FILENAME
    arr_files = []
    arr_dir = []
    arr_ext = []
    output_dir = './'
    separated = True
    level = 0
    
    for opt, arg in opts:
        # usage
        if opt in ('-h', '--help'):
            usage(argv[0])
        
        elif opt in ('-f', '--file'):
            arr_files.append(arg)
            
        elif opt in ('-d', '--directory'):
            arr_dir.append(arg)
        
        elif opt in ('-o', '--outputfolder'):
            output_dir = arg
        
        elif opt in ('-s', '--separated'):
            separated = False
        
        elif opt in ('-l', '--level'):
            level = int(arg)
        
        elif opt in ('-e', '--extension'):
            arr_ext.append(arg)
        elif opt in ('-O', '--outputfile'):
            OUTPUT_FILENAME = arg
    
    print()
    begin = time.time()
    if (arr_files != []): process_files(arr_files, separated, output_dir)
    if (arr_dir != []): process_directory(arr_dir, arr_ext, separated, output_dir, level)
    end = time.time()
    print()
   
    print(bcolors.OKGREEN + '================================================================')
    print('> Done !')
    print('> Execution time : ', end='')
    print('%.2f' % (end - begin), end='s\n')
    print('================================================================' + bcolors.ENDC)

if __name__ == '__main__':
    main(sys.argv)
