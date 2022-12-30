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
    print(bcolors.BOLD + 'Provide the source file : \n' + bcolors.ENDC)
        
    print('\t-f <filename> | specify the targeted file')
    print('\t--file=<filename> | specify the targeted file')
    
    print('\n\t--- Or provide a list of files : ---\n')
    
    print('\t-f <filename1> -f<filename2> ...')
    print('\t--file=<filename1> --file=<filename2> ...')
    
    sys.exit()


# Compute and return the hash of the file
def crc(filename):
    prev = 0
    # Open and read binary file
    for line in open(filename, "rb"):
        prev = zlib.crc32(line, prev)
    return "%X" % (prev & 0xFFFFFFFF)

def check_corruption(file, crc_hash):
    if (crc(file) == crc_hash): print(bcolors.OKGREEN + '> The file ' + bcolors.OKBLUE  + bcolors.BOLD + '\"' +  file + '\"' + bcolors.ENDC + bcolors.OKGREEN + ' is not corrupted !' + bcolors.ENDC)
    else : print(bcolors.FAIL + '> The file ' + bcolors.WARNING + bcolors.BOLD + '\"' + file + '\"' + bcolors.ENDC + bcolors.FAIL + ' is corrupted !' + bcolors.ENDC)
    
def process_source_hash(arr_source, arr_hash, dir):
    for file, hash in zip(arr_source, arr_hash):
        path = os.path.join(dir, file)
        check_corruption(path, hash)

def process_source_hash_depth(arr_file, arr_hash, dir):
    print("okay")
    print(dir)
    for path, _, files in os.walk(dir):
        for name in files:
            filename = os.path.join(path, name)
            print(filename) 

def retrieve_file_data(file):
    arr_file, arr_hash = [], []
    
    file = open(file, 'r')
    Lines = file.readlines()
    
    for line in Lines:
        # We split the line with the space separator 
        data = line.split()
        if len(data) == 2:
            arr_file.append(data[0])
            arr_hash.append(data[1])
    
    return arr_file, arr_hash

def process_sfv_file(arr_sfv, depth):
    print(depth)
    print(arr_sfv)
    for file in arr_sfv: 
        dir = os.path.dirname(file)
        arr_file, arr_hash = retrieve_file_data(file)
        if not depth: process_source_hash(arr_file, arr_hash, dir)
        else : process_source_hash_depth(arr_file, arr_hash, dir)
             
            
# main function
def main(argv):
    
    # get the option 
    try:
        opts, args = getopt.getopt(argv[1:], 'hfc:s:d', ['help', 'file=', 'crc=', 'sfv=', 'depth'])
    except getopt.GetoptError: usage(argv[0])
    
    if (len(argv) < 2): usage(argv[0])
    print(args)
    print(opts)
    
    depth = False
    arr_source = []
    arr_sfv = []
    arr_crc_hash = []

    for opt, arg in opts:
        # usage
        if opt in ('-h', '--help'):
            usage(argv[0])
        
        elif opt in ('-f', '--file'):
            arr_source.append(arg)
        
        elif opt in ('-c', '--crc'):
            arr_crc_hash.append(arg)
        
        elif opt in ('-s', '--sfv'):
            arr_sfv.append(arg)
            
        elif opt in ('-d', '--depth'):
            depth = True
    
    
    print()
    process_source_hash(arr_source, arr_crc_hash, '')
    process_sfv_file(arr_sfv, depth)


if __name__ == '__main__':
    main(sys.argv)
