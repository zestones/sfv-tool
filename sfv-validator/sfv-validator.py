#!/usr/bin/python

# import
import getopt
import zlib
import time
import copy
import sys
import os
import re

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
    
    print(bcolors.BOLD + 'Provide source file and hash : \n' + bcolors.ENDC)  
    print('\t-f <filename> -c <crc_hash> | specify the targeted file and the hash')
    print('\t--file=<filename> -crc=<crc_hash> | specify the targeted file and the hash')
    
    print('\n\t--- Or provide a list of source and hash : ---\n')
    print('\t-f <filename> -c <crc_hash> -f <filename> -c <crc_hash> ... | specify the targeted file and the hash')
    print('\t--file=<filename> -crc=<crc_hash> --file=<filename> -crc=<crc_hash>... | specify the targeted file and the hash')
    
    print(bcolors.BOLD + '\nprovide SFV files : \n' + bcolors.ENDC)
    
    print('\t-s <sfv-file>')
    print('\t--sfv=<sfv-file>')
    
    print('\n\t--- Or give a list of SFV files : ---\n')
    
    print('\t-s <sfv-file> -s <sfv-file> ...')
    print('\t--sfv=<sfv-file> --sfv=<sfv-file>\n')
    
    print(bcolors.BOLD + 'If you want to chech files in subfolders use :\n' + bcolors.ENDC)
    print('\t-d | tell the programe to search source files in subfolders')
    print('\t-depth | tell the programe to search source files in subfolders')
    
    sys.exit()


# Compute and return the hash of the file
def crc(filename):
    prev = 0
    # Open and read binary file
    for line in open(filename, "rb"):
        prev = zlib.crc32(line, prev)
    
    crc32 = "%X" % (prev & 0xFFFFFFFF)
    zero = ''.join('0' for _ in range (8 - len(crc32)))
    return (zero + crc32)

def retrieve_file_data(file):
    arr_file, arr_hash = [], []

    file = open(file, 'r')
    Lines = file.readlines()
    for line in Lines:
        # We split the line with the space separator 
        data = re.split(' ', line)
        
        if len(data) == 2:
            arr_file.append(data[0])
            arr_hash.append(data[1].strip())
    
    return arr_file, arr_hash

def check_corruption(file, crc_hash):
    if not os.path.isfile(file):
        print(bcolors.FAIL + '> File ' + bcolors.WARNING + bcolors.BOLD + '\"' + file + '\"' + bcolors.ENDC + bcolors.FAIL + ' not found !' + bcolors.ENDC)
        return

    if (crc(file).lower() == crc_hash): print(bcolors.OKGREEN + '> The file ' + bcolors.OKBLUE  + bcolors.BOLD + '\"' +  file + '\"' + bcolors.ENDC + bcolors.OKGREEN + ' is not corrupted !' + bcolors.ENDC)
    else : print(bcolors.FAIL + '> The file ' + bcolors.WARNING + bcolors.BOLD + '\"' + file + '\"' + bcolors.ENDC + bcolors.FAIL + ' is corrupted !' + bcolors.ENDC)
    
def process_source_hash(arr_source, arr_hash, dir):
    for file, hash in zip(arr_source, arr_hash):
        path = os.path.join(dir, file)
        print(path)
        check_corruption(path, hash)

def process_source_hash_depth(arr_file, arr_hash, dir):
   
    arr_source = []
    # get all the files in the subfolders 
    for path, _, files in os.walk(dir):
        for name in files: arr_source.append(os.path.join(path, name))

    cpy_files = copy.deepcopy(arr_file)
    corrupted = True
    # search for the non corrupted files
    for file, hash in zip(arr_file, arr_hash):
        for source in arr_source:
            if os.path.basename(source) == file:
                if crc(source) == hash:
                    print(bcolors.OKGREEN + '> The file ' + bcolors.OKBLUE  + bcolors.BOLD + '\"' +  file + '\"' + bcolors.ENDC + bcolors.OKGREEN + ' is not corrupted !' + bcolors.ENDC)
                    corrupted = False
                    arr_source.remove(source)
                    cpy_files.remove(file)
                    break
        if not corrupted: corrupted = True
    
    if cpy_files != []: print(bcolors.FAIL + bcolors.BOLD + '\n----------\n Some file(s) are corrupted : \n----------\n' + bcolors.ENDC)
    # Display the corrupted files founded
    for file in cpy_files:
        for source in arr_source:
            if os.path.basename(source) == file: 
                print(bcolors.FAIL + '> The file ' + bcolors.WARNING + bcolors.BOLD + '\"' + file + '\"' + bcolors.ENDC + bcolors.FAIL + ' is corrupted !' + bcolors.ENDC + bcolors.BOLD + '\n\tPath : ' + source + bcolors.ENDC)
                arr_source.remove(source)
 
def process_sfv_file(arr_sfv, depth):
    for file in arr_sfv: 
        dir = os.path.dirname(file)
        
        if not os.path.isfile(file):
            print(bcolors.FAIL + '> Cannot open ' + bcolors.WARNING + bcolors.BOLD + '\"' + file + '\"' + bcolors.ENDC + bcolors.FAIL + ' .SFV not found !' + bcolors.ENDC)
            continue
        
        arr_file, arr_hash = retrieve_file_data(file)
        if not depth: process_source_hash(arr_file, arr_hash, dir)
        else : process_source_hash_depth(arr_file, arr_hash, dir)

# main function
def main(argv):
    
    # get the option 
    try:
        opts, _ = getopt.getopt(argv[1:], 'hf:c:s:d', ['help', 'file=', 'crc=', 'sfv=', 'depth'])
    except getopt.GetoptError: usage(argv[0])
    
    if (len(argv) < 2): usage(argv[0])
      
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
    begin = time.time()
    process_source_hash(arr_source, arr_crc_hash, '')
    process_sfv_file(arr_sfv, depth)
    end = time.time()
    print()

    print(bcolors.OKGREEN + '================================================================')
    print('> Done !')
    print('> Execution time : ', end='')
    print('%.2f' % (end - begin), end='s\n')
    print('================================================================' + bcolors.ENDC)

if __name__ == '__main__':
    main(sys.argv)
