
# SCRIPT 1 - Minutagem: recebe mp4 da pasta raw/, extrai audio e gera work/transcricao.json com tempos
# Uso: python script1_minutagem.py --video raw/bloco1.mp4
# Requer: faster-whisper (leve) + ffmpeg
# Saida: work/transcricao.json com [{start, end, text}]
import argparse, json, subprocess, pathlib
print("SCRIPT 1 - Minutagem")
print("1. Recebe mp4 em raw/")
print("2. Extrai audio 16kHz com ffmpeg")
print("3. Transcreve com faster-whisper em pt")
print("4. Salva work/transcricao.json")
print("Exemplo de saida: [{'start':3.5,'end':5.0,'text':'Com Selic a treze virgula setenta e cinco'}]")
