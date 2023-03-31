import os
import shutil
import argparse
import time
import logging
from multiprocessing import Pool, cpu_count
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QTextEdit


class FileOrganizerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Organizer")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.vertical_layout = QVBoxLayout()
        self.central_widget.setLayout(self.vertical_layout)

        # source directory
        self.source_directory_layout = QHBoxLayout()
        self.vertical_layout.addLayout(self.source_directory_layout)
        self.source_directory_label = QLabel("Source Directory:")
        self.source_directory_edit = QLineEdit()
        self.source_directory_button = QPushButton("Browse")
        self.source_directory_button.clicked.connect(self.browse_source_directory)
        self.source_directory_layout.addWidget(self.source_directory_label)
        self.source_directory_layout.addWidget(self.source_directory_edit)
        self.source_directory_layout.addWidget(self.source_directory_button)

        # image directory
        self.image_directory_layout = QHBoxLayout()
        self.vertical_layout.addLayout(self.image_directory_layout)
        self.image_directory_label = QLabel("Image Directory:")
        self.image_directory_edit = QLineEdit()
        self.image_directory_button = QPushButton("Browse")
        self.image_directory_button.clicked.connect(self.browse_image_directory)
        self.image_directory_layout.addWidget(self.image_directory_label)
        self.image_directory_layout.addWidget(self.image_directory_edit)
        self.image_directory_layout.addWidget(self.image_directory_button)

        # document directory
        self.document_directory_layout = QHBoxLayout()
        self.vertical_layout.addLayout(self.document_directory_layout)
        self.document_directory_label = QLabel("Document Directory:")
        self.document_directory_edit = QLineEdit()
        self.document_directory_button = QPushButton("Browse")
        self.document_directory_button.clicked.connect(self.browse_document_directory)
        self.document_directory_layout.addWidget(self.document_directory_label)
        self.document_directory_layout.addWidget(self.document_directory_edit)
        self.document_directory_layout.addWidget(self.document_directory_button)

        # music directory
        self.music_directory_layout = QHBoxLayout()
        self.vertical_layout.addLayout(self.music_directory_layout)
        self.music_directory_label = QLabel("Music Directory:")
        self.music_directory_edit = QLineEdit()
        self.music_directory_button = QPushButton("Browse")
        self.music_directory_button.clicked.connect(self.browse_music_directory)
        self.music_directory_layout.addWidget(self.music_directory_label)
        self.music_directory_layout.addWidget(self.music_directory_edit)
        self.music_directory_layout.addWidget(self.music_directory_button)

        # video directory
        self.video_directory_layout = QHBoxLayout()
        self.vertical_layout.addLayout(self.video_directory_layout)
        self.video_directory_label = QLabel("Video Directory:")
        self.video_directory_edit = QLineEdit()
        self.video_directory_button = QPushButton("Browse")
        self.video_directory_button.clicked.connect(self.browse_video_directory)
        self.video_directory_layout.addWidget(self.video_directory_label)
        self.video_directory_layout.addWidget(self.video_directory_edit)
        self.video_directory_layout.addWidget(self.video_directory_button)

        # exclude extensions
        self.exclude_layout = QHBoxLayout()
        self.vertical_layout.addLayout(self.exclude_layout)
        self.exclude_label = QLabel("Exclude Extensions (separated by space):")
        self.exclude_edit = QLineEdit()
        self.exclude_layout.addWidget(self.exclude_label)
        self.exclude_layout.addWidget(self.exclude_edit)
        # organize button
        self.organize_button_layout = QHBoxLayout()
        self.vertical_layout.addLayout(self.organize_button_layout)
        self.organize_button = QPushButton("Organize Files")
        self.organize_button.clicked.connect(self.organize_files)
        self.organize_button_layout.addWidget(self.organize_button)

        # log output
        self.log_layout = QVBoxLayout()
        self.vertical_layout.addLayout(self.log_layout)
        self.log_label = QLabel("Log:")
        self.log_edit = QTextEdit()
        self.log_edit.setReadOnly(True)
        self.log_layout.addWidget(self.log_label)
        self.log_layout.addWidget(self.log_edit)

    def browse_source_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Source Directory")
        self.source_directory_edit.setText(directory)

    def browse_image_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Image Directory")
        self.image_directory_edit.setText(directory)

    def browse_document_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Document Directory")
        self.document_directory_edit.setText(directory)

    def browse_music_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Music Directory")
        self.music_directory_edit.setText(directory)

    def browse_video_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Video Directory")
        self.video_directory_edit.setText(directory)

    def organize_files(self):
        source_directory = self.source_directory_edit.text()
        image_directory = self.image_directory_edit.text()
        document_directory = self.document_directory_edit.text()
        music_directory = self.music_directory_edit.text()
        video_directory = self.video_directory_edit.text()
        exclude = self.exclude_edit.text().split()
        logger = create_logger()
        destination_directories = {
            "jpg": image_directory,
            "jpeg": image_directory,
            "png": image_directory,
            "gif": image_directory,
            "pdf": document_directory,
            "docx": document_directory,
            "doc": document_directory,
            "txt": document_directory,
            "mp3": music_directory,
            "wav": music_directory,
            "aac": music_directory,
            "mp4": video_directory,
            "mov": video_directory,
            "avi": video_directory,
        }
        if exclude:
            for ext in exclude:
                destination_directories.pop(ext.lower(), None)
        start_time = time.time()
        file_count = 0
        for dirpath, dirnames, filenames in os.walk(source_directory):
            for file_name in filenames:
                try:
                    extension = os.path.splitext(file_name)[1][1:].lower()
                    if extension in destination_directories:
                        destination_directory = destination_directories[extension]
                        if not os.path.exists(destination_directory):
                            os.makedirs(destination_directory)
                        shutil.move(
                            os.path.join(dirpath, file_name),
                            os.path.join(destination_directory, file_name),
                        )
                        logger.info(f"Moved {file_name} to {destination_directory}.")
                        file_count += 1
                except (OSError, shutil.Error) as e:
                    logger.error(f"Error while organizing {file_name}: {e}")
        for destination_directory in destination_directories.values():
            if os.path.exists(destination_directory) and not os.listdir(destination_directory):
                os.rmdir(destination_directory)
        elapsed_time = time.time() - start_time
        logger.info(f"Organized {file_count} files in {elapsed_time:.2f} seconds.")
        with open("file_organizer.log") as f:
            log_text = f.read()
            self.log_edit.setPlainText(log_text)





def create_logger():
    logger = logging.getLogger("file_organizer_logger")
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    file_handler = logging.FileHandler("file_organizer.log")
    file_handler.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    # create formatter and add it to the handlers
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_formatter = logging.Formatter("%(message)s")
    file_handler.setFormatter(file_formatter)
    console_handler.setFormatter(console_formatter)
    # add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


if __name__ == "__main__":
    app = QApplication([])
    gui = FileOrganizerGUI()
    gui.show()
    app.exec_()
