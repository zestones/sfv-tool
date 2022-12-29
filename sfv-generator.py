#!/usr/bin/python

# import
import getopt
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
    print('\t-o <directory> | the generated files will be created in <directory>')
    
    print(bcolors.BOLD + '\nOutput files : \n' + bcolors.ENDC)
    print('\t-s | Adding this option will generate one sfv file for all provided files')
    print('\tIf you want to have one sfv file for each provided file don\'t add this option')
    
    sys.exit()

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
    return "%X" % (prev & 0xFFFFFFFF)


def write_sfv(filename, opt, output_dir):
    
    # get the file name from the path
    file = os.path.basename(filename)
  
    if (opt == 'a+'):
        name = 'auto-generated'
    else:
        # extract the name and the extension of the file
        name, _ = os.path.splitext(file)
    
    if (output_dir != ''):
            dir_to_file = output_dir + '/' + name + '.sfv'
            os.makedirs(os.path.dirname(dir_to_file), exist_ok=True)
            f = open(dir_to_file, opt)
    else:
        f = open(name + '.sfv', opt)
        
    crc_value = crc(filename) 
    f.write(file + '\t' + crc_value + '\n')

    f.close()

# processs the files passed in parameter
def process_files(arr_files, separated, output_dir):
        
    if(separated): opt = "w+"
    else: opt = "a+"
    
    for file in arr_files:
        if (os.path.isdir(file)):
            print(bcolors.WARNING + "> " +  file + " : " + bcolors.FAIL + "Folders can't be processed !" + bcolors.ENDC)
            continue
        
        write_sfv(file, opt, output_dir)

# processs the directory passed in parameter
def process_directory(arr_dir, separated, output_dir, level):
    arr_files = []

    # retrieve the files inside the directories
    for dir in arr_dir:
        for path, subdirs, files in walklevel(dir, level):
            for name in files:
                arr_files.append(os.path.join(path, name))
    
    process_files(arr_files, separated, output_dir)

# main function
def main(argv):
    
    # get the option 
    try:
        opts, args = getopt.getopt(argv[1:], 'hsd:f:o:l:', ['help', 'file=', 'directory=', 'output=', 'separated=', 'level='])
    except getopt.GetoptError: usage(argv[0])
    
    arr_files = []
    arr_dir = []
    output_dir = ''
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
        
        elif opt in ('-o', '--output'):
            output_dir = arg
        
        elif opt in ('-s', '--separated'):
            separated = False
        
        elif opt in ('-l', '--level'):
            level = int(arg)
        
    process_files(arr_files, separated, output_dir)
    process_directory(arr_dir, separated, output_dir, level)


if __name__ == '__main__':
    main(sys.argv)
