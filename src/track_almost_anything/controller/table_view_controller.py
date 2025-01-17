from track_almost_anything._logging import log_debug

from PySide6.QtWidgets import (
    QTableView,
    QAbstractItemView,
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from typing import List


class TableViewController:
    def __init__(self, table_view: QTableView):
        self.table_view = table_view

        self.model = QStandardItemModel()
        self.model.setColumnCount(1)  # Only one column for now
        self.model.setHorizontalHeaderLabels(["Items"])

        self.table_view.setModel(self.model)
        self.table_view.setSelectionMode(QAbstractItemView.MultiSelection)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.table_view.verticalHeader().setDefaultSectionSize(15)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.horizontalHeader().hide()

    def populate_table(self, items: List[str]) -> None:
        """Populate the table with a list of text items."""
        self.model.setRowCount(0)
        for item in items:
            standard_item = QStandardItem(item)
            standard_item.setEditable(False)
            self.model.appendRow(standard_item)

    def clear_table(self) -> None:
        self.model.clear()

    def deselect_all(self) -> None:
        self.table_view.clearSelection()

    def select_all(self) -> None:
        self.table_view.selectAll()

    def get_selection(self) -> List[str]:
        selected_indexes = self.table_view.selectionModel().selectedRows()
        selected_items = [
            self.model.itemFromIndex(index).text() for index in selected_indexes
        ]
        return selected_items

    # Only serves to test the functionality of selecting items in the table.
    def print_selected_rows(self) -> None:
        """Print the currently selected rows."""
        selected_indexes = self.table_view.selectionModel().selectedRows()
        selected_items = [
            self.model.itemFromIndex(index).text() for index in selected_indexes
        ]
        log_debug("Selected items:", selected_items)
