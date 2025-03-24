import sys
import os
import threading
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, 
                            QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, 
                            QProgressBar, QMessageBox, QFrame)
from PyQt5.QtGui import QIcon, QFont, QDragEnterEvent, QDropEvent
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QMimeData

# Import watermark processing modules
from watermark_detector import WatermarkDetector
from watermark_remover import WatermarkRemover

class DropArea(QLabel):
    fileDropped = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setText("Drop PDF file here\nor click to browse")
        self.setDefaultStyle()
        self.setAcceptDrops(True)
    
    def setDefaultStyle(self):
        """Set the default style for the drop area"""
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #7b68ee;
                border-radius: 10px;
                padding: 40px;
                background-color: #2a2a2a;
                color: #bbb;
                font-size: 16px;
            }
            QLabel:hover {
                background-color: #333333;
                border-color: #9f90f5;
            }
        """)
    
    def setDragEnterStyle(self):
        """Style when file is dragged over"""
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #9f90f5;
                border-radius: 10px;
                padding: 40px;
                background-color: #333333;
                color: #ddd;
                font-size: 16px;
            }
        """)
    
    def setFileSelectedStyle(self):
        """Style when file is selected"""
        self.setStyleSheet("""
            QLabel {
                border: 2px solid #9f90f5;
                border-radius: 10px;
                padding: 40px;
                background-color: #333333;
                color: #fff;
                font-size: 16px;
            }
        """)
    
    def resetToDefault(self):
        """Reset the drop area to default state"""
        self.setText("Drop PDF file here\nor click to browse")
        self.setDefaultStyle()
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1:
            url = event.mimeData().urls()[0]
            if url.isLocalFile() and url.toLocalFile().lower().endswith('.pdf'):
                event.acceptProposedAction()
                self.setDragEnterStyle()
    
    def dragLeaveEvent(self, event):
        self.setDefaultStyle()
    
    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1:
            file_path = event.mimeData().urls()[0].toLocalFile()
            if file_path.lower().endswith('.pdf'):
                self.fileDropped.emit(file_path)
                self.setText(os.path.basename(file_path))
                self.setFileSelectedStyle()
                event.acceptProposedAction()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked()
    
    def clicked(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select PDF File", "", "PDF Files (*.pdf)", options=options
        )
        if file_path:
            self.fileDropped.emit(file_path)
            self.setText(os.path.basename(file_path))
            self.setFileSelectedStyle()


class StatusLabel(QLabel):
    def __init__(self, text=""):
        super().__init__(text)
        self.setAlignment(Qt.AlignCenter)
        self.setWordWrap(True)
        self.setStyleSheet("""
            QLabel {
                color: #bbb;
                font-size: 14px;
                margin-top: 10px;
                margin-bottom: 10px;
            }
        """)
        self.hide()

class MainWindow(QMainWindow):
    update_status = pyqtSignal(str)
    update_progress = pyqtSignal(int)
    process_complete = pyqtSignal(bool, str)
    reset_ui = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Gamma AI Watermark Remover")
        self.setMinimumSize(600, 500)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            QLabel {
                color: #e0e0e0;
            }
            QPushButton {
                background-color: #7b68ee;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 30px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6a5acd;
            }
            QPushButton:disabled {
                background-color: #4a4a4a;
                color: #888;
            }
            QProgressBar {
                border: 2px solid #555;
                border-radius: 8px;
                text-align: center;
                background-color: #2a2a2a;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #7b68ee;
                border-radius: 6px;
            }
        """)
        
        self.detector = WatermarkDetector()
        self.remover = WatermarkRemover()
        self.current_file_path = None
        
        self.init_ui()
        self.setup_connections()
        
        # Create necessary folders
        os.makedirs('uploads', exist_ok=True)
        os.makedirs('outputs', exist_ok=True)
    
    def init_ui(self):
        # Main layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # App title
        title_label = QLabel("Gamma AI Watermark Remover")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #ddd;
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 10px;
            }
        """)
        
        # Description
        desc_label = QLabel("Remove watermarks from Gamma AI generated PDFs")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setStyleSheet("color: #bbb; font-size: 14px; margin-bottom: 20px;")
        
        # Drop area for files
        self.drop_area = DropArea()
        
        # Status display
        self.status_label = StatusLabel()
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(12)
        self.progress_bar.hide()
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.process_button = QPushButton("Remove Watermark")
        self.process_button.setFixedHeight(45)
        self.process_button.setEnabled(False)

        self.reset_button = QPushButton("Reset")
        self.reset_button.setFixedHeight(45)
        self.reset_button.setEnabled(False)
        
        button_layout.addStretch()
        button_layout.addWidget(self.process_button)
        button_layout.addWidget(self.reset_button)
        button_layout.addStretch()
        
        # Add everything to main layout
        main_layout.addWidget(title_label)
        main_layout.addWidget(desc_label)
        main_layout.addWidget(self.drop_area)
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.progress_bar)
        main_layout.addLayout(button_layout)
        main_layout.addStretch()
        
        # Footer with author and version info
        footer_layout = QHBoxLayout()
        
        # Left side - Author info
        author_layout = QVBoxLayout()
        author_layout.setSpacing(2)  # Reduced spacing between labels

        # Author label with clickable GitHub link - green color and underlined
        author_label = QLabel()
        author_label.setText('Author : <a href="https://github.com/DedInc" style="color:#40c060; text-decoration:underline;">@DedInc</a>')
        author_label.setOpenExternalLinks(True)  # This makes the link clickable
        author_label.setAlignment(Qt.AlignLeft)
        author_label.setStyleSheet("font-size: 12px; color: #666;")

        # Ported by label with clickable GitHub link - green color and underlined
        ported_by_label = QLabel()
        ported_by_label.setText('Ported By : <a href="https://github.com/AlexanderQueen" style="color:#40c060; text-decoration:underline;">@AlexanderQueen</a>')
        ported_by_label.setOpenExternalLinks(True)  # This makes the link clickable
        ported_by_label.setAlignment(Qt.AlignLeft)
        ported_by_label.setStyleSheet("font-size: 12px; color: #666;")

        author_layout.addWidget(author_label)
        author_layout.addWidget(ported_by_label)
        
        # Right side - Version info
        version_label = QLabel("v1.0.0")
        version_label.setAlignment(Qt.AlignRight)
        version_label.setStyleSheet("color: #40c060; font-size: 12px;")
        
        footer_layout.addLayout(author_layout)
        footer_layout.addStretch()
        footer_layout.addWidget(version_label)
        
        main_layout.addLayout(footer_layout)
        
        self.setCentralWidget(main_widget)
    
    def setup_connections(self):
        self.drop_area.fileDropped.connect(self.file_selected)
        self.process_button.clicked.connect(self.process_file)
        self.reset_button.clicked.connect(self.reset_interface)
        self.update_status.connect(self.status_label.setText)
        self.update_status.connect(lambda msg: self.status_label.show())
        self.update_progress.connect(self.progress_bar.setValue)
        self.process_complete.connect(self.handle_process_complete)
        self.reset_ui.connect(self.reset_interface)
    
    def file_selected(self, file_path):
        self.current_file_path = file_path
        self.process_button.setEnabled(True)
        self.reset_button.setEnabled(True)
    
    # Apply green styling to status label
        self.status_label.setStyleSheet("""
            QLabel {
                color: #40c060;
                font-size: 14px;
                margin-top: 10px;
                margin-bottom: 10px;
                font-weight: bold;
        }
    """)
    
        self.status_label.setText(f"Selected: {os.path.basename(file_path)}")
        self.status_label.show()
    
    def process_file(self):
        if not self.current_file_path:
            return
        
        self.process_button.setEnabled(False)
        self.progress_bar.setValue(0)
        self.progress_bar.show()
        self.update_status.emit("Analyzing PDF for watermarks...")
        
        # Start processing in a separate thread
        thread = threading.Thread(target=self.process_file_thread)
        thread.daemon = True
        thread.start()
    
    def reset_interface(self):
        """Reset the interface to initial state"""
        # Reset drop area
        self.drop_area.resetToDefault()
        
        # Reset status and progress
        self.status_label.hide()
        self.progress_bar.setValue(0)
        self.progress_bar.hide()
        
        # Reset buttons
        self.process_button.setEnabled(False)
        self.reset_button.setEnabled(False)
        
        # Clear current file path
        self.current_file_path = None
        
        # Remove open folder button if it exists
        if hasattr(self, 'open_folder_button'):
            self.centralWidget().layout().removeWidget(self.open_folder_button)
            self.open_folder_button.deleteLater()
            delattr(self, 'open_folder_button')
    
    def process_file_thread(self):
        try:
            # Step 1: Identify watermarks (20%)
            self.update_progress.emit(10)
            images_to_remove_info, error = self.detector.identify_watermarks(self.current_file_path)
            
            if error:
                self.process_complete.emit(False, f"Error: {error}")
                return
            
            self.update_progress.emit(40)
            
            # Step 2: Check if watermarks were found
            if not images_to_remove_info:
                self.update_progress.emit(100)
                self.process_complete.emit(True, "No watermarks found in the PDF.")
                return
            
            # Step 3: Remove watermarks (40% -> 80%)
            self.update_status.emit(f"Found {len(images_to_remove_info)} watermark images. Removing...")
            
            filename = os.path.basename(self.current_file_path)
            output_filename = 'processed_' + filename
            output_path = os.path.join('outputs', output_filename)
            
            self.update_progress.emit(60)
            processed_pdf_path, error = self.remover.remove_watermarks(
                self.current_file_path, 
                images_to_remove_info, 
                output_path
            )
            
            if error:
                self.process_complete.emit(False, f"Error: {error}")
                return
            
            # Step 4: Complete (80% -> 100%)
            self.update_progress.emit(100)
            
            # Success message with output path
            output_dir = os.path.abspath(os.path.dirname(processed_pdf_path))
            success_message = (f"Watermarks removed successfully!\n\n"
                              f"Saved as: {os.path.basename(processed_pdf_path)}\n"
                              f"Location: {output_dir}")
            
            self.process_complete.emit(True, success_message)
            
        except Exception as e:
            self.process_complete.emit(False, f"Error processing file: {str(e)}")
    
    def handle_process_complete(self, success, message):
        self.reset_button.setEnabled(True)
        
        # Update status label with appropriate styling based on success/failure
        if success:
            if "No watermarks found" in message:
                # Yellow for "no watermarks found" case
                self.status_label.setStyleSheet("""
                    QLabel {
                        color: #f0c040;
                        font-size: 14px;
                        margin-top: 10px;
                        margin-bottom: 10px;
                        font-weight: bold;
                    }
                """)
            else:
                # Green for success
                self.status_label.setStyleSheet("""
                    QLabel {
                        color: #40c060;
                        font-size: 14px;
                        margin-top: 10px;
                        margin-bottom: 10px;
                        font-weight: bold;
                    }
                """)
        else:
            # Red for error
            self.status_label.setStyleSheet("""
                QLabel {
                    color: #e05050;
                    font-size: 14px;
                    margin-top: 10px;
                    margin-bottom: 10px;
                    font-weight: bold;
                }
            """)
        
        self.update_status.emit(message)
        self.status_label.show()
        
        # For successful processing with watermarks removed
        if success and "No watermarks found" not in message:
            # Create a button to open the output folder
            output_dir = os.path.abspath('outputs')
            
            # If we already have an open folder button, remove it first
            if hasattr(self, 'open_folder_button'):
                self.centralWidget().layout().removeWidget(self.open_folder_button)
                self.open_folder_button.deleteLater()
            
            # Create a new button
            self.open_folder_button = QPushButton("Open Output Folder")
            self.open_folder_button.setFixedHeight(45)
            self.open_folder_button.clicked.connect(lambda: 
                os.startfile(output_dir) if sys.platform == "win32" else os.system(f'open "{output_dir}"')
            )
            
            # Add button to layout
            layout = self.centralWidget().layout()
            layout.insertWidget(layout.count()-1, self.open_folder_button)


def main():
    app = QApplication(sys.argv)
    # Set application-wide font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Get the correct path whether running as script or frozen executable
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle (compiled with PyInstaller)
        application_path = sys._MEIPASS
    else:
        # If running as a normal Python script
        application_path = os.path.dirname(os.path.abspath(__file__))
    
    icon_path = os.path.join(application_path, "assets", "icon.png")
    app_icon = QIcon(icon_path)
    app.setWindowIcon(app_icon)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()