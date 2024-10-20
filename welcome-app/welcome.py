import sys
import platform
import psutil  # Make sure to install this package if not already available
import subprocess  # Needed to run pkexec for Calamares
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
)
from PyQt5.QtCore import Qt  # Import Qt for alignment

class WelcomeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window title and fixed size
        self.setWindowTitle('Welcome to TTH-Linux')
        self.setFixedSize(400, 300)  # Fixed width and height

        # Create layout
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)  # Add margins for better spacing

        # Create welcome message
        welcome_label = QLabel('Welcome to TTH-Linux!')
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(welcome_label)

        # Distro description
        description_label = QLabel(
            "<p style='font-size: 14px;'>"
            "<b>TTH-Linux</b> is a user-friendly Linux distribution designed to provide a seamless experience for both new and experienced users.</p>"
        )
        description_label.setWordWrap(True)  # Allow text to wrap
        layout.addWidget(description_label)

        # Create button to launch Calamares
        calamares_button = QPushButton('Launch Calamares')
        calamares_button.clicked.connect(self.launch_calamares)
        layout.addWidget(calamares_button)

        # Additional Information Button
        info_button = QPushButton('Show Additional Information')
        info_button.clicked.connect(self.show_additional_info)
        layout.addWidget(info_button)

        # Add website footer
        footer_label = QLabel('<a href="https://techtonehub.com/">https://techtonehub.com/</a>')
        footer_label.setOpenExternalLinks(True)  # Allow the label to open links in a browser
        footer_label.setAlignment(Qt.AlignCenter)  # Center the footer
        layout.addWidget(footer_label)

        # Set layout to the window
        self.setLayout(layout)

    def launch_calamares(self):
        # Try to launch Calamares with pkexec for root privileges
        try:
            subprocess.run(["pkexec", "calamares"], check=True)
        except subprocess.CalledProcessError as e:
            # If there's an error, show a message box
            error_dialog = QMessageBox(self)
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setWindowTitle("Error")
            error_dialog.setText("Failed to launch Calamares with admin rights. Please check the logs.")
            error_dialog.setInformativeText(str(e))
            error_dialog.exec_()

    def show_additional_info(self):
        # Create a message box to show additional information
        info_msg = QMessageBox(self)
        info_msg.setWindowTitle("Additional Information")
        
        # System Information
        system_info = f"System Information:\n" \
                      f"Operating System: {platform.system()} {platform.release()}\n" \
                      f"Processor: {platform.processor()}\n" \
                      f"RAM: {round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB\n" \
                      f"Disk Usage: {self.get_disk_usage()}"

        # Getting Started Tips
        getting_started_tips = "Getting Started Tips:\n" \
                                "- Explore the system settings.\n" \
                                "- Check out the installed applications.\n" \
                                "- Visit our website for tutorials and documentation."

        # Combine information
        full_message = f"{system_info}\n\n{getting_started_tips}"
        
        # Set message box text
        info_msg.setText(full_message)
        info_msg.exec_()

    def get_disk_usage(self):
        disk = psutil.disk_usage('/')
        return f"{round(disk.total / (1024 ** 3), 2)} GB total, " \
               f"{round(disk.used / (1024 ** 3), 2)} GB used, " \
               f"{round(disk.free / (1024 ** 3), 2)} GB free"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    welcome_app = WelcomeApp()
    welcome_app.show()
    sys.exit(app.exec_())
