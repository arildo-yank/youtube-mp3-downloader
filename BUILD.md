
Aí vai um BUILD.md completo (PyInstaller + .app no macOS e .exe no Windows), em inglês e português, pronto pra colar no GitHub.

⸻

🏗 BUILD.md — PyInstaller (.app / .exe)

This guide explains how to package YouTube Downloader Pro+ into a standalone app using PyInstaller.

⸻

🇺🇸 English

1) Prerequisites

Python deps

Inside your virtualenv:

pip install --upgrade pip
pip install pyinstaller
pip install yt-dlp PyQt6 certifi

System dependency (FFmpeg)

Your app converts to MP3 using FFmpeg. You have two options:
	•	Option A (recommended): Keep FFmpeg as a system dependency (document it in INSTALL.md)
	•	Option B: Bundle FFmpeg inside your app (advanced; see section “Bundling FFmpeg”)

Verify FFmpeg:

ffmpeg -version


⸻

2) Project structure expected

Example:

downloader/
  main.py
  README.md
  INSTALL.md
  BUILD.md

If your entry file is not main.py, replace commands accordingly.

⸻

3) Build for macOS (.app)

3.1 Basic build (GUI app)

From the project folder:

pyinstaller --noconfirm --windowed --name "YouTubeDownloaderPro" main.py

Output:
	•	dist/YouTubeDownloaderPro.app

3.2 One-folder vs one-file
	•	macOS apps are naturally “folder-like” .app bundles, so this is already the standard.
	•	If you want to distribute a zip:
	•	zip the .app from dist/

3.3 Run the app

open dist/YouTubeDownloaderPro.app


⸻

4) Build for Windows (.exe)

4.1 Basic build (GUI app)

In PowerShell/CMD:

pyinstaller --noconfirm --windowed --name "YouTubeDownloaderPro" main.py

Output:
	•	dist\YouTubeDownloaderPro\YouTubeDownloaderPro.exe

4.2 Optional: single EXE (onefile)

pyinstaller --noconfirm --windowed --onefile --name "YouTubeDownloaderPro" main.py

Output:
	•	dist\YouTubeDownloaderPro.exe

Note: --onefile often starts slower and can trigger more antivirus false positives.

⸻

5) Common PyQt6 Packaging Notes

PyInstaller usually handles PyQt6 well, but if the app launches with a blank window or plugin errors, try:

pyinstaller --noconfirm --windowed --name "YouTubeDownloaderPro" --collect-all PyQt6 main.py


⸻

6) Bundling FFmpeg (Optional)

If you want the app to work without FFmpeg installed system-wide:

6.1 macOS
	1.	Install FFmpeg via Homebrew:

brew install ffmpeg


	2.	Find ffmpeg path:

which ffmpeg

Usually:

/opt/homebrew/bin/ffmpeg


	3.	Bundle it into the app:

pyinstaller --noconfirm --windowed --name "YouTubeDownloaderPro" \
  --add-binary "/opt/homebrew/bin/ffmpeg:bin" \
  main.py



6.2 Windows
	1.	Download FFmpeg binary (or install via winget)
	2.	Locate ffmpeg.exe
	3.	Bundle it:

pyinstaller --noconfirm --windowed --onefile --name "YouTubeDownloaderPro" `
  --add-binary "C:\path\to\ffmpeg.exe;bin" `
  main.py



6.3 Important (code change recommended)

If you bundle FFmpeg, it’s best to point yt-dlp to it using ffmpeg_location.

Add to your ydl_opts:

ydl_opts["ffmpeg_location"] = "bin"

Or use an absolute path if you detect it at runtime.

⸻

7) Code Signing (macOS) — Optional but recommended

Unsigned apps may show Gatekeeper warnings. For personal use you can right-click → Open.
For distribution, sign with Apple Developer ID.

(High-level steps; exact setup depends on your Apple account):
	•	codesign the .app
	•	optionally notarize

⸻

8) Where to find the final build
	•	macOS: dist/YouTubeDownloaderPro.app
	•	Windows:
	•	onedir: dist\YouTubeDownloaderPro\
	•	onefile: dist\YouTubeDownloaderPro.exe

⸻

🇧🇷 Português

1) Pré-requisitos

Dependências Python

Dentro do seu venv:

pip install --upgrade pip
pip install pyinstaller
pip install yt-dlp PyQt6 certifi

Dependência do sistema (FFmpeg)

O app converte para MP3 usando FFmpeg. Você tem duas opções:
	•	Opção A (recomendado): manter FFmpeg como dependência do sistema (documentado no INSTALL.md)
	•	Opção B: embutir FFmpeg dentro do app (avançado; veja “Bundling FFmpeg”)

Verifique:

ffmpeg -version


⸻

2) Estrutura esperada do projeto

Exemplo:

downloader/
  main.py
  README.md
  INSTALL.md
  BUILD.md

Se seu arquivo principal não for main.py, troque nos comandos.

⸻

3) Build para macOS (.app)

3.1 Build básico (app com interface)

Dentro da pasta do projeto:

pyinstaller --noconfirm --windowed --name "YouTubeDownloaderPro" main.py

Saída:
	•	dist/YouTubeDownloaderPro.app

3.2 One-folder vs one-file
	•	No macOS, o .app já é um “bundle” padrão.
	•	Para distribuir:
	•	compacte o .app da pasta dist/

3.3 Rodar o app

open dist/YouTubeDownloaderPro.app


⸻

4) Build para Windows (.exe)

4.1 Build básico (app com interface)

No PowerShell/CMD:

pyinstaller --noconfirm --windowed --name "YouTubeDownloaderPro" main.py

Saída:
	•	dist\YouTubeDownloaderPro\YouTubeDownloaderPro.exe

4.2 Opcional: EXE único (onefile)

pyinstaller --noconfirm --windowed --onefile --name "YouTubeDownloaderPro" main.py

Saída:
	•	dist\YouTubeDownloaderPro.exe

Obs: --onefile costuma abrir mais lento e pode dar mais falso positivo em antivírus.

⸻

5) Observações PyQt6 (plugins)

Se abrir com tela em branco ou erro de plugin, use:

pyinstaller --noconfirm --windowed --name "YouTubeDownloaderPro" --collect-all PyQt6 main.py


⸻

6) Embutir FFmpeg (Opcional)

Se quiser que o app funcione sem FFmpeg instalado no sistema:

6.1 macOS
	1.	Instale via Homebrew:

brew install ffmpeg


	2.	Descubra o caminho:

which ffmpeg

Normalmente:

/opt/homebrew/bin/ffmpeg


	3.	Inclua no build:

pyinstaller --noconfirm --windowed --name "YouTubeDownloaderPro" \
  --add-binary "/opt/homebrew/bin/ffmpeg:bin" \
  main.py



6.2 Windows
	1.	Baixe o ffmpeg (ou instale via winget)
	2.	Ache o ffmpeg.exe
	3.	Inclua no build:

pyinstaller --noconfirm --windowed --onefile --name "YouTubeDownloaderPro" `
  --add-binary "C:\path\to\ffmpeg.exe;bin" `
  main.py



6.3 Importante (mudança recomendada no código)

Se embutir FFmpeg, é melhor apontar o yt-dlp para ele usando ffmpeg_location.

No seu ydl_opts, adicione:

ydl_opts["ffmpeg_location"] = "bin"


⸻

7) Assinatura (macOS) — Opcional (recomendado para distribuição)

Apps não assinados podem gerar alerta do Gatekeeper. Para uso pessoal, dá pra abrir via botão direito → Open.
Para distribuir, o ideal é assinar e (opcionalmente) notarizar com Apple Developer ID.

⸻

8) Onde fica o build final
	•	macOS: dist/YouTubeDownloaderPro.app
	•	Windows:
	•	onedir: dist\YouTubeDownloaderPro\
	•	onefile: dist\YouTubeDownloaderPro.exe

