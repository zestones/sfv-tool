#!/usr/bin/python

import getopt
import zlib
import sys
import os

# error message
def usage(program):
    print('Usage : ' + program)
    print('Provide a file : \n')
        
    print('\t-f <filename> | specify the targeted file')
    print('\t--file=<filename> | specify the targeted file')
    
    print('\n\t--- Or provide a list of files : ---\n')
    
    print('\t-f <filename1> -f<filename2> ...')
    print('\t--file=<filename1> --file=<filename2> ...')
    
    print('\nProvide a directory : \n')
    print('\t-d <directory>')
    print('\t--directory=<directory>')
    
    print('\n\t--- Or provide a list of directories : ---\n')
    
    print('\t-d <directory1> -d <directory2> ...')
    print('\t--directory=<directory1> --directory=<directory2> ...')
    
    print('\nProvide an output directory : \n')
    print('\t-o <directory> | the generated files will be created in <directory>')
    
    print('\nNumber of files : \n')
    print('\t-s | Adding this option will generate one sfv file for all provided files')
    print('\tIf you want to have one sfv file for each provided file don\'t add this option')
    
    sys.exit()

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

def process_files(arr_files, separated, output_dir):
        
    if(separated): opt = "w+"
    else: opt = "a+"
    
    for file in arr_files:
        write_sfv(file, opt, output_dir)


def main(argv):
    
    try:
        opts, args = getopt.getopt(argv[1:], 'hsd:f:o:', ['help', 'file=', 'directory=', 'output=', 'separated='])
    except getopt.GetoptError: usage(argv[0])
    
    arr_files = []
    arr_dir = []
    output_dir = ''
    separated = True
    
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
            
    process_files(arr_files, separated, output_dir)


if __name__ == '__main__':
    main(sys.argv)
