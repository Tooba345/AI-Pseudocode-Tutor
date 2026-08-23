from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton
)
from PySide6.QtCore import Qt, Signal


class HomePage(QWidget):

    start_learning = Signal()

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        # Title
        title = QLabel("🤖 AI Pseudocode Tutor")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 34px;
            font-weight: bold;
            color: #4F7CFF;
        """)

        # Subtitle
        subtitle = QLabel(
            "Learn Cambridge 9618 Pseudocode with AI\n"
            "Type a question or upload an image."
        )
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            font-size: 18px;
            color: white;
        """)

        # Features
        features = QLabel(
            "✅ Generate pseudocode\n"
            "📖 Line-by-line explanation\n"
            "📷 Upload question images\n"
            "🌳 Generate flowcharts\n"
            "📄 Export to PDF & DOCX"
        )
        features.setAlignment(Qt.AlignCenter)
        features.setStyleSheet("""
            font-size: 16px;
            color: #DDDDDD;
        """)

        # Start Button
        start_button = QPushButton("🚀 Start Learning")
        start_button.setFixedSize(220, 55)

        start_button.setStyleSheet("""
            QPushButton {
                background-color: #4F7CFF;
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 18px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #3B68E8;
            }
        """)

        # Tell the Home Page when the button is clicked
        start_button.clicked.connect(self.start_learning.emit)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(features)
        layout.addWidget(
            start_button,
            alignment=Qt.AlignCenter
        )

        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #1E1E2F;
            }
        """)