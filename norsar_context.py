# -*- coding: utf-8 -*-

from pathlib import Path
import os

DIR_IMPORT = "C:\\temp"

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