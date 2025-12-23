Perfeito 👍
Abaixo está o INSTALL.md completo, profissional, em inglês e português, alinhado exatamente com o teu projeto e pronto para colocar no GitHub.

Você pode copiar e colar direto em um arquivo chamado INSTALL.md.

⸻

🛠 Installation Guide — YouTube Downloader Pro+

This document explains how to install and run YouTube Downloader Pro+ on macOS, Windows, and Linux.

⸻

🇺🇸 English

✅ Prerequisites
	•	Python 3.9+
	•	Internet connection
	•	Basic terminal knowledge

Check Python version:

python --version


⸻

📦 Step 1 — Create a Virtual Environment (Recommended)

python -m venv .venv
source .venv/bin/activate   # macOS / Linux

On Windows:

python -m venv .venv
.venv\Scripts\activate


⸻

📦 Step 2 — Install Python Dependencies

pip install --upgrade pip
pip install yt-dlp PyQt6 certifi


⸻

🔊 Step 3 — Install FFmpeg (Required for MP3)

FFmpeg is required to convert audio to MP3.

macOS (Homebrew)

brew install ffmpeg

Verify:

ffmpeg -version


⸻

Ubuntu / Debian

sudo apt update
sudo apt install ffmpeg


⸻

Windows

winget install Gyan.FFmpeg

Restart the terminal after installation.

⸻

🔎 Step 4 — Verify FFmpeg MP3 Support

ffmpeg -encoders | grep mp3

Expected:

A....D libmp3lame


⸻

🚀 Step 5 — Run the Application

python main.py

The GUI window will open.

⸻

🔞 Optional — Age-Restricted Videos (Cookies)
	1.	Log into YouTube in your browser
	2.	Export cookies as cookies.txt
	3.	Load the file inside the app (Cookies → Browse)

⸻

🧪 Quick Test (Optional)

yt-dlp -x --audio-format mp3 https://www.youtube.com/watch?v=dQw4w9WgXcQ

If an .mp3 file is created, everything is configured correctly.

⸻

🇧🇷 Português

✅ Pré-requisitos
	•	Python 3.9 ou superior
	•	Conexão com a internet
	•	Conhecimento básico de terminal

Verifique a versão do Python:

python --version


⸻

📦 Passo 1 — Criar Ambiente Virtual (Recomendado)

python -m venv .venv
source .venv/bin/activate   # macOS / Linux

No Windows:

python -m venv .venv
.venv\Scripts\activate


⸻

📦 Passo 2 — Instalar Dependências Python

pip install --upgrade pip
pip install yt-dlp PyQt6 certifi


⸻

🔊 Passo 3 — Instalar FFmpeg (Obrigatório para MP3)

O FFmpeg é necessário para converter áudio em MP3.

macOS (Homebrew)

brew install ffmpeg

Verifique:

ffmpeg -version


⸻

Ubuntu / Debian

sudo apt update
sudo apt install ffmpeg


⸻

Windows

winget install Gyan.FFmpeg

Reinicie o terminal após a instalação.

⸻

🔎 Passo 4 — Verificar Suporte a MP3

ffmpeg -encoders | grep mp3

Resultado esperado:

A....D libmp3lame


⸻

🚀 Passo 5 — Executar a Aplicação

python main.py

A interface gráfica será aberta.

⸻

🔞 Opcional — Vídeos com Restrição de Idade
	1.	Faça login no YouTube no navegador
	2.	Exporte os cookies como cookies.txt
	3.	Carregue o arquivo no app (Cookies → Procurar)

⸻

🧪 Teste Rápido (Opcional)

yt-dlp -x --audio-format mp3 https://www.youtube.com/watch?v=dQw4w9WgXcQ

Se o arquivo .mp3 for gerado, está tudo configurado corretamente.

⸻

🧠 Notes / Notas
	•	FFmpeg não é instalado via pip
	•	O app depende do FFmpeg disponível no PATH do sistema
	•	Para distribuição, recomenda-se empacotar com PyInstaller

⸻

📄 License

This project is intended for educational and personal use.
Respect YouTube’s Terms of Service.

