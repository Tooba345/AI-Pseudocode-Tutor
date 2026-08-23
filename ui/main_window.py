from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QStackedWidget
)

from ui.home_page import HomePage
from ui.chat_page import ChatPage
from ui.flowchart_page import FlowchartPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("🤖 AI Pseudocode Tutor")
        self.resize(1200, 800)

        # Main container
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Navigation bar
        navigation = QHBoxLayout()

        self.home_button = QPushButton("🏠 Home")
        self.chat_button = QPushButton("💬 Chat")
        self.flowchart_button = QPushButton("🌳 Flowchart")

        navigation.addWidget(self.home_button)
        navigation.addWidget(self.chat_button)
        navigation.addWidget(self.flowchart_button)

        main_layout.addLayout(navigation)

        # Pages
        self.pages = QStackedWidget()

        self.home_page = HomePage()
        self.chat_page = ChatPage()
        self.flowchart_page = FlowchartPage()

        self.pages.addWidget(self.home_page)
        self.pages.addWidget(self.chat_page)
        self.pages.addWidget(self.flowchart_page)

        main_layout.addWidget(self.pages)

        # Navigation buttons
        self.home_button.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.home_page)
        )

        self.chat_button.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.chat_page)
        )

        self.flowchart_button.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.flowchart_page)
        )
        self.home_page.start_learning.connect(
            lambda: self.pages.setCurrentWidget(self.chat_page)
)
        # Styling
        self.setStyleSheet("""
            QMainWindow {
                background: #1E1E2F;
            }

            QPushButton {
                background: #2B2B40;
                color: white;
                border: 1px solid #4F7CFF;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background: #4F7CFF;
            }
        """)