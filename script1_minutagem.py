# script1_minutagem.py - Clube Prev - So extrair minutagem - MAX 4 PALAVRAS POR CARD
# Uso: python script1_minutagem.py raw/video.mp4
# Gera: work/video.json (cards de no maximo 4 palavras) + work/transcricao.json
import sys
import os
import json

MAX_PALAVRAS = 4

def chunk_words(words):
    # Quebra a lista de palavras em grupos de no maximo 4
    for i in range(0, len(words), MAX_PALAVRAS):
        grupo = words[i:i+MAX_PALAVRAS]
        if not grupo:
            continue
        yield {
            "start": round(float(grupo[0]["start"]), 2),
            "end": round(float(grupo[-1]["end"]), 2),
            "text": " ".join(w["text"] for w in grupo),
            "words": grupo,
        }

def main():
    video_path = sys.argv[1] if len(sys.argv) > 1 else "raw/video.mp4"
    if not os.path.exists(video_path):
        print(f"ERRO: nao achei {video_path}")
        return
    bloco = os.path.splitext(os.path.basename(video_path))[0]
    print(f"Processando: {video_path} -> bloco: {bloco} (max {MAX_PALAVRAS} palavras por card)")

    print("1/3 Extraindo audio...")
    from moviepy import VideoFileClip
    clip = VideoFileClip(video_path)
    if clip.audio is None:
        print("ERRO: video sem audio")
        clip.close()
        return
    os.makedirs("work", exist_ok=True)
    audio_path = "work/temp_audio.mp3"
    clip.audio.write_audiofile(audio_path, logger=None)
    clip.close()

    print("2/3 Transcrevendo com Whisper base...")
    import whisper
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, language="pt", fp16=False, word_timestamps=True)

    cards = []
    for seg in result["segments"]:
        words = []
        for w in seg.get("words", []):
            words.append({
                "start": round(float(w["start"]), 2),
                "end": round(float(w["end"]), 2),
                "text": w["word"].strip()
            })
        # Se o Whisper nao deu palavras, usa o segmento inteiro como 1 card
        if not words:
            cards.append({
                "start": round(float(seg["start"]), 2),
                "end": round(float(seg["end"]), 2),
                "text": seg["text"].strip(),
                "words": []
            })
            continue
        # Quebra em cards de no maximo 4 palavras
        for c in chunk_words(words):
            cards.append(c)
            print(f"{c['start']:.2f} - {c['end']:.2f}: {c['text']}")

    out_cards = f"work/{bloco}.json"
    with open(out_cards, "w", encoding="utf-8") as f:
        json.dump({"cards": cards}, f, ensure_ascii=False, indent=2)
    with open("work/transcricao.json", "w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)
    print(f"\n3/3 Pronto! Salvo em {out_cards} com {len(cards)} cards de ate {MAX_PALAVRAS} palavras.")

if __name__ == "__main__":
    main()
