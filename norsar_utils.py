# -*- coding: utf-8 -*-

from win32file import CreateFile, CloseHandle
from win32con import GENERIC_READ, GENERIC_WRITE, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL

def has_exclusive_access(filename):    
    # Check if we have exclusive access to a file
    try:
        handle = CreateFile(str(filename), GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, None)
        CloseHandle(handle)
    except:
        return False            
    return True