from PyQt5 import QtGui
from PyQt5.QtCore import QAbstractTableModel, Qt

class PandasModel(QAbstractTableModel):

    def __init__(self, data, key):
        super(PandasModel, self).__init__()
        self._data = data
        self._key = key

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                stat = self.format_stat(self._data.iloc[index.row(), index.column()])
                return stat
            if role == Qt.ForegroundRole and self._key is not None:
                val = self.getKeyByteFromTable(self._data.iloc[index.row(), index.column()])
                if val == self._key[index.column()]:
                    return QtGui.QColor('white')
        return None

    def getKeyByteFromTable(self, stat):
        return int(stat[0])

    def format_stat(self, stat):
        return str("{:02X}\n{:.3f}".format(stat[0], stat[2]))

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None