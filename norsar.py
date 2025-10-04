# -*- coding: utf-8 -*-

import norsar_log
import sys, os, pyodbc
from pathlib import Path

dir_import = Path("C:\\temp")

# Exit codes for this program
class ExitStatus: Success, Running, Error = range(3)

def fetch_files(log, dirname):
    pass

def import_norsar_files(dirname):    
    try:        
        log = norsar_log.create_log("norsar")   
        log.info("=========== START IMPORT ===========")
        
        dir_script = Path(__file__).parent.absolute() # Path to this script
        dir_work = dir_script / "work" # Path to work directory
        os.makedirs(dir_work, exist_ok = True) # Create work directory
        
        files = fetch_files(log, dirname)
        
        log.info("=========== END IMPORT ===========")
        sys.exit(status)    
    except Exception as ex:            
        print(str(ex))    
        sys.exit(ExitStatus.Error)        

if __name__ == "__main__":
    import_norsar_files(dir_import)
