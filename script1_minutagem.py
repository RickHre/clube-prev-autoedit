# script1_minutagem.py - Clube Prev
# Uso: python script1_minutagem.py raw/bloco2.mp4
import sys
import os
import json

def main():
    video_path = sys.argv[1] if len(sys.argv) > 1 else "raw/bloco2.mp4"
    if not os.path.exists(video_path):
        print(f"ERRO: nao achei {video_path}")
        print("Confere se o video esta em raw/")
        return

    print(f"Processando: {video_path}")

    # 1. Extrai audio
    print("1/3 Extraindo audio...")
    from moviepy import VideoFileClip
    clip = VideoFileClip(video_path)
    audio_path = "work/temp_audio.mp3"
    os.makedirs("work", exist_ok=True)
    clip.audio.write_audiofile(audio_path, logger=None)
    clip.close()
    print(f"Audio salvo em {audio_path}")

    # 2. Transcreve com whisper
    print("2/3 Transcrevendo com whisper (modelo tiny, rapido)...")
    print("Se aparecer 'FP16 is not supported on CPU; using FP32' - eh normal, nao eh erro.")
    import whisper
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, language="pt", fp16=False)

    # 3. Salva transcricao.json
    segmentos = []
    for seg in result["segments"]:
        segmentos.append({
            "start": round(float(seg["start"]), 2),
            "end": round(float(seg["end"]), 2),
            "text": seg["text"].strip()
        })
        print(f"{seg['start']:.2f} - {seg['end']:.2f}: {seg['text'].strip()}")

    out_path = "work/transcricao.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(segmentos, f, ensure_ascii=False, indent=2)

    print(f"\n3/3 Pronto! Salvo em {out_path} com {len(segmentos)} trechos.")
    print("Agora abre work/transcricao.json e cola no blueprint padrao.")

if __name__ == "__main__":
    main()