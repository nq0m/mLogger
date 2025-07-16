import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# mLogger-POTA main application
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QSizePolicy, QDialog, QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QScrollArea
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QEvent
from include.ui_elements import MLoggerLabel, MLoggerButton, MLoggerLineEdit
from include.database import ContactDB
from include.config import save_config, get_config_filename, get_config_dir
from include.utc_utils import utc_isoformat, utc_ymd

class MainWindow(QWidget):


    # Removed window size debug output
    def __init__(self):
        super().__init__()
        self.setWindowTitle('mLogger-POTA')
        self.setStyleSheet('background-color: #1c2d3c;')
        self.resize(800, 600)  # Set initial window size
        self.setup_complete = False
        self.setup_info = None
        self.db = None  # Will be initialized after setup

        # Entry fields
        self.call_field = MLoggerLineEdit()
        self.sent_rst_field = MLoggerLineEdit()
        self.recv_rst_field = MLoggerLineEdit()
        self.park_field = MLoggerLineEdit()
        self.comments_field = MLoggerLineEdit()

        # Smaller font for labels
        from PySide6.QtGui import QFont
        label_font = QFont('Arial', 9)

        # --- Config Bar ---
        self.config_bar = MLoggerLabel("")
        self.config_bar.setFont(QFont('Arial', 12))
        self.config_bar.setStyleSheet('background-color: #4b7d65; color: #1c2d3c; border-radius: 4px; padding: 6px 12px;')
        self.config_bar.setMinimumHeight(32)
        self.config_bar.setText('Frequency: ---    Mode: ---')
        self.config_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

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

        # --- Contact Table ---
        self.contact_table = QTableWidget(0, 7)
        self.contact_table.setHorizontalHeaderLabels([
            'Time', 'Their Call', 'Sent RST', 'Rec RST', 'Their Park', 'Frequency', 'Mode'])
        self.contact_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.contact_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.contact_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.contact_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.contact_table.verticalHeader().setVisible(False)
        self.contact_table.setStyleSheet('background: #AAAAAA; color: #1c2d3c;')
        # QSizePolicy already imported at top, so no need to import again
        self.contact_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # Scroll area for table
        table_scroll = QScrollArea()
        table_scroll.setWidgetResizable(True)
        table_scroll.setWidget(self.contact_table)
        table_scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # GroupBox for table
        table_group = QGroupBox('Logged Contacts')
        table_group_layout = QVBoxLayout()
        table_group_layout.addWidget(table_scroll)
        table_group.setLayout(table_group_layout)
        table_group.setStyleSheet('QGroupBox { border-radius: 8px; border: 2px solid #4b7d65; margin-top: 8px; color: #4b7d65; font-weight: bold; } QGroupBox:title { subcontrol-origin: margin; left: 10px; padding: 0 4px; }')
        table_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.config_bar)
        layout.addWidget(group_box)
        layout.addWidget(table_group)
        self.setLayout(layout)

        # Launch setup dialog immediately if not configured
        if not self.setup_complete:
            self.show_setup_dialog()

    def update_config_bar(self):
        freq = self.setup_info['frequency'] if self.setup_info else '---'
        mode = self.setup_info['mode'] if self.setup_info else '---'
        self.config_bar.setText(f'Frequency: {freq}    Mode: {mode}')

        # Keyboard shortcuts (install event filter and set focus at the very end)
        for field in [self.sent_rst_field, self.recv_rst_field, self.park_field, self.comments_field]:
            field.installEventFilter(self)
        # (Revert) Remove debug print
        self.call_field.returnPressed.connect(self.save_fields)
        self.call_field.setFocus()

    def clear_fields(self):
        self.call_field.clear()
        self.sent_rst_field.clear()
        self.recv_rst_field.clear()
        self.park_field.clear()
        self.comments_field.clear()
        self.call_field.setFocus()

    def save_fields(self):
        cmd = self.call_field.text().strip().upper()
        # Prevent any !COMMAND from being logged as a contact
        if cmd.startswith('!'):
            if cmd == '!SETUP':
                self.show_setup_dialog()
            elif cmd == '!ADIF' and self.setup_complete:
                from include.adif_export import export_adif
                config_dir = get_config_dir()
                date_str = utc_ymd()
                setup_info = self.setup_info
                adif_filename = get_config_filename(setup_info['callsign'], setup_info['activation_park'], date_str).replace('.json', '.adi')
                adif_path = os.path.join(config_dir, adif_filename)
                contacts = self.db.get_contacts() if self.db else []
                export_adif(contacts, adif_path, setup_info)
                self.show_adif_export_dialog(adif_path)
            self.clear_fields()
            self.call_field.setFocus()
            return
        if not self.setup_complete:
            self.clear_fields()
            self.call_field.setFocus()
            return
        if not self.db:
            pass
        # Use frequency and mode from setup_info
        freq = self.setup_info['frequency'] if self.setup_info else ''
        mode = self.setup_info['mode'] if self.setup_info else ''
        from include.band_utils import get_band_from_frequency
        band = get_band_from_frequency(freq)
        contact = {
            'callsign': self.call_field.text(),
            'sent_rst': self.sent_rst_field.text(),
            'recv_rst': self.recv_rst_field.text(),
            'park': self.park_field.text(),
            'frequency': freq,
            'mode': mode,
            'comments': self.comments_field.text(),
            'band': band,
            'timestamp': utc_isoformat()
        }
        self.db.add_contact(contact)
        self.add_contact_to_table(contact)
        self.clear_fields()
        self.call_field.setFocus()
    def show_adif_export_dialog(self, adif_path):
        dialog = QDialog(self)
        dialog.setWindowTitle('ADIF Export Complete')
        dialog.setStyleSheet('background-color: #1c2d3c;')
        layout = QVBoxLayout()
        info_label = MLoggerLabel('ADIF file exported successfully!')
        info_label.setFont(QFont('Arial', 12))
        info_label.setStyleSheet('color: #4b7d65; font-weight: bold;')
        path_label = MLoggerLabel(adif_path)
        path_label.setFont(QFont('Arial', 10))
        path_label.setStyleSheet('color: #43FF64;')
        ok_btn = MLoggerButton('OK')
        ok_btn.setFont(QFont('Arial', 11))
        ok_btn.clicked.connect(dialog.accept)
        layout.addWidget(info_label)
        layout.addWidget(path_label)
        layout.addWidget(ok_btn)
        dialog.setLayout(layout)
        dialog.exec()
        # Do not add a contact for !ADIF command
        self.clear_fields()
        self.call_field.setFocus()

    def add_contact_to_table(self, contact):
        row = self.contact_table.rowCount()
        self.contact_table.insertRow(row)
        # Format timestamp to HH:MM:SS
        ts = contact.get('timestamp', '')
        time_str = ts[11:19] if len(ts) >= 19 else ts  # 'YYYY-MM-DDTHH:MM:SS...'
        self.contact_table.setItem(row, 0, QTableWidgetItem(time_str))
        self.contact_table.setItem(row, 1, QTableWidgetItem(contact.get('callsign', '')))
        self.contact_table.setItem(row, 2, QTableWidgetItem(contact.get('sent_rst', '')))
        self.contact_table.setItem(row, 3, QTableWidgetItem(contact.get('recv_rst', '')))
        self.contact_table.setItem(row, 4, QTableWidgetItem(contact.get('park', '')))
        self.contact_table.setItem(row, 5, QTableWidgetItem(contact.get('frequency', '')))
        self.contact_table.setItem(row, 6, QTableWidgetItem(contact.get('mode', '')))

    def show_setup_dialog(self):
        dialog = SetupDialog(self, initial_data=self.setup_info)
        if dialog.exec() == QDialog.Accepted:
            setup_info = dialog.get_setup_info()
            self.setup_info = setup_info
            self.update_config_bar()
            date_str = utc_ymd()
            config_dir = get_config_dir()
            config_filename = get_config_filename(setup_info['callsign'], setup_info['activation_park'], date_str)
            config_path = os.path.join(config_dir, config_filename)
            db_name = config_filename.replace('.json', '.sqlite')
            db_path = os.path.join(config_dir, db_name)

            # Check if config and db already exist
            config_exists = os.path.exists(config_path)
            db_exists = os.path.exists(db_path)
            if config_exists and db_exists:
                self.db = ContactDB(db_path)
                self.setup_complete = True
                self.setWindowTitle(f"mLogger-POTA - {setup_info['callsign']}@{setup_info['activation_park']}")
                self.load_contacts_to_table()
                return
            # Otherwise, save config and create db
            save_config(
                setup_info['callsign'],
                setup_info['activation_park'],
                setup_info,
                date_str
            )
            self.db = ContactDB(db_path)
            self.setup_complete = True
            self.setWindowTitle(f"mLogger-POTA - {setup_info['callsign']}@{setup_info['activation_park']}")
            self.load_contacts_to_table()
        else:
            self.setup_complete = False

    def load_contacts_to_table(self):
        self.contact_table.setRowCount(0)
        if self.db is not None:
            for contact in reversed(self.db.get_contacts()):
                self.add_contact_to_table(contact)

    def closeEvent(self, event):
        if self.db is not None:
            self.db.close()
        event.accept()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Escape:
                self.clear_fields()
                return True
            elif event.key() in (Qt.Key_Return, Qt.Key_Enter):
                self.save_fields()
                return True
        return super().eventFilter(obj, event)

class SetupDialog(QDialog):
    def __init__(self, parent=None, initial_data=None):
        super().__init__(parent)
        self.setWindowTitle('Setup')
        self.setStyleSheet('background-color: #1c2d3c;')
        from PySide6.QtGui import QFont
        label_font = QFont('Arial', 9)
        # Entry fields
        self.callsign_field = MLoggerLineEdit()
        self.park_field = MLoggerLineEdit()
        self.freq_field = MLoggerLineEdit()
        self.mode_field = MLoggerLineEdit()
        # Pre-fill fields if initial_data is provided
        if initial_data:
            self.callsign_field.setText(initial_data.get('callsign', ''))
            self.park_field.setText(initial_data.get('activation_park', ''))
            self.freq_field.setText(initial_data.get('frequency', ''))
            self.mode_field.setText(initial_data.get('mode', ''))
        # Grid layout for labels above fields
        grid = QGridLayout()
        callsign_label = MLoggerLabel('Your Callsign')
        callsign_label.setFont(label_font)
        park_label = MLoggerLabel('Activation Park')
        park_label.setFont(label_font)
        freq_label = MLoggerLabel('Frequency (MHz)')
        freq_label.setFont(label_font)
        mode_label = MLoggerLabel('Mode')
        mode_label.setFont(label_font)
        grid.addWidget(callsign_label, 0, 0)
        grid.addWidget(park_label, 0, 1)
        grid.addWidget(freq_label, 2, 0)
        grid.addWidget(mode_label, 2, 1)
        grid.addWidget(self.callsign_field, 1, 0)
        grid.addWidget(self.park_field, 1, 1)
        grid.addWidget(self.freq_field, 3, 0)
        grid.addWidget(self.mode_field, 3, 1)
        # Buttons
        self.save_btn = MLoggerButton('Save')
        self.cancel_btn = MLoggerButton('Cancel')
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        btn_row = QHBoxLayout()
        btn_row.addWidget(self.save_btn)
        btn_row.addWidget(self.cancel_btn)
        # GroupBox
        group_box = QGroupBox('Setup Information')
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
        self.callsign_field.setFocus()

    def get_setup_info(self):
        return {
            'callsign': self.callsign_field.text(),
            'activation_park': self.park_field.text(),
            'frequency': self.freq_field.text(),
            'mode': self.mode_field.text()
        }

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
