########### General file handling utilities
import time
import sys
import os
import stat
import gzip
import pandas as pd
from shutil import which, rmtree, copyfile
import traceback

SCRIPT_VERSION = 1.12 #add 'fq' extension

script_base = os.path.basename(__file__)
_outputBase = '{}_v{}'.format(os.path.splitext(script_base)[0],SCRIPT_VERSION)


class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.filename = filename
        renameWithTimestamp(self.filename)
        open(self.filename, 'a').close()
        try:
            log = open(self.filename, "a")
            log.write("#### Command  ######## Initiated at {} ####\n".format(time.ctime()))
            log.write(" ".join(sys.argv)+"\n\n")
            log.close()
        except IOError:
            print("ERROR: Log not initiated. Unable to write to {}".format(self.filename))
            self.filename = None
        
    def __getattr__(self, attr): return getattr(self.terminal, attr)

    def write(self, message):
        self.terminal.write(message)
        if self.filename is not None:
            try:
                log = open(self.filename, "a")
                log.write(message)
                log.close()
            except IOError:
                self.terminal.write("ERROR: No log being kept. Unable to write to {}".format(self.filename))
                ##Print Wolud get into infinite exception loop
        
def flexible_handle(filename,compression=False,mode='rt'):
    if compression:
        return gzip.open(filename,mode)
    else:
        return open(filename,mode)

########## Python
required_python = 3
preferred_python = 4     
def has_preferred_python():
    thispy = sys.version_info
    valid = False
    if thispy.major >= required_python:
        valid = True
        if thispy.minor < preferred_python:
            print('This script was developed on python {}.{}. You are using {}. The script will run, but may have erratic behavior. Please load/install a more recent version'.format(required_python,preferred_python,thispy))
    else:
        print('This script was developed on python {}.{}. You are using {}. Please load/install a more recent version'.format(required_python,preferred_python,thispy))
    return valid
    

def appendToFilename(filename,insert):
    (base, ext) = os.path.splitext(filename)
    if ext == '.gz':
        (base,ext2) = os.path.splitext(base)
        ext = ext2 + ext
    return base + insert + ext 
    
##New_ext should include the dot
def setExt(filename,new_ext,decompress=False):
    if decompress:
        (name,gz) = os.path.splitext(filename)
        if gz == '.gz':
            filename = name
        else:
            print("Warning: supposedly compressed file needing new extension does not end with gz")
    (base, _) = os.path.splitext(filename)
    if not new_ext[0] == '.':
        new_ext = '.'+new_ext
    return base + new_ext 

def renameWithTimestamp(filename):
    result = False
    if os.path.isfile(filename):
        TimeStmp = time.localtime(os.path.getmtime(filename))
        newName = appendToFilename(filename,"_"+time.strftime("%Y%m%d%H%M%S",TimeStmp))
        try:
            os.rename(filename,newName)   
        except Exception as e:
            result = False
            print("Unable to add timestamp to file: "+ filename)
            print("\t{}".format(e))
        else:
            result = True
    return result

## Avoid overwriting files (ToDo, ask for a response from user)
def checkForOverwrite(filename,force=False,_verbose=True):
    if os.path.isfile(filename):
        if force:
            if _verbose:
                print("Deleting old output file: {}".format(filename))
            os.remove(filename)
        else:
            filename = renameWithTimestamp(filename)
            if os.path.isfile(filename):
                raise Exception("Output file {} is in the way".format(filename))
    return filename

## Utility to update records while preserving old files
def safeOverwriteCSV(filename, df, **kwargs):
    assert isinstance(df,pd.DataFrame), "Must provide dataframe"
    safeOverwriteTable(filename,df,'csv',**kwargs)
    
def safeOverwriteTable(filename, df, out_fmt, **kwargs):
    assert isinstance(df,pd.DataFrame), "Must provide dataframe"
    if os.path.splitext(filename)[1] == '':
        filename += '.'+out_fmt
    renameWithTimestamp(filename) 
    try:
        if  os.path.exists(filename):
            filename = appendToFilename(filename,"_"+time.strftime("%Y%m%d%H%M%S"))
        if out_fmt == 'csv':
            df.to_csv(filename, **kwargs)
        elif out_fmt == 'tab':
            df.to_csv(filename, sep='\t',**kwargs)
        elif out_fmt == 'excel':
            filename = setExt(filename, 'xlsx') ##Pandas needs to have the extension
            df.to_excel(filename, **kwargs)
        elif out_fmt == 'json':
            df.to_json(filename,**kwargs) ##JSON does not take "index" as keyword
        else:
            raise ValueError("Need another format: {}".format(out_fmt))
        os.chmod(filename, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
    except IOError:
        print("\nERROR: Unable to write to {}\n".format(filename))
        result = False
    else:
        result = True
    return result

import re
def makeSafeName(filename):
    safe_name = re.sub(r'[()*&%#@{}[\]| ><?*:;"'']','_',filename)
    return safe_name.replace('/','-')

def linkWithSafeFilename(filename,out_dir=None):
    d = os.path.dirname(filename)
    b = os.path.basename(filename)
    safename = makeSafeName(b)
    safepath = os.path.join(d,safename)
    if not os.path.exists(safepath):
        os.link(filename,safepath)
    return safepath    
    
    
def safeMakeDir(dirname):
    if not os.path.isdir(dirname):
        if not os.path.exists(dirname):
            os.makedirs(dirname)  
        else:
            raise IOError("File exists. Cannot make directory: "+dirname)  

def safePathExists(path):
    return isinstance(path,str) and os.path.exists(path)

def safeChangePathBase(path,old_base,new_base):
    result = path
    if isinstance(result,str) and result.startswith(old_base):
        result = os.path.join(new_base,path[len(old_base):])
    return result
        
##Usage: files is either a single filename or list of filenames
##FreshDir will first remove the destination directory
## The value NONE can be passed as placeholder in the filelist
def addLinksToDir(files,out_directory,freshDir=False,copy_if_fail=False):
    filelist = files if isinstance(files,list) else [files]
    #setup directory
    if freshDir and os.path.isdir(out_directory):
        rmtree(out_directory)
    safeMakeDir(out_directory)
    #make lists
    dest_links = []
    for f in filelist:
        if pd.notnull(f):
            b = os.path.basename(f)
            if b == '':
                dest = None
            else:
                dest = os.path.join(out_directory,b)
        else:
            dest = None
        dest_links.append(dest)
    try:
#         print("Making linkes")
        makeLinks(filelist,dest_links,make_dest_dirs=freshDir,updating=(not freshDir),copy_if_fail=copy_if_fail)
    except ValueError:
        if freshDir and os.path.isdir(out_directory):
            rmtree(out_directory)
        raise
    return dest_links

def appendToColumns(df,suffix,exclude=None):
    assert isinstance(df, pd.DataFrame)
    assert isinstance(suffix,str)
    if exclude is None:
        exclude = []
    assert isinstance(exclude,list)
    columns = [x for x in df.columns if x not in exclude]
    r_cols = {c: c+suffix for c in columns}
    return df.rename(columns=r_cols)
        
from filecmp import cmp
##Update allows file to be renamed to avoid collisions. If you want to delete old files, my recommendation is to write to a fresh directory.
# The value NONE can be passed to both source and dest as placeholder 
def makeLinks(source_files,dest_links,make_dest_dirs=False,updating=False,copy_if_fail=False):
    ##Validate
    if not (len(source_files) == len(dest_links)):
        raise ValueError("The source and destination lists must be equal length")
    ###TODO: this gets mixed up if "none" is in the list
    if not (len(source_files) == len(set(source_files))):
        raise ValueError("Items in the source list must be unique.")
    if not (len(dest_links) == len(dest_links)):
        raise ValueError("Items in the destination list be unique.")
    for f in source_files:
        if (f != None):
            if (not isinstance(f,str)):
                raise ValueError("Filename value passed to makeLinks is not a string")
            elif not os.path.isfile(f):
                raise ValueError("Filename value passed to makeLinks is not a file location") 
    ##Check for legit desitination names; rename if requested
    final_dest = []
    for src, dest in zip(source_files,dest_links):
        if not ((src is None) == (dest is None)):
            raise ValueError("Source and Destination locations must be same type (either None or string)")
        ##Is string
        if not isinstance(dest,str):
            raise ValueError("Link value passed to makeLinks is not a string")
        ## make directory if requested
        dest_dir = os.path.dirname(dest)
        if not os.path.isdir(dest_dir):
            if make_dest_dirs:
                os.mkdir(dest_dir)
            else:
                raise ValueError("Link destination directory does not exist")
        ## copy file (rename if needed)        
        my_dest = dest
        if os.path.exists(my_dest):
            if updating:
                ##Avoid name conflicts
                i = 1
                while (os.path.exists(my_dest)) and (i < 10) and (not cmp(src,my_dest)):
                    my_dest = appendToFilename(dest, '_{}'.format(i))
                    i += 1  
            else:               
                raise ValueError("Link value passed to makeLinks already exists")
        final_dest.append(my_dest)
        ## copy the file
        if  os.path.exists(my_dest): ##Do nothing if identical, need to check if it exists to avoid error in cmp
            if not cmp(src,my_dest):
                raise  ValueError("Link exists and is not identical: {}".format(my_dest)) 
        else:
            try:
                os.link(src,my_dest)
            except OSError:
                if copy_if_fail:
                    copyfile(src,my_dest)
                else:
                    print("Failed to link. Updating: ".format(updating))
                    raise          
#         os.chmod(my_dest, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)  
    if not (len(source_files) == len(final_dest)):
        raise ValueError("The source and destination lists must be equal length")            
#     for src,f_dest in zip(source_files,final_dest):    

    return final_dest
            
    
def safeMakeOutputFolder(basename):
    folder = os.path.join(os.getcwd(),basename+"_"+time.strftime("%Y%m%d%H%M%S"))
    safeMakeDir(folder)
    return folder

format_guesser = { '.fasta' : 'fasta',
            '.fa'   : 'fasta',
            '.fastq' : 'fastq',
            '.fq' : 'fastq',
            '.gb' : 'gb',
            '.gbk' : 'gb',
            '.fna' : 'fasta',
            '.embl': 'embl'
            }
##Print exception details. Pass Exception as e
def printExceptionDetails(e,warn=None):
    if warn is None:
        warn='Exception'
    print("{}: {}".format(warn,e))
    print("at line:")
    traceback.print_tb(sys.exc_info()[2])
    traceback.print_exc()

def guessFileFormat(filename):
    (base,ext) = os.path.splitext(filename)
    compressed = False
    if ext == '.gz':
        compressed = True
        (base,ext) = os.path.splitext(base)
    if ext in format_guesser:
        seq_format = format_guesser[ext]
    else:
        seq_format = None
    return seq_format, compressed

def castColumnsToBool(df,boolCol,trueValue):
    assert isinstance(df,pd.DataFrame)
    assert isinstance(boolCol,list) #assume list of string
    assert len(boolCol) > 0 
    assert isinstance(trueValue,list)#assume list of string
    assert len(trueValue) > 0
    for c in boolCol:   
        df[c] = df[c].isin(trueValue) if c in df.columns else False
    return df

##Selecting fields from Pandas; avoiding null and text
 
def avoidItemsThatStartWith(df,col,str_start):
    not_values = df[col].isnull() ##TODO: this should probably be broader and drop everything that is not a string
    avoid_strings = df[col].str.startswith(str_start) ##Anything that is not HTTP is made relative
    return ~(not_values | avoid_strings)                
    

def is_exe(fpath):
    return isinstance(fpath,str) and os.path.isfile(fpath) and os.access(fpath, os.X_OK)

def find_executable(default_names,search_paths,PATH_first=True):
    on_path = None
    for n in default_names:
        on_path = which(n)
        if is_exe(on_path):
            break
    if PATH_first and is_exe(on_path):
        return on_path
    else:
        for p in search_paths:
            if is_exe(p):
                return(p)
    return on_path
    