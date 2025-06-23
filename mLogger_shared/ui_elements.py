# Shared UI elements for mLogger applications
from PySide6.QtWidgets import QPushButton, QLabel, QLineEdit
from PySide6.QtGui import QFont

# Color scheme
NAVY = '#1c2d3c'
GRAY = '#AAAAAA'
SIGNAL_GREEN = '#4b7d65'

class MLoggerLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont('Arial', 12))
        self.setStyleSheet(f'color: {SIGNAL_GREEN}; background: {NAVY}; padding: 4px;')

class MLoggerButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont('Arial', 12, QFont.Bold))
        self.setStyleSheet(f'background-color: {SIGNAL_GREEN}; color: {NAVY}; border-radius: 4px; padding: 6px 12px;')

class MLoggerLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont('Arial', 12))
        self.setStyleSheet(f'background: {GRAY}; color: {NAVY}; border: 1px solid {NAVY}; padding: 4px;')
