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

    def _GetPath(self,NoteId):
        SafeId = "".join(Char for Char in NoteId if Char.isalnum() or Char in ("-","_")).rstrip()
        return os.path.join(self.StoragePath, f"{SafeId}.md")

    def CreateOrUpdate(self,NoteId,Title,Content,Tags:List[str] = None) ->Dict:
        Tags = Tags or []
        FilePath = self._GetPath(NoteId)
        NowTimeStamp = datetime.utcnow().isoformat()

        MetaData = {
            "id": NoteId,
            "title":Title,
            "tags":Tags,
            "updated_at":NowTimeStamp
        }
        FileContent = f"<!--METADATA:{json.dumps(MetaData)}-->\n# {Title}\n\n{Content}"

        with open(FilePath,"w",encoding="utf-8") as TargetFile:
            TargetFile.write(FileContent)

        return {**MetaData, "content":Content}
    
    def GetNote(self,NoteId):
        FilePath = self._GetPath(NoteId)
        if not os.path.exists(FilePath):
            return None 
        with open(FilePath,"r", encoding="utf-8") as TargetFile:
            RawData = TargetFile.read()

        if RawData.startswith("<!--METADATA:"):
            Parts = RawData.split("-->\n",1)
            MetaJson = Parts[0].replace("<!--METADATA:","")
            MetaData = json.loads(MetaJson)
            BodyContent = Parts[1] if len(Parts) > 1 else ""
            return {**MetaData, "content":BodyContent}
        return {"id":NoteId, "title":NoteId,"tags":[],"content":RawData,"updated_at":""}
    def ListNotes(self):
        NotesList =[ ]
        FilePaths = glob.glob(os.path.join(self.StoragePath,"*.md"))
        for CurrentPath in FilePaths:
            NoteId = os.path.basename(CurrentPath).replace(".md","")
            NoteData = self.GetNote(NoteId)
            if NoteData:
                NotesList.append({
                    "id": NoteData.get("id"),
                    "title":NoteData.get("title"),
                    "tags":NoteData.get("tags", []),
                    "updated_at": NoteData.get("updated_at")
                })
        return NotesList

    def DeleteNote(self,NoteId):
        FilePath = self._GetPath(NoteId)
        if os.path.exists(FilePath):
            os.remove(FilePath)
            return True 
        return False
    
    def SearchNotes(self,SearchQuery):
        QueryLower = SearchQuery.lower()
        AllNotes = self.ListNotes()
        SearchResults = []

        for MetaData in AllNotes:
            FullNote = self.GetNote(MetaData["id"])
            if FullNote:
                TitleMatch = QueryLower in FullNote["title"].lower()
                ContentMatch = QueryLower in FullNote["content"].lower()
                TagMatch = any(QueryLower in Tag.lower() for Tag in FullNote.get("tags",[]))
                if TitleMatch or ContentMatch or TagMatch:
                    SearchResults.append(FullNote)  
        return SearchResults