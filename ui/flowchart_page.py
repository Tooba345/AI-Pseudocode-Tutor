from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QScrollArea
)

from PySide6.QtCore import Qt


class FlowchartPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setSpacing(15)

        # ==========================================
        # TITLE
        # ==========================================

        title = QLabel("🌳 Code Flowchart")
        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""
            font-size: 30px;
            font-weight: bold;
            color: white;
            padding: 10px;
        """)

        subtitle = QLabel(
            "Visualize your Cambridge 9618 pseudocode step by step."
        )

        subtitle.setAlignment(Qt.AlignCenter)

        subtitle.setStyleSheet("""
            font-size: 16px;
            color: #B8B8CC;
            padding-bottom: 10px;
        """)

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # ==========================================
        # PSEUDOCODE INPUT
        # ==========================================

        input_label = QLabel("📝 Enter your pseudocode:")

        input_label.setStyleSheet("""
            color: white;
            font-size: 17px;
            font-weight: bold;
        """)

        self.pseudocode_input = QTextEdit()

        self.pseudocode_input.setPlaceholderText(
            "Example:\n\n"
            "START\n"
            "INPUT Number\n"
            "IF Number MOD 2 = 0 THEN\n"
            "    OUTPUT \"Even\"\n"
            "ELSE\n"
            "    OUTPUT \"Odd\"\n"
            "ENDIF\n"
            "END"
        )

        self.pseudocode_input.setMinimumHeight(180)

        self.generate_button = QPushButton(
            "🌳 Generate Flowchart"
        )

        self.generate_button.setFixedHeight(50)

        self.generate_button.clicked.connect(
            self.generate_flowchart
        )

        layout.addWidget(input_label)
        layout.addWidget(self.pseudocode_input)
        layout.addWidget(self.generate_button)

        # ==========================================
        # FLOWCHART AREA
        # ==========================================

        flowchart_label = QLabel("📊 Flowchart")

        flowchart_label.setStyleSheet("""
            color: white;
            font-size: 20px;
            font-weight: bold;
            padding-top: 10px;
        """)

        layout.addWidget(flowchart_label)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.flowchart_container = QWidget()

        self.flowchart_layout = QVBoxLayout(
            self.flowchart_container
        )

        self.flowchart_layout.setAlignment(
            Qt.AlignTop | Qt.AlignHCenter
        )

        self.scroll_area.setWidget(
            self.flowchart_container
        )

        layout.addWidget(self.scroll_area)

        self.setLayout(layout)

        # ==========================================
        # STYLING
        # ==========================================

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

            QScrollArea {
                background: #2B2B40;
                border: 1px solid #44445A;
                border-radius: 10px;
            }

            QPushButton {
                background: #4F7CFF;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 17px;
                font-weight: bold;
            }

            QPushButton:hover {
                background: #3B68E8;
            }
        """)

    # ==========================================
    # CLEAR FLOWCHART
    # ==========================================

    def clear_flowchart(self):

        while self.flowchart_layout.count():

            item = self.flowchart_layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()

    # ==========================================
    # CREATE NORMAL NODE
    # ==========================================

    def create_node(self, text, node_type="process"):

        node = QLabel(text)

        node.setAlignment(Qt.AlignCenter)
        node.setWordWrap(True)
        node.setMinimumWidth(350)
        node.setMaximumWidth(500)

        if node_type == "start":
            border = "#32CD32"

        elif node_type == "end":
            border = "#FF5555"

        elif node_type == "decision":
            border = "#FFD43B"

        elif node_type == "input":
            border = "#4F7CFF"

        elif node_type == "output":
            border = "#00C2FF"

        else:
            border = "#4F7CFF"

        node.setStyleSheet(f"""
            QLabel {{
                background: #2B2B40;
                color: white;
                border: 2px solid {border};
                border-radius: 12px;
                padding: 15px;
                font-size: 15px;
                font-weight: bold;
            }}
        """)

        return node

    # ==========================================
    # ARROW
    # ==========================================

    def add_arrow(self, text="↓"):

        arrow = QLabel(text)

        arrow.setAlignment(Qt.AlignCenter)

        arrow.setStyleSheet("""
            QLabel {
                color: #4F7CFF;
                font-size: 25px;
                font-weight: bold;
                padding: 3px;
            }
        """)

        self.flowchart_layout.addWidget(arrow)

    # ==========================================
    # GENERATE FLOWCHART
    # ==========================================

    def generate_flowchart(self):

        pseudocode = (
            self.pseudocode_input
            .toPlainText()
            .strip()
        )

        if pseudocode == "":
            return

        self.clear_flowchart()

        lines = [
            line.strip()
            for line in pseudocode.splitlines()
            if line.strip()
        ]

        i = 0

        while i < len(lines):

            line = lines[i]
            upper = line.upper()

            # ======================================
            # START
            # ======================================

            if upper == "START":

                self.flowchart_layout.addWidget(
                    self.create_node(
                        "🟢 START",
                        "start"
                    )
                )

                self.add_arrow()

            # ======================================
            # END
            # ======================================

            elif upper in ["END", "ENDPROGRAM"]:

                self.flowchart_layout.addWidget(
                    self.create_node(
                        "🔴 END",
                        "end"
                    )
                )

            # ======================================
            # INPUT
            # ======================================

            elif upper.startswith("INPUT"):

                self.flowchart_layout.addWidget(
                    self.create_node(
                        "📥 " + line,
                        "input"
                    )
                )

                self.add_arrow()

            # ======================================
            # OUTPUT
            # ======================================

            elif upper.startswith("OUTPUT"):

                self.flowchart_layout.addWidget(
                    self.create_node(
                        "📤 " + line,
                        "output"
                    )
                )

                self.add_arrow()

            # ======================================
            # IF / ELSE
            # ======================================

            elif upper.startswith("IF"):

                # Decision node
                decision = self.create_node(
                    "🔷 " + line,
                    "decision"
                )

                self.flowchart_layout.addWidget(
                    decision
                )

                # Look for ELSE / ENDIF
                yes_lines = []
                no_lines = []

                i += 1

                current_branch = yes_lines

                while i < len(lines):

                    current = lines[i]
                    current_upper = current.upper()

                    if current_upper == "ELSE":

                        current_branch = no_lines

                    elif current_upper == "ENDIF":

                        break

                    else:

                        current_branch.append(
                            current
                        )

                    i += 1

                # ==================================
                # BRANCHES
                # ==================================

                branches = QHBoxLayout()

                # YES branch
                yes_widget = QWidget()
                yes_layout = QVBoxLayout(
                    yes_widget
                )

                yes_label = QLabel("✅ YES")

                yes_label.setAlignment(
                    Qt.AlignCenter
                )

                yes_label.setStyleSheet("""
                    color: #32CD32;
                    font-size: 16px;
                    font-weight: bold;
                """)

                yes_layout.addWidget(
                    yes_label
                )

                for branch_line in yes_lines:

                    node_type = "process"

                    branch_upper = (
                        branch_line.upper()
                    )

                    if branch_upper.startswith(
                        "OUTPUT"
                    ):
                        node_type = "output"

                    elif branch_upper.startswith(
                        "INPUT"
                    ):
                        node_type = "input"

                    node = self.create_node(
                        branch_line,
                        node_type
                    )

                    yes_layout.addWidget(node)

                # NO branch
                no_widget = QWidget()
                no_layout = QVBoxLayout(
                    no_widget
                )

                no_label = QLabel("❌ NO")

                no_label.setAlignment(
                    Qt.AlignCenter
                )

                no_label.setStyleSheet("""
                    color: #FF5555;
                    font-size: 16px;
                    font-weight: bold;
                """)

                no_layout.addWidget(
                    no_label
                )

                for branch_line in no_lines:

                    node_type = "process"

                    branch_upper = (
                        branch_line.upper()
                    )

                    if branch_upper.startswith(
                        "OUTPUT"
                    ):
                        node_type = "output"

                    elif branch_upper.startswith(
                        "INPUT"
                    ):
                        node_type = "input"

                    node = self.create_node(
                        branch_line,
                        node_type
                    )

                    no_layout.addWidget(node)

                branches.addWidget(
                    yes_widget
                )

                branches.addWidget(
                    no_widget
                )

                branch_container = QWidget()

                branch_container.setLayout(
                    branches
                )

                self.flowchart_layout.addWidget(
                    branch_container
                )

                self.add_arrow()

            # ======================================
            # FOR LOOP
            # ======================================

            elif upper.startswith("FOR"):

                node = self.create_node(
                    "🔄 " + line,
                    "decision"
                )

                self.flowchart_layout.addWidget(
                    node
                )

                self.add_arrow()

            # ======================================
            # WHILE LOOP
            # ======================================

            elif upper.startswith("WHILE"):

                node = self.create_node(
                    "🔄 " + line,
                    "decision"
                )

                self.flowchart_layout.addWidget(
                    node
                )

                self.add_arrow()

            # ======================================
            # REPEAT
            # ======================================

            elif upper.startswith("REPEAT"):

                node = self.create_node(
                    "🔄 " + line,
                    "decision"
                )

                self.flowchart_layout.addWidget(
                    node
                )

                self.add_arrow()

            # ======================================
            # OTHER PROCESS
            # ======================================

            elif upper not in [
                "ENDIF",
                "ELSE"
            ]:

                node = self.create_node(
                    "⚙️ " + line,
                    "process"
                )

                self.flowchart_layout.addWidget(
                    node
                )

                self.add_arrow()

            i += 1