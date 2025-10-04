# -*- coding: utf-8 -*-

import sys
from pathlib import Path
from norsar_log import create_log
from norsar_context import NorsarContext
from norsar_fetch_files import fetch_files
from norsar_import_file import import_file

# Exit codes for this program
class ExitStatus: Success, Error, Running = range(3)
    
def import_norsar_files():    
    try:        
        log = create_log("norsar")   
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
