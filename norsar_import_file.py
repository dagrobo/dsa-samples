# -*- coding: utf-8 -*-

from norsar_analyze import analyze_file
from shutil import move

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