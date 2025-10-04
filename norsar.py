# -*- coding: utf-8 -*-

import norsar_log
import sys, os, subprocess, pyodbc
from pathlib import Path
from shutil import move, copy
from win32file import CreateFile, CloseHandle
from win32con import GENERIC_READ, GENERIC_WRITE, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL

DIR_IMPORT = "C:\\temp"

# Exit codes for this program
class ExitStatus: Success, Running, Error = range(3)

class NorsarContext():
    # Define a class used to hold contextual information    
    def __init__(self, script_dir):                    
        # Declare variables for all norsar directories, and create them if they don't exist already
        self.directory_script = script_dir
        self.directory_import = Path(DIR_IMPORT)
        self.directory_work = self.directory_script / "work"        
        self.directory_ignore = self.directory_script / "ignore"  
        
        os.makedirs(self.directory_work, exist_ok = True) # Create work directory
        os.makedirs(self.directory_ignore, exist_ok = True) # Create ignore directory
        
def has_exclusive_access(filename):    
    # Check if we have exclusive access to a file
    try:
        handle = CreateFile(str(filename), GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, None)
        CloseHandle(handle)
    except:
        return False            
    return True

def fetch_files(log, ctx):    
    ifiles = ctx.directory_import.glob("*.txt")
    for file in ifiles:
        try:
            # If we don't have full access to the file, skip it for now
            if not has_exclusive_access(file):
                log.info("Unable to aquire exclusive access to " + str(file))
                continue            
                        
            log.info("Moving file " + str(file) + " to work directory")
            move(file, ctx.directory_work)            
            
        except Exception as ex:
            log.error(str(ex), exc_info=True)
            
    return ctx.directory_work.glob("*.txt")

def analyze_file(log, ctx, file):
    log.info("Analyzing file " + str(file)) 
    copy(ctx.directory_script / "c1_def.INP", ctx.directory_script / "IO_BUFF.$$$")
    move(file, ctx.directory_script / "CTBTphd.txt")
    log.info("Running ctbtcon.exe") 
    subprocess.run([str(ctx.directory_script / "ctbtcon.exe")])
    log.info("Running gamma.exe") 
    subprocess.run([str(ctx.directory_script / "gamma.exe")])
    log.info("Analysis done")     

def ignore_file(log, ctx, file):
    log.info("Ignoring file " + str(file))
    move(file, ctx.directory_ignore)                

def import_file(log, ctx, file):    
    found = False
    with file.open() as fd:    
        lines = [line.rstrip() for line in fd]
    for i in range(len(lines)):
        if lines[i] == "#Header 3":
            if lines[i+1].endswith("FULL"):
                analyze_file(log, ctx, file)
                found = True
                break
    if found == False:
        ignore_file(log, ctx, file)            
    
def import_norsar_files():    
    try:        
        log = norsar_log.create_log("norsar")   
        log.info("=========== START IMPORT ===========")
        
        ctx = NorsarContext(Path(__file__).parent.absolute())                        
        files = fetch_files(log, ctx)
        for file in files:
            import_file(log, ctx, file)
        
        log.info("=========== END IMPORT ===========")
        sys.exit(ExitStatus.Success)    
    except Exception as ex:            
        print(str(ex))    
        sys.exit(ExitStatus.Error)        

if __name__ == "__main__":
    import_norsar_files()
