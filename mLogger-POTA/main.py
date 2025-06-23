import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# mLogger-POTA main application
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QSizePolicy
from mLogger_shared.ui_elements import MLoggerLabel, MLoggerButton, MLoggerLineEdit
from PySide6.QtCore import Qt, QEvent

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('mLogger-POTA')
        self.setStyleSheet('background-color: #1c2d3c;')

        # Entry fields
        self.call_field = MLoggerLineEdit()
        self.sent_rst_field = MLoggerLineEdit()
        self.recv_rst_field = MLoggerLineEdit()
        self.park_field = MLoggerLineEdit()
        self.comments_field = MLoggerLineEdit()

        # Smaller font for labels
        from PySide6.QtGui import QFont
        label_font = QFont('Arial', 9)

        # Grid layout for labels above fields
        grid = QGridLayout()
        # Row 0: Labels
        call_label = MLoggerLabel('Their Call')
        call_label.setFont(label_font)
        sent_rst_label = MLoggerLabel('Sent RST')
        sent_rst_label.setFont(label_font)
        recv_rst_label = MLoggerLabel('Received RST')
        recv_rst_label.setFont(label_font)
        park_label = MLoggerLabel('Their Park')
        park_label.setFont(label_font)
        comments_label = MLoggerLabel('Comments')
        comments_label.setFont(label_font)
        grid.addWidget(call_label, 0, 0)
        grid.addWidget(sent_rst_label, 0, 1)
        grid.addWidget(recv_rst_label, 0, 2)
        grid.addWidget(park_label, 2, 0)
        grid.addWidget(comments_label, 2, 1)
        # Row 1: Entry fields
        grid.addWidget(self.call_field, 1, 0)
        grid.addWidget(self.sent_rst_field, 1, 1)
        grid.addWidget(self.recv_rst_field, 1, 2)
        grid.addWidget(self.park_field, 3, 0)
        grid.addWidget(self.comments_field, 3, 1, 1, 2)

        # Buttons
        self.clear_btn = MLoggerButton('Clear')
        self.save_btn = MLoggerButton('Save')
        self.clear_btn.clicked.connect(self.clear_fields)
        self.save_btn.clicked.connect(self.save_fields)
        btn_row = QHBoxLayout()
        btn_row.addWidget(self.clear_btn)
        btn_row.addWidget(self.save_btn)

        # GroupBox for contact entry
        group_box = QGroupBox('Contact Entry')
        group_box_layout = QVBoxLayout()
        group_box_layout.addLayout(grid)
        group_box_layout.addLayout(btn_row)
        group_box.setLayout(group_box_layout)
        group_box.setStyleSheet('QGroupBox { border-radius: 8px; border: 2px solid #4b7d65; margin-top: 8px; color: #4b7d65; font-weight: bold; } QGroupBox:title { subcontrol-origin: margin; left: 10px; padding: 0 4px; }')
        group_box.setSizePolicy(group_box.sizePolicy().horizontalPolicy(), QSizePolicy.Fixed)
        group_box.setMinimumHeight(group_box.sizeHint().height())

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(group_box)
        layout.addStretch(1)
        self.setLayout(layout)

        # Keyboard shortcuts
        for field in [self.call_field, self.sent_rst_field, self.recv_rst_field, self.park_field, self.comments_field]:
            field.installEventFilter(self)
        self.call_field.setFocus()

    def clear_fields(self):
        self.call_field.clear()
        self.sent_rst_field.clear()
        self.recv_rst_field.clear()
        self.park_field.clear()
        self.comments_field.clear()
        self.call_field.setFocus()

    def save_fields(self):
        # Placeholder for save logic
        self.clear_fields()
        self.call_field.setFocus()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Escape:
                self.clear_fields()
                return True
            elif event.key() in (Qt.Key_Return, Qt.Key_Enter):
                self.save_fields()
                return True
        return super().eventFilter(obj, event)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
