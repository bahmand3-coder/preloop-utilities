"""
PRELOOP UTILITIES - Professional IT-Toolkit
Graphical User Interface (GUI)
"""

import sys
import platform
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QScrollArea, QGridLayout, QPushButton,
    QProgressBar, QFrame, QStackedWidget
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPixmap, QIcon

from core.boot_manager import BootManager
from core.diagnostics import Diagnostics
from core.system_info import SystemInfoProvider
from core.utils import format_bytes


class WorkerThread(QThread):
    """Background worker thread for diagnostics"""
    finished = pyqtSignal()
    progress = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, task):
        super().__init__()
        self.task = task

    def run(self):
        try:
            if self.task == "diagnostics":
                self._run_diagnostics()
            elif self.task == "memtest":
                self._run_memtest()
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

    def _run_diagnostics(self):
        provider = SystemInfoProvider()
        self.progress.emit("Gathering system information...")
        provider.get_formatted_system_info()
        self.progress.emit("Scanning boot entries...")
        provider.boot_manager.scan_boot_entries()

    def _run_memtest(self):
        diagnostics = Diagnostics()
        self.progress.emit("Starting memory test...")
        diagnostics.run_memory_test(duration_seconds=30)
        self.progress.emit("Memory test completed")


class PreloopMainWindow(QMainWindow):
    """Main PRELOOP Utilities window"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PRELOOP UTILITIES - Professional IT-Toolkit")
        self.setGeometry(100, 100, 1400, 900)

        # Initialize components
        self.info_provider = SystemInfoProvider()
        self.boot_manager = BootManager()
        self.diagnostics = Diagnostics()

        # Setup UI
        self._setup_ui()
        self._setup_styles()
        self._setup_timers()

    def _setup_ui(self):
        """Setup user interface"""
        # Main central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()

        # Header
        header = self._create_header()
        main_layout.addWidget(header)

        # Tabs
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #0a2f3f; }
            QTabBar::tab {
                background: #051a24;
                color: #00ccff;
                padding: 8px 20px;
                border: 1px solid #0a2f3f;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #0a2f3f;
                color: #00ffff;
                border-bottom: 2px solid #00ccff;
            }
        """)

        # Tab 1: Dashboard
        tabs.addTab(self._create_dashboard_tab(), "Dashboard")

        # Tab 2: System Info
        tabs.addTab(self._create_sysinfo_tab(), "System Info")

        # Tab 3: Boot Options
        tabs.addTab(self._create_boot_tab(), "Boot Options")

        # Tab 4: Diagnostics
        tabs.addTab(self._create_diagnostics_tab(), "Diagnostics")

        # Tab 5: Tools
        tabs.addTab(self._create_tools_tab(), "Tools")

        main_layout.addWidget(tabs)

        central_widget.setLayout(main_layout)

    def _create_header(self) -> QWidget:
        """Create application header"""
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background: #0a1f2e;
                border-bottom: 2px solid #00ccff;
                padding: 15px;
            }
        """)
        layout = QVBoxLayout()

        title = QLabel("PRELOOP UTILITIES")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: #ffffff;")

        subtitle = QLabel("Professional Technician Toolkit - Multi-Boot & System Diagnostics")
        subtitle.setFont(QFont("Arial", 12))
        subtitle.setStyleSheet("color: #00ccff;")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.setSpacing(5)
        layout.setContentsMargins(10, 5, 10, 5)

        header.setLayout(layout)
        return header

    def _create_dashboard_tab(self) -> QWidget:
        """Create dashboard tab"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Status cards
        cards_layout = QGridLayout()

        # Quick Status
        status_card = self._create_info_card("SYSTEM STATUS", "✓ HEALTHY")
        cards_layout.addWidget(status_card, 0, 0)

        # CPU Status
        cpu_info = self.info_provider.get_formatted_system_info()
        cpu_card = self._create_info_card("PROCESSOR", cpu_info.get("cpu", "N/A"))
        cards_layout.addWidget(cpu_card, 0, 1)

        # RAM Status
        ram_card = self._create_info_card("MEMORY", cpu_info.get("ram", "N/A"))
        cards_layout.addWidget(ram_card, 0, 2)

        # Boot Mode
        boot_card = self._create_info_card("BOOT MODE", cpu_info.get("boot_mode", "N/A"))
        cards_layout.addWidget(boot_card, 1, 0)

        # BIOS
        bios_card = self._create_info_card("FIRMWARE", cpu_info.get("bios", "N/A"))
        cards_layout.addWidget(bios_card, 1, 1)

        # Secure Boot
        sb_card = self._create_info_card("SECURE BOOT", cpu_info.get("secure_boot", "N/A"))
        cards_layout.addWidget(sb_card, 1, 2)

        layout.addLayout(cards_layout)

        # Quick Actions
        layout.addSpacing(20)
        actions_label = QLabel("Quick Actions")
        actions_label.setStyleSheet("color: #00ccff; font-weight: bold;")
        layout.addWidget(actions_label)

        actions_layout = QHBoxLayout()

        btn_sysinfo = QPushButton("Refresh System Info")
        btn_sysinfo.setStyleSheet(self._get_button_style())
        btn_sysinfo.clicked.connect(self._refresh_system_info)
        actions_layout.addWidget(btn_sysinfo)

        btn_memtest = QPushButton("Run Memory Test")
        btn_memtest.setStyleSheet(self._get_button_style())
        actions_layout.addWidget(btn_memtest)

        btn_diskhealth = QPushButton("Check Disk Health")
        btn_diskhealth.setStyleSheet(self._get_button_style())
        actions_layout.addWidget(btn_diskhealth)

        layout.addLayout(actions_layout)
        layout.addStretch()

        widget.setLayout(layout)
        return widget

    def _create_sysinfo_tab(self) -> QWidget:
        """Create system information tab"""
        widget = QWidget()
        layout = QVBoxLayout()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { background: #051a24; border: 1px solid #0a2f3f; }")

        content = QWidget()
        content_layout = QGridLayout()

        info = self.info_provider.get_formatted_system_info()

        row = 0
        for label, value in info.items():
            label_widget = QLabel(label.upper().replace('_', ' '))
            label_widget.setStyleSheet("color: #00ccff; font-weight: bold;")
            value_widget = QLabel(str(value))
            value_widget.setStyleSheet("color: #a0a0a0;")
            value_widget.setWordWrap(True)

            content_layout.addWidget(label_widget, row, 0)
            content_layout.addWidget(value_widget, row, 1)
            row += 1

        content.setLayout(content_layout)
        scroll.setWidget(content)
        layout.addWidget(scroll)

        widget.setLayout(layout)
        return widget

    def _create_boot_tab(self) -> QWidget:
        """Create boot options tab"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Boot mode info
        boot_info = self.boot_manager.get_boot_mode_info()

        boot_info_label = QLabel(f"Current Boot Mode: {boot_info['boot_mode_display']}")
        boot_info_label.setStyleSheet("color: #00ffff; font-size: 14px; font-weight: bold;")
        layout.addWidget(boot_info_label)

        layout.addSpacing(10)

        # Boot entries
        entries_label = QLabel("Available Boot Entries:")
        entries_label.setStyleSheet("color: #00ccff; font-weight: bold;")
        layout.addWidget(entries_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { background: #051a24; border: 1px solid #0a2f3f; }")

        entries_widget = QWidget()
        entries_layout = QVBoxLayout()

        all_entries = self.boot_manager.scan_boot_entries()

        if not all_entries:
            no_entries = QLabel("No boot entries found")
            no_entries.setStyleSheet("color: #ffaa00;")
            entries_layout.addWidget(no_entries)
        else:
            for entry in all_entries:
                entry_frame = QFrame()
                entry_frame.setStyleSheet("""
                    QFrame {
                        background: #0a2f3f;
                        border: 1px solid #00ccff;
                        border-radius: 5px;
                        padding: 10px;
                        margin: 5px 0px;
                    }
                """)
                entry_layout = QVBoxLayout()

                name = QLabel(f"► {entry.name}")
                name.setStyleSheet("color: #00ffff; font-weight: bold;")
                entry_layout.addWidget(name)

                path = QLabel(f"Path: {entry.boot_path}")
                path.setStyleSheet("color: #a0a0a0; font-size: 10px;")
                entry_layout.addWidget(path)

                entry_frame.setLayout(entry_layout)
                entries_layout.addWidget(entry_frame)

        entries_layout.addStretch()
        entries_widget.setLayout(entries_layout)
        scroll.setWidget(entries_widget)
        layout.addWidget(scroll)

        widget.setLayout(layout)
        return widget

    def _create_diagnostics_tab(self) -> QWidget:
        """Create diagnostics tab"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Storage info
        storage_label = QLabel("Storage Devices:")
        storage_label.setStyleSheet("color: #00ccff; font-weight: bold;")
        layout.addWidget(storage_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { background: #051a24; border: 1px solid #0a2f3f; }")

        storage_widget = QWidget()
        storage_layout = QVBoxLayout()

        storage_info = self.info_provider.get_formatted_storage_info()

        for drive in storage_info:
            drive_frame = QFrame()
            drive_frame.setStyleSheet("""
                QFrame {
                    background: #0a2f3f;
                    border: 1px solid #00ccff;
                    border-radius: 5px;
                    padding: 10px;
                    margin: 5px 0px;
                }
            """)
            drive_layout = QVBoxLayout()

            device = QLabel(f"► {drive['device']}")
            device.setStyleSheet("color: #00ffff; font-weight: bold;")
            drive_layout.addWidget(device)

            # Usage bar
            usage_percent = int(drive['usage'].rstrip('%'))
            progress = QProgressBar()
            progress.setValue(usage_percent)
            progress.setStyleSheet(self._get_progress_style())
            drive_layout.addWidget(progress)

            info_text = f"{drive['used']} / {drive['total']} ({drive['usage']})"
            info = QLabel(info_text)
            info.setStyleSheet("color: #a0a0a0; font-size: 10px;")
            drive_layout.addWidget(info)

            drive_frame.setLayout(drive_layout)
            storage_layout.addWidget(drive_frame)

        storage_layout.addStretch()
        storage_widget.setLayout(storage_layout)
        scroll.setWidget(storage_widget)
        layout.addWidget(scroll)

        widget.setLayout(layout)
        return widget

    def _create_tools_tab(self) -> QWidget:
        """Create tools tab"""
        widget = QWidget()
        layout = QVBoxLayout()

        tools_label = QLabel("System Tools:")
        tools_label.setStyleSheet("color: #00ccff; font-weight: bold;")
        layout.addWidget(tools_label)

        # Tool buttons
        tools_layout = QGridLayout()

        btn_memtest = QPushButton("Memory Test")
        btn_memtest.setStyleSheet(self._get_button_style())
        tools_layout.addWidget(btn_memtest, 0, 0)

        btn_diskcheck = QPushButton("Disk Health")
        btn_diskcheck.setStyleSheet(self._get_button_style())
        tools_layout.addWidget(btn_diskcheck, 0, 1)

        btn_refresh = QPushButton("Refresh Data")
        btn_refresh.setStyleSheet(self._get_button_style())
        btn_refresh.clicked.connect(self._refresh_system_info)
        tools_layout.addWidget(btn_refresh, 0, 2)

        btn_about = QPushButton("About")
        btn_about.setStyleSheet(self._get_button_style())
        tools_layout.addWidget(btn_about, 1, 0)

        layout.addLayout(tools_layout)
        layout.addStretch()

        widget.setLayout(layout)
        return widget

    def _create_info_card(self, title: str, value: str) -> QFrame:
        """Create information card"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: #0a2f3f;
                border: 2px solid #00ccff;
                border-radius: 8px;
                padding: 15px;
                margin: 5px;
            }
        """)
        layout = QVBoxLayout()

        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #00ccff;")

        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        value_label.setStyleSheet("color: #ffffff;")
        value_label.setWordWrap(True)

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.setSpacing(5)

        card.setLayout(layout)
        return card

    def _setup_styles(self):
        """Setup application styles"""
        self.setStyleSheet("""
            QMainWindow {
                background: #051a24;
            }
            QWidget {
                background: #051a24;
                color: #a0a0a0;
            }
            QLabel {
                color: #a0a0a0;
            }
            QTabWidget {
                background: #051a24;
            }
            QScrollArea {
                background: #051a24;
                border: 1px solid #0a2f3f;
            }
            QScrollBar:vertical {
                background: #0a1f2e;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #00ccff;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background: #00ffff;
            }
        """)

    def _get_button_style(self) -> str:
        """Get button stylesheet"""
        return """
            QPushButton {
                background: #0a2f3f;
                color: #00ccff;
                border: 2px solid #00ccff;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background: #0a4f6f;
                border: 2px solid #00ffff;
                color: #00ffff;
            }
            QPushButton:pressed {
                background: #051a3f;
            }
        """

    def _get_progress_style(self) -> str:
        """Get progress bar stylesheet"""
        return """
            QProgressBar {
                background: #051a24;
                border: 1px solid #0a2f3f;
                border-radius: 3px;
                height: 15px;
            }
            QProgressBar::chunk {
                background: #00ccff;
                border-radius: 2px;
            }
        """

    def _setup_timers(self):
        """Setup update timers"""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._refresh_system_info)
        self.update_timer.start(5000)  # Update every 5 seconds

    def _refresh_system_info(self):
        """Refresh system information"""
        self.info_provider = SystemInfoProvider()


def main():
    """Main entry point"""
    app = QApplication(sys.argv)

    window = PreloopMainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
