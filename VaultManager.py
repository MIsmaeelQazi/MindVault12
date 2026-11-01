import os
import json
import glob
from typing import List, Dict, Optional 
from datetime import datetime

THEVAULTPATH =os.path.abspath("./vault")

def PathExists():
    if not os.path.exists(THEVAULTPATH):
        os.makedirs(THEVAULTPATH)

class VaultManager:
    def __init__(self,StoragePath:str =THEVAULTPATH):
        self.StoragePath = StoragePath
        PathExists()

    def _GetPath(self,NoteId)

