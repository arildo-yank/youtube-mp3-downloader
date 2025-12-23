```bash
(base) arildoyank@Arildos-iMac ~ % file:/Volumes/TITRAGO_DEV/downloader/
```
Perfeito. Abaixo está um README.md completo, profissional, baseado exatamente no código que você me passou, com explicação em inglês e português, pronto para colocar no GitHub.

Você pode copiar e colar direto em README.md.

⸻

🎬 YouTube Downloader Pro+

A desktop application built with Python + PyQt6 + yt-dlp to download YouTube videos or playlists, supporting MP4 video and MP3 audio, with progress tracking, cancellation, and support for age-restricted videos via cookies.

⸻

🇺🇸 English

✨ Features
	•	Download single YouTube videos or entire playlists
	•	Choose output format:
	•	🎥 Video (MP4)
	•	🎧 Audio (MP3, converted via FFmpeg)
	•	Real-time progress bar
	•	Cancel download at any time
	•	Support for age-restricted content using cookies
	•	Automatic MP3 extraction with configurable quality
	•	Clean and simple PyQt6 GUI
	•	Optional button to open an online downloader fallback

⸻

🧱 Technologies Used
	•	Python 3
	•	PyQt6 – GUI
	•	yt-dlp – YouTube download engine
	•	FFmpeg – Audio conversion (MP3)
	•	certifi + SSL – Secure HTTPS handling

⸻

📦 Requirements

Python packages

pip install yt-dlp PyQt6 certifi

System dependency (required for MP3 conversion)
FFmpeg must be installed and available in PATH.

macOS (Homebrew):

brew install ffmpeg

Verify:

ffmpeg -version


⸻

🚀 How to Run

python main.py

The application will open a graphical window.

⸻

⚙️ How It Works
	1.	Paste a YouTube URL
	2.	Select:
	•	Video or Playlist
	•	MP4 or MP3
	3.	Choose the destination folder
	4.	(Optional) Load a cookies.txt file for restricted videos
	5.	Click Start Download

The download runs in a background thread (QThread) to keep the UI responsive.

⸻

🔞 Age-Restricted Videos

For videos that require login or age confirmation:
	1.	Export cookies from your browser (YouTube logged in)
	2.	Save as cookies.txt
	3.	Load it using Cookies → Browse

The app automatically passes this file to yt-dlp.

⸻

🛑 Cancel Download

The Cancel button safely stops the download thread and resets the UI.

⸻

🧪 Supported Output
	•	MP4 (merged video + audio)
	•	MP3 (via libmp3lame, 192 kbps)

⸻

📂 Example Path

/Volumes/TITRAGO_DEV/downloader/


⸻

🇧🇷 Português

✨ Funcionalidades
	•	Download de vídeo único ou playlist completa
	•	Escolha do formato:
	•	🎥 Vídeo (MP4)
	•	🎧 Áudio (MP3, convertido com FFmpeg)
	•	Barra de progresso em tempo real
	•	Botão de cancelamento
	•	Suporte a vídeos com restrição de idade via cookies
	•	Conversão automática para MP3
	•	Interface gráfica simples e profissional (PyQt6)
	•	Botão opcional para abrir um downloader online

⸻

🧱 Tecnologias Utilizadas
	•	Python 3
	•	PyQt6 – Interface gráfica
	•	yt-dlp – Engine de download
	•	FFmpeg – Conversão de áudio
	•	certifi + SSL – Conexões seguras

⸻

📦 Dependências

Pacotes Python

pip install yt-dlp PyQt6 certifi

Dependência do sistema (obrigatória para MP3)
O FFmpeg precisa estar instalado no sistema.

macOS (Homebrew):

brew install ffmpeg

Teste:

ffmpeg -version


⸻

🚀 Como Executar

python main.py

A aplicação abrirá em uma janela gráfica.

⸻

⚙️ Funcionamento Interno
	1.	Insira a URL do YouTube
	2.	Escolha:
	•	Vídeo ou Playlist
	•	MP4 ou MP3
	3.	Selecione a pasta de destino
	4.	(Opcional) Selecione um arquivo cookies.txt
	5.	Clique em Iniciar Download

O download roda em uma thread separada, evitando travamentos da interface.

⸻

🔞 Vídeos com Restrição de Idade

Para vídeos que exigem login:
	1.	Exporte os cookies do navegador (YouTube logado)
	2.	Salve como cookies.txt
	3.	Carregue no app usando Cookies → Procurar

⸻

🛑 Cancelamento

O botão Cancelar interrompe o download com segurança e restaura a interface.

⸻

🧪 Formatos Suportados
	•	MP4 (vídeo + áudio mesclados)
	•	MP3 (192 kbps – libmp3lame)

⸻

📂 Exemplo de Caminho Local

/Volumes/TITRAGO_DEV/downloader/


⸻

📄 License

This project is for educational and personal use.
Use responsibly and respect YouTube’s Terms of Service.

