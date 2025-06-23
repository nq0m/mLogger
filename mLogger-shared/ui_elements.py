# Shared UI elements for mLogger applications
from PySide6.QtWidgets import QPushButton, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QColor

# Color scheme
NAVY = '#001F3F'
GRAY = '#AAAAAA'
SIGNAL_GREEN = '#43FF64'

class MLoggerLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(f'color: {SIGNAL_GREEN}; font-weight: bold;')

class MLoggerButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(f'background-color: {NAVY}; color: {SIGNAL_GREEN}; font-weight: bold;')

class MLoggerLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f'background-color: {GRAY}; color: {NAVY};')
