from __future__ import annotations

from typing import Callable

from PyQt5.QtWidgets import QUndoCommand

from ImagingS.document import Commit, Document, VersionController


class CommitCommand(QUndoCommand):
    def __init__(self, commit: Commit, controller: VersionController, callback: Callable[[Document], None], firstredo: bool = False) -> None:
        super().__init__()
        self.commit = commit
        self.controller = controller
        self.callback = callback
        if not firstredo:
            self.firstredo = False
        self.setText(self.commit.message)

    def undo(self):
        assert self.commit.parent is not None
        self.controller.head = self.commit.parent
        self.callback(self.controller.getDocument(self.commit.parent))

    def redo(self):
        if hasattr(self, "firstredo"):
            del self.firstredo
            return
        self.controller.head = self.commit
        self.callback(self.controller.getDocument(self.commit))
