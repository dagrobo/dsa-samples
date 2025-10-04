# -*- coding: utf-8 -*-

from norsar_utils import has_exclusive_access
from shutil import move

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