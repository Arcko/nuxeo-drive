# coding: utf-8
from contextlib import suppress
from typing import Any, Dict, List, Tuple, TYPE_CHECKING

from PyQt5.QtCore import (
    QAbstractListModel,
    QModelIndex,
    QObject,
    Qt,
    pyqtProperty,
    pyqtSignal,
    pyqtSlot,
)

if TYPE_CHECKING:
    from .api import QMLDriveApi  # noqa
    from .application import Application  # noqa
    from ..engine.engine import Engine  # noqa

__all__ = ("FileModel", "LanguageModel")


class EngineModel(QAbstractListModel):
    engineChanged = pyqtSignal()
    statusChanged = pyqtSignal(object)
    uiChanged = pyqtSignal()

    UID_ROLE = Qt.UserRole + 1
    TYPE_ROLE = Qt.UserRole + 2
    SERVER_ROLE = Qt.UserRole + 3
    FOLDER_ROLE = Qt.UserRole + 4
    USERNAME_ROLE = Qt.UserRole + 5
    URL_ROLE = Qt.UserRole + 6
    UI_ROLE = Qt.UserRole + 7
    FORCE_UI_ROLE = Qt.UserRole + 8

    def __init__(self, application: "Application", parent: QObject = None) -> None:
        super(EngineModel, self).__init__(parent)
        self.application = application
        self.engines_uid: List[str] = []

    def roleNames(self) -> Dict[int, bytes]:
        return {
            self.UID_ROLE: b"uid",
            self.TYPE_ROLE: b"type",
            self.SERVER_ROLE: b"server",
            self.FOLDER_ROLE: b"folder",
            self.USERNAME_ROLE: b"username",
            self.URL_ROLE: b"url",
            self.UI_ROLE: b"ui",
            self.FORCE_UI_ROLE: b"forceUi",
        }

    def nameRoles(self) -> Dict[bytes, int]:
        return {
            b"uid": self.UID_ROLE,
            b"type": self.TYPE_ROLE,
            b"server": self.SERVER_ROLE,
            b"folder": self.FOLDER_ROLE,
            b"username": self.USERNAME_ROLE,
            b"url": self.URL_ROLE,
            b"ui": self.UI_ROLE,
            b"forceUi": self.FORCE_UI_ROLE,
        }

    def addEngine(self, uid: str, parent: QModelIndex = QModelIndex()) -> None:
        if uid in self.engines_uid:
            return
        count = self.rowCount()
        self.beginInsertRows(parent, count, count)
        self.engines_uid.append(uid)
        self.endInsertRows()
        self._connect_engine(self.application.manager._engines[uid])
        self.engineChanged.emit()

    def removeEngine(self, uid: str) -> None:
        with suppress(ValueError):
            idx = self.engines_uid.index(uid)
            self.removeRows(idx, 1)
            self.engineChanged.emit()

    def data(self, index: QModelIndex, role: int = UID_ROLE) -> Any:
        index = index.row()
        if index < 0 or index >= self.count:
            return None
        uid = self.engines_uid[index]
        row = self.application.manager._engines[uid]
        if role == self.UID_ROLE:
            return row.uid
        elif role == self.TYPE_ROLE:
            return row.type
        elif role == self.SERVER_ROLE:
            return row.name
        elif role == self.FOLDER_ROLE:
            return str(row.local_folder)
        elif role == self.USERNAME_ROLE:
            return row.remote_user
        elif role == self.URL_ROLE:
            return row.server_url
        elif role == self.UI_ROLE:
            return row.wui
        elif role == self.FORCE_UI_ROLE:
            return row.force_ui or row.wui
        return None

    @pyqtSlot(int, str, result=str)
    def get(self, index: int, role: str = "uid") -> str:
        if index < 0 or index >= self.count:
            return ""
        uid = self.engines_uid[index]
        row = self.application.manager._engines[uid]
        if role == "uid":
            return row.uid
        elif role == "type":
            return row.type
        elif role == "server":
            return row.name
        elif role == "folder":
            return str(row.local_folder)
        elif role == "username":
            return row.remote_user
        elif role == "url":
            return row.server_url
        elif role == "ui":
            return row.wui
        elif role == "forceUi":
            return row.force_ui or row.wui
        return ""

    def removeRows(
        self, row: int, count: int, parent: QModelIndex = QModelIndex()
    ) -> bool:
        try:
            self.beginRemoveRows(parent, row, row + count - 1)
            for i in range(count):
                self.engines_uid.pop(row)
            self.endRemoveRows()
            return True
        except:
            return False

    def empty(self) -> None:
        count = self.rowCount()
        self.removeRows(0, count)

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.engines_uid)

    @pyqtProperty("int", notify=engineChanged)
    def count(self) -> int:
        return self.rowCount()

    def _connect_engine(self, engine: "Engine") -> None:
        engine.invalidAuthentication.connect(self._relay_engine_events)
        engine.newConflict.connect(self._relay_engine_events)
        engine.newError.connect(self._relay_engine_events)
        engine.syncCompleted.connect(self._relay_engine_events)
        engine.syncResumed.connect(self._relay_engine_events)
        engine.syncStarted.connect(self._relay_engine_events)
        engine.syncSuspended.connect(self._relay_engine_events)
        engine.uiChanged.connect(self.uiChanged)

    def _relay_engine_events(self):
        engine = self.sender()
        self.statusChanged.emit(engine)


class FileModel(QAbstractListModel):
    fileChanged = pyqtSignal()

    ID = Qt.UserRole + 1
    DETAILS = Qt.UserRole + 2
    FOLDERISH = Qt.UserRole + 3
    LAST_CONTRIBUTOR = Qt.UserRole + 4
    LAST_ERROR = Qt.UserRole + 5
    LAST_LOCAL_UDPATE = Qt.UserRole + 6
    LAST_REMOTE_UDPATE = Qt.UserRole + 7
    LAST_SYNC_DATE = Qt.UserRole + 8
    LAST_TRANSFER = Qt.UserRole + 9
    LOCAL_PARENT_PATH = Qt.UserRole + 10
    LOCAL_PATH = Qt.UserRole + 11
    NAME = Qt.UserRole + 12
    REMOTE_CAN_RENAME = Qt.UserRole + 13
    REMOTE_CAN_UPDATE = Qt.UserRole + 14
    REMOTE_NAME = Qt.UserRole + 15
    REMOTE_REF = Qt.UserRole + 16
    STATE = Qt.UserRole + 17

    def __init__(self, parent: QObject = None) -> None:
        super(FileModel, self).__init__(parent)
        self.files: List[Dict[str, Any]] = []

    def roleNames(self) -> Dict[int, bytes]:
        return {
            self.ID: b"id",
            self.DETAILS: b"last_error_details",
            self.FOLDERISH: b"folderish",
            self.LAST_CONTRIBUTOR: b"last_contributor",
            self.LAST_ERROR: b"last_error",
            self.LAST_LOCAL_UDPATE: b"last_local_update",
            self.LAST_REMOTE_UDPATE: b"last_remote_update",
            self.LAST_SYNC_DATE: b"last_sync_date",
            self.LAST_TRANSFER: b"last_transfer",
            self.LOCAL_PARENT_PATH: b"local_parent_path",
            self.LOCAL_PATH: b"local_path",
            self.NAME: b"name",
            self.REMOTE_CAN_RENAME: b"remote_can_rename",
            self.REMOTE_CAN_UPDATE: b"remote_can_update",
            self.REMOTE_NAME: b"remote_name",
            self.REMOTE_REF: b"remote_ref",
            self.STATE: b"state",
        }

    def addFiles(
        self, files: List[Dict[str, Any]], parent: QModelIndex = QModelIndex()
    ) -> None:
        count = self.rowCount()
        self.beginInsertRows(parent, count, count + len(files) - 1)
        self.files.extend(files)
        self.fileChanged.emit()
        self.endInsertRows()

    def data(self, index: QModelIndex, role: int = NAME) -> Any:
        row = self.files[index.row()]
        if role == self.ID:
            return row["id"]
        elif role == self.DETAILS:
            return row["last_error_details"]
        elif role == self.FOLDERISH:
            return row["folderish"]
        elif role == self.LAST_CONTRIBUTOR:
            return row["last_contributor"]
        elif role == self.LAST_ERROR:
            return row["last_error"]
        elif role == self.LAST_LOCAL_UDPATE:
            return row["last_local_update"]
        elif role == self.LAST_REMOTE_UDPATE:
            return row["last_remote_update"]
        elif role == self.LAST_SYNC_DATE:
            return row["last_sync_date"]
        elif role == self.LAST_TRANSFER:
            return row["last_transfer"]
        elif role == self.LOCAL_PARENT_PATH:
            return str(row["local_parent_path"])
        elif role == self.LOCAL_PATH:
            return str(row["local_path"])
        elif role == self.NAME:
            return row["name"]
        elif role == self.REMOTE_CAN_RENAME:
            return row["remote_can_rename"]
        elif role == self.REMOTE_CAN_UPDATE:
            return row["remote_can_update"]
        elif role == self.REMOTE_NAME:
            return row["remote_name"]
        elif role == self.REMOTE_REF:
            return row["remote_ref"]
        elif role == self.STATE:
            return row["state"]
        return ""

    @pyqtSlot(int, int)
    def removeRows(
        self, row: int, count: int, parent: QModelIndex = QModelIndex()
    ) -> bool:
        try:
            self.beginRemoveRows(parent, row, row + count - 1)
            for i in range(count):
                self.files.pop(row)
            self.fileChanged.emit()
            self.endRemoveRows()
            return True
        except:
            return False

    def empty(self) -> None:
        count = self.rowCount()
        self.removeRows(0, count)

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.files)

    @pyqtProperty("int", notify=fileChanged)
    def count(self) -> int:
        return self.rowCount()


class LanguageModel(QAbstractListModel):
    NAME_ROLE = Qt.UserRole + 1
    TAG_ROLE = Qt.UserRole + 2

    def __init__(self, parent: QObject = None) -> None:
        super(LanguageModel, self).__init__(parent)
        self.languages: List[Tuple[str, str]] = []

    def roleNames(self) -> Dict[int, bytes]:
        return {self.NAME_ROLE: b"name", self.TAG_ROLE: b"tag"}

    def addLanguages(
        self, languages: List[Tuple[str, str]], parent: QModelIndex = QModelIndex()
    ) -> None:
        count = self.rowCount()
        self.beginInsertRows(parent, count, count + len(languages) - 1)
        self.languages.extend(languages)
        self.endInsertRows()

    def data(self, index: QModelIndex, role: int = TAG_ROLE) -> str:
        row = self.languages[index.row()]
        if role == self.NAME_ROLE:
            return row[1]
        elif role == self.TAG_ROLE:
            return row[0]
        return ""

    @pyqtSlot(int, result=str)
    def getTag(self, index: int) -> str:
        return self.languages[index][0]

    @pyqtSlot(int, result=str)
    def getName(self, index: int) -> str:
        return self.languages[index][1]

    def removeRows(
        self, row: int, count: int, parent: QModelIndex = QModelIndex()
    ) -> bool:
        try:
            self.beginRemoveRows(parent, row, row + count - 1)
            for i in range(count):
                self.languages.pop(row)
            self.endRemoveRows()
            return True
        except:
            return False

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.languages)
