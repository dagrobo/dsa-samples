# -*- coding: utf-8 -*-

import norsar_log
import sys, os, pyodbc
from pathlib import Path

dir_import = Path("C:\\temp")
dir_script = Path(__file__).parent.absolute()    
dir_work = dir_script / "work"

# Exit codes for this program
class ExitStatus: Success, Running, Error = range(3)

def import_norsar_files(log, dirname):
    os.makedirs(dir_work, exist_ok = True)
    log.info("importing from %s" % dirname)

if __name__ == "__main__":
    try:        
        log = norsar_log.create_log("norsar")   
        log.info("=========== START IMPORT ===========")
        status = import_norsar_files(log, dir_import)
        log.info("=========== END IMPORT ===========")
        sys.exit(status)    
    except Exception as ex:            
        print(str(ex))    
        sys.exit(ExitStatus.Error)    
