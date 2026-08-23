from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QFileDialog,
    QLabel
)

from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QThread, Signal

from utils.api_client import ClaudeClient
from utils.ai_tutor import create_tutor_prompt


class ClaudeWorker(QThread):

    finished = Signal(str)

    def __init__(self, client, prompt, image_path=None):
        super().__init__()

        self.client = client
        self.prompt = prompt
        self.image_path = image_path

    def run(self):

        response = self.client.ask(
            self.prompt,
            self.image_path
        )

        self.finished.emit(response)


class ChatPage(QWidget):

    def __init__(self):
        super().__init__()

        self.claude = ClaudeClient()
        self.worker = None

        # Keep track of uploaded image
        self.current_image_path = None

        # Main layout
        layout = QVBoxLayout()

        # Chat display
        self.chat_box = QTextEdit()
        self.chat_box.setReadOnly(True)
        self.chat_box.setPlaceholderText(
            "💬 Your conversation will appear here..."
        )

        # Image preview
        self.image_preview = QLabel()
        self.image_preview.setAlignment(Qt.AlignCenter)
        self.image_preview.setMaximumHeight(250)
        self.image_preview.hide()

        # Input
        input_layout = QHBoxLayout()

        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText(
            "Ask a Cambridge 9618 pseudocode question..."
        )

        self.upload_button = QPushButton("📷 Upload")
        self.send_button = QPushButton("➤ Send")

        input_layout.addWidget(self.question_input)
        input_layout.addWidget(self.upload_button)
        input_layout.addWidget(self.send_button)

        layout.addWidget(self.chat_box)
        layout.addWidget(self.image_preview)
        layout.addLayout(input_layout)

        self.setLayout(layout)

        # Connections
        self.send_button.clicked.connect(
            self.send_message
        )

        self.upload_button.clicked.connect(
            self.upload_image
        )

        self.question_input.returnPressed.connect(
            self.send_message
        )

        # Styling
        self.setStyleSheet("""
            QWidget {
                background: #1E1E2F;
            }

            QTextEdit {
                background: #2B2B40;
                color: white;
                border: 1px solid #44445A;
                border-radius: 10px;
                padding: 12px;
                font-size: 15px;
            }

            QLineEdit {
                background: #2B2B40;
                color: white;
                border: 1px solid #44445A;
                border-radius: 10px;
                padding: 10px;
                font-size: 15px;
            }

            QPushButton {
                background: #4F7CFF;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 15px;
                font-weight: bold;
            }

            QPushButton:hover {
                background: #3B68E8;
            }

            QLabel {
                color: white;
            }
        """)

    def send_message(self):

        question = self.question_input.text().strip()

        # If there is no question but there is an image,
        # give Claude a default instruction.
        if question == "" and self.current_image_path:
            question = (
                "Read this question carefully. "
                "Solve it using Cambridge 9618 pseudocode. "
                "Explain the solution clearly."
            )

        if question == "":
            return

        # Show user's message
        self.chat_box.append(
            f"<b>👤 You:</b><br>{question}<br>"
        )

        # Show image status
        if self.current_image_path:
            self.chat_box.append(
                "<b>📷 Image attached</b><br>"
            )

        # Clear input
        self.question_input.clear()

        # Create tutor prompt
        prompt = create_tutor_prompt(question)

        # Thinking message
        self.chat_box.append(
            "<b>🤖 AI:</b><br>Thinking...<br>"
        )

        # Disable controls
        self.send_button.setEnabled(False)
        self.upload_button.setEnabled(False)
        self.question_input.setEnabled(False)

        # Start Claude worker
        self.worker = ClaudeWorker(
            self.claude,
            prompt,
            self.current_image_path
        )

        self.worker.finished.connect(
            self.show_response
        )

        self.worker.start()

    def show_response(self, response):

        formatted_response = response.replace(
            "\n",
            "<br>"
        )

        self.chat_box.append(
            f"<b>🤖 AI:</b><br>"
            f"{formatted_response}<br>"
        )

        scrollbar = self.chat_box.verticalScrollBar()
        scrollbar.setValue(
            scrollbar.maximum()
        )

        # Re-enable controls
        self.send_button.setEnabled(True)
        self.upload_button.setEnabled(True)
        self.question_input.setEnabled(True)

        self.question_input.setFocus()

        self.worker = None

    def upload_image(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Question Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.webp)"
        )

        if not file_path:
            return

        # Load image
        pixmap = QPixmap(file_path)

        if pixmap.isNull():

            self.chat_box.append(
                "❌ Could not load that image."
            )

            return

        # Remember the actual image path
        self.current_image_path = file_path

        # Preview
        scaled_pixmap = pixmap.scaled(
            500,
            250,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.image_preview.setPixmap(
            scaled_pixmap
        )

        self.image_preview.show()

        self.chat_box.append(
            "<b>📷 Image attached.</b><br>"
            "Ask a question about it or press Send to solve it."
        )

        scrollbar = self.chat_box.verticalScrollBar()
        scrollbar.setValue(
            scrollbar.maximum()
        )