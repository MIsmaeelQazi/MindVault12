from fastapi import FastAPI,HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List,Optional
from VaultManager import VaultManager

THEAPP = FastAPI(title="MindVault API Core", version="2.0.0")
THEAPP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TheVault = VaultManager()

class NotePayload(BaseModel):
    Title:str
    Content:str
    Tags:Optional[List[str]] = []

@THEAPP.get("/api/health")
def HealthCheck():
    return {"status":"online", "system":"MindVault Engine"}

@THEAPP.get("/api/notes")
def GetAllNotes():
    return TheVault.ListNotes()

@THEAPP.get("/api/notes/{NoteId}")
def GetNote(NoteId:str):
    TheNote = TheVault.GetNote(NoteId)
    if not TheNote:
        raise HTTPException(status_code=404, detail="Note not found")
    return TheNote

@THEAPP.post("/api/notes/{NoteId}")
def SaveNote(NoteId:str, Payload:NotePayload):
    return TheVault.CreateOrUpdate(
        NoteId=NoteId,
        Title=Payload.Title,
        Content=Payload.Content,
        Tags=Payload.Tags
    )

@THEAPP.delete("/api/notes/{NoteId}")
def DeleteNote(NoteId:str):
    IsDeleted = TheVault.DeleteNote(NoteId)
    if not IsDeleted:
        raise HTTPException(status_code=404, detail="Note not found or could not be deleted")
    return {"status":"deleted","id":NoteId}
@THEAPP.get("/api/search")
def SearchNotes(Q:str = Query(...,min_length=1)):
    return TheVault.SearchNotes(Q)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:THEAPP",host="127.0.0.1",port=8000, reload=True)