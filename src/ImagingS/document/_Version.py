from __future__ import annotations

from datetime import datetime
from io import BytesIO
from typing import List, Optional

from . import Document, DocumentFormat


class Commit:
    def __init__(self, time: datetime, data: bytes, message: str, parent: Optional[Commit]) -> None:
        self.time = time
        self.message = message
        self.data = data
        self.parent = parent


class VersionController:
    def __init__(self) -> None:
        self.commits: List[Commit] = []
        self.head: Optional[Commit] = None

    def commit(self, doc: Document, message: str) -> Commit:
        io = BytesIO()
        doc.save(io, DocumentFormat.ISD)
        data = io.getvalue()
        cmt = Commit(datetime.now(), data, message, self.head)
        self.commits.append(cmt)
        self.head = cmt
        return cmt

    def getDocument(self, commit: Commit) -> Document:
        io = BytesIO(commit.data)
        return Document.load(io, DocumentFormat.ISD)

    def clear(self):
        self.commits.clear()
        self.head = None
