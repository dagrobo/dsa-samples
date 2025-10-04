# -*- coding: utf-8 -*-

import subprocess, pyodbc
from shutil import move, copy
from pathlib import Path

def analyze_file(log, ctx, file):
    log.info("Analyzing file " + str(file)) 
    copy(ctx.directory_script / "c1_def.INP", ctx.directory_script / "IO_BUFF.$$$")
    # FIX: Get next sample id
    move(file, ctx.directory_script / "CTBTphd.txt")
    log.info("Running ctbtcon.exe") 
    subprocess.run([str(ctx.directory_script / "ctbtcon.exe")])
    log.info("Running gamma.exe") 
    subprocess.run([str(ctx.directory_script / "gamma.exe")])
    log.info("Analysis done")  
    if Path(ctx.directory_script / "SP_BUFF.$$$").is_file():
        pass