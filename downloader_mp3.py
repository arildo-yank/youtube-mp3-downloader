import sys
import yt_dlp
import os
import re
import ssl
import certifi
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton,
    QFileDialog, QVBoxLayout, QWidget, QMessageBox, QProgressBar,
    QHBoxLayout, QRadioButton, QGroupBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from yt_dlp.utils import DownloadError


def configure_ssl():
    """Configures the default SSL context to use certifi's certificate bundle."""
    try:
        ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())
    except Exception as e:
        print(f"Error configuring SSL context: {e}")


class DownloadThread(QThread):
    progress_updated = pyqtSignal(int)
    status_updated = pyqtSignal(str)
    download_finished = pyqtSignal(bool, str)

    def __init__(self, url, save_path, is_playlist=False, audio_only=False, cookie_file=""):
        super().__init__()
        self.url = url
        self.save_path = save_path
        self.is_playlist = is_playlist
        self.audio_only = audio_only
        self.cookie_file = cookie_file
        self.canceled = False

    def run(self):
        try:
            if self.is_playlist:
                self.download_playlist()
            else:
                self.download_single_video()

            if not self.canceled:
                self.download_finished.emit(True, "Download concluído com sucesso!")

        except DownloadError as e:
            msg = str(e)
            if "Sign in to confirm your age" in msg or "age" in msg.lower():
                msg = "Erro: Conteúdo com restrição de idade!\nUse um arquivo de cookies autenticado."
            self.download_finished.emit(False, f"Erro do yt-dlp: {msg}")

        except Exception as e:
            self.download_finished.emit(False, f"Erro inesperado: {str(e)}")

    def download_single_video(self):
        self.status_updated.emit("Obtendo informações do vídeo com yt-dlp...")

        ydl_opts = {
            # Para vídeo, tentamos MP4 (mais compatível). Para áudio, extraímos MP3.
            'format': 'bestaudio/best' if self.audio_only else 'bv*+ba/b',
            'outtmpl': os.path.join(self.save_path, '%(title)s.%(ext)s'),
            'progress_hooks': [self.yt_dlp_progress_hook],
            'quiet': True,
            'noprogress': True,
            'ignoreerrors': True,
            'retries': 5,
        }

        # Cookies (opcional) para conteúdos restritos
        if self.cookie_file:
            ydl_opts['cookiefile'] = self.cookie_file

        # Se for áudio, converte para MP3 (precisa do ffmpeg instalado)
        if self.audio_only:
            ydl_opts['postprocessors'] = [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }
            ]
        else:
            # Força container MP4 quando possível
            ydl_opts['merge_output_format'] = 'mp4'

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])

        self.status_updated.emit("Download finalizado com yt-dlp.")

    def yt_dlp_progress_hook(self, d):
        if d['status'] == 'downloading':
            if 'total_bytes' in d and d['total_bytes'] > 0:
                progress = int(d['downloaded_bytes'] / d['total_bytes'] * 100)
            elif 'total_bytes_estimate' in d and d['total_bytes_estimate'] > 0:
                progress = int(d['downloaded_bytes'] / d['total_bytes_estimate'] * 100)
            else:
                progress = 0
            self.progress_updated.emit(progress)
            self.status_updated.emit(f"Progresso: {progress}%")
        elif d['status'] == 'finished':
            self.progress_updated.emit(100)
            self.status_updated.emit("Download finalizado com yt-dlp.")

    def download_playlist(self):
        self.status_updated.emit("Carregando playlist com yt-dlp...")

        ydl_opts = {
            'format': 'bestaudio/best' if self.audio_only else 'bv*+ba/b',
            'outtmpl': os.path.join(self.save_path, '%(playlist_title)s', '%(title)s.%(ext)s'),
            'progress_hooks': [self.yt_dlp_progress_hook],
            'quiet': True,
            'noprogress': True,
            'ignoreerrors': True,
            'retries': 5,
            'noplaylist': False,
        }

        if self.cookie_file:
            ydl_opts['cookiefile'] = self.cookie_file

        if self.audio_only:
            ydl_opts['postprocessors'] = [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }
            ]
        else:
            ydl_opts['merge_output_format'] = 'mp4'

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])

        self.status_updated.emit("Playlist finalizada com yt-dlp.")


    def cancel(self):
        """Sets the cancellation flag."""
        self.canceled = True


class YouTubeDownloader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader Pro+")
        self.setGeometry(300, 300, 650, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)

        settings_group = QGroupBox("Configurações de Download")
        settings_layout = QVBoxLayout()

        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Tipo de conteúdo:"))
        self.video_radio = QRadioButton("Vídeo Único")
        self.video_radio.setChecked(True)
        type_layout.addWidget(self.video_radio)
        self.playlist_radio = QRadioButton("Playlist Completa")
        type_layout.addWidget(self.playlist_radio)
        settings_layout.addLayout(type_layout)

        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Formato de saída:"))
        self.video_format = QRadioButton("Vídeo (MP4)")
        self.video_format.setChecked(True)
        format_layout.addWidget(self.video_format)
        self.audio_format = QRadioButton("Áudio (MP3)")
        format_layout.addWidget(self.audio_format)
        settings_layout.addLayout(format_layout)

        cookie_layout = QHBoxLayout()
        cookie_layout.addWidget(QLabel("Cookies (para vídeos restritos):"))
        self.cookie_label = QLabel("Nenhum arquivo selecionado")
        self.cookie_label.setStyleSheet("color: gray; font-style: italic;")
        cookie_layout.addWidget(self.cookie_label, 70)
        self.cookie_button = QPushButton("Procurar")
        self.cookie_button.clicked.connect(self.select_cookie_file)
        cookie_layout.addWidget(self.cookie_button, 30)
        settings_layout.addLayout(cookie_layout)

        settings_group.setLayout(settings_layout)
        main_layout.addWidget(settings_group)

        url_group = QGroupBox("Detalhes do Download")
        url_layout = QVBoxLayout()
        url_layout.addWidget(QLabel("URL do YouTube:"))
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Cole um link padrão do YouTube aqui...")
        url_layout.addWidget(self.url_input)

        url_layout.addWidget(QLabel("Local para salvar:"))
        dir_layout = QHBoxLayout()
        self.dir_label = QLabel("Nenhum diretório selecionado")
        self.dir_label.setStyleSheet("color: gray; font-style: italic;")
        dir_layout.addWidget(self.dir_label, 85)
        self.browse_button = QPushButton("Procurar")
        self.browse_button.clicked.connect(self.choose_directory)
        dir_layout.addWidget(self.browse_button, 15)
        url_layout.addLayout(dir_layout)
        url_group.setLayout(url_layout)
        main_layout.addWidget(url_group)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

        self.status_label = QLabel("Pronto para baixar")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)

        button_layout = QHBoxLayout()
        self.download_button = QPushButton("Iniciar Download")
        self.download_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 8px;")
        self.download_button.clicked.connect(self.start_download)
        button_layout.addWidget(self.download_button, 70)

        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.setStyleSheet("background-color: #f44336; color: white; padding: 8px;")
        self.cancel_button.clicked.connect(self.cancel_download)
        self.cancel_button.setEnabled(False)
        button_layout.addWidget(self.cancel_button, 30)
        main_layout.addLayout(button_layout)

        self.save_path = ""
        self.cookie_path = ""
        self.download_thread = None

    def choose_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Selecionar Diretório")
        if directory:
            self.save_path = directory
            self.dir_label.setText(directory)
            self.dir_label.setStyleSheet("color: black; font-style: normal;")

    def select_cookie_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Selecionar arquivo de cookies", "",
                                              "Arquivos TXT (*.txt);;Todos os arquivos (*)")
        if file:
            self.cookie_path = file
            self.cookie_label.setText(os.path.basename(file))
            self.cookie_label.setStyleSheet("color: black; font-style: normal;")

    def start_download(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Aviso", "Por favor, insira uma URL do YouTube!")
            return
        if not self.save_path:
            QMessageBox.warning(self, "Aviso", "Por favor, selecione um diretório para salvar!")
            return

        is_playlist = self.playlist_radio.isChecked()
        audio_only = self.audio_format.isChecked()

        self.download_thread = DownloadThread(url, self.save_path, is_playlist, audio_only, self.cookie_path)
        self.download_thread.progress_updated.connect(self.update_progress)
        self.download_thread.status_updated.connect(self.status_label.setText)
        self.download_thread.download_finished.connect(self.download_completed)

        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.download_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.status_label.setText("Iniciando download...")
        self.download_thread.start()

        # Adiciona botão para baixar online ao layout de botões
        self.online_button = QPushButton("Abrir no Downloader Online")
        self.online_button.setStyleSheet("background-color: #2196F3; color: white; padding: 8px;")
        self.online_button.clicked.connect(self.open_online_downloader)
        # Encontra o layout dos botões (download/cancelar) e adiciona o novo botão
        # O layout é o anterior ao último main_layout.addLayout(button_layout)
        # Recupera o button_layout do main_layout
        # O último layout adicionado ao main_layout é button_layout
        # Portanto, podemos acessar main_layout.itemAt(main_layout.count()-1).layout()
        main_layout = self.centralWidget().layout()
        button_layout = main_layout.itemAt(main_layout.count()-1).layout()
        button_layout.addWidget(self.online_button, 30)
    def open_online_downloader(self):
        import webbrowser
        url = self.url_input.text().strip()
        video_id = ""

        if "youtu.be" in url:
            video_id = url.split("/")[-1].split("?")[0].split("&")[0]
        elif "youtube.com" in url and "watch?v=" in url:
            video_id = url.split("watch?v=")[-1].split("&")[0].split("?")[0]

        if video_id:
            online_url = f"https://utomp3.com/youtube-converter/youtube/{video_id}"
            webbrowser.open(online_url)
            QMessageBox.information(self, "Abrindo no navegador", f"Link aberto: {online_url}")
        else:
            QMessageBox.warning(self, "Aviso", "Insira um link válido do YouTube para abrir no downloader online!")

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def cancel_download(self):
        if self.download_thread and self.download_thread.isRunning():
            self.download_thread.cancel()
            self.status_label.setText("Download cancelado")
            self.download_button.setEnabled(True)
            self.cancel_button.setEnabled(False)
            self.progress_bar.setVisible(False)

    def download_completed(self, success, message):
        if success:
            self.status_label.setText("Download concluído!")
            QMessageBox.information(self, "Sucesso", message)
        else:
            self.status_label.setText("Erro no download")
            QMessageBox.critical(self, "Erro", message)

        self.progress_bar.setVisible(False)
        self.download_button.setEnabled(True)
        self.cancel_button.setEnabled(False)


if __name__ == "__main__":
    configure_ssl()
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = YouTubeDownloader()
    window.show()
    sys.exit(app.exec())