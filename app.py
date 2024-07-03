import sys
import sounddevice as sd
import numpy as np
import scipy.io.wavfile
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QTextEdit, QLineEdit
from PyQt5.QtCore import QThread, pyqtSignal

class AudioRecorder(QThread):
    update_label = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.duration = 5  # default duration in seconds
        self.filename = 'output.wav'
        self.fs = 44100  # Sample rate

    def run(self):
        try:
            self.update_label.emit("Recording...")
            myrecording = sd.rec(int(self.duration * self.fs), samplerate=self.fs, channels=2, dtype='int16')
            sd.wait()  # Wait until recording is finished
            scipy.io.wavfile.write(self.filename, self.fs, myrecording)  # Save as WAV file
            self.update_label.emit("Recording complete")
        except Exception as e:
            self.update_label.emit(f"Error: {e}")

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Audio Recorder & Chat Interface')
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        self.label = QLabel('Press the button to start recording', self)
        layout.addWidget(self.label)

        self.record_button = QPushButton('Start Recording', self)
        self.record_button.clicked.connect(self.start_recording)
        layout.addWidget(self.record_button)

        self.save_button = QPushButton('Save As...', self)
        self.save_button.clicked.connect(self.save_as)
        layout.addWidget(self.save_button)

        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        self.chat_input = QLineEdit(self)
        self.chat_input.setPlaceholderText('Type your message here...')
        self.chat_input.returnPressed.connect(self.send_message)
        layout.addWidget(self.chat_input)

        self.setLayout(layout)

        self.recorder = AudioRecorder()
        self.recorder.update_label.connect(self.update_label)

    def start_recording(self):
        if self.recorder.isRunning():
            self.label.setText("Recording already in progress")
        else:
            self.recorder.start()

    def save_as(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getSaveFileName(self, "Save File", "", "WAV Files (*.wav);;All Files (*)", options=options)
        if file:
            self.recorder.filename = file

    def update_label(self, text):
        self.label.setText(text)

    def send_message(self):
        user_input = self.chat_input.text()
        if user_input:
            self.chat_display.append(f'You: {user_input}')
            self.chat_input.clear()
            # For now, we just display the user's input without any response.
            self.chat_display.append(f'AI: (This is a placeholder response)')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())