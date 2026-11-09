# script2_render.py - Clube Prev V4 - fix tela preta 9:16 + karaoke palavra por palavra
# Uso: python script2_render.py --video raw/bloco3.mp4 --config work/blueprint_config.json --formato 9:16 --qualidade 480p
import argparse, json, os, sys, textwrap, re

def resolver_vars(texto, variaveis):
    if not isinstance(texto, str): return str(texto or "")
    mapa={}
    for k,v in variaveis.items():
        mapa[k.upper()]=v; mapa["VAR_"+k.upper()]=v
    mapa.update({"VAR_FUND_NAME":variaveis.get("fund",""),"VAR_FUND":variaveis.get("fund",""),"VAR_DIV":variaveis.get("div",""),"VAR_PVP":variaveis.get("pvp",""),"VAR_DESCONTO":variaveis.get("desconto",""),"VAR_TEMA":variaveis.get("tema","")})
    def repl(m): return str(mapa.get(m.group(1).strip(), m.group(0)))
    return re.sub(r"\{\{\s*([A-Za-z_0-9]+)\s*\}\}", repl, texto)

def carregar_config(path_config):
    print(f"[DEBUG] Config: {path_config} Existe? {os.path.exists(path_config)}")
    if not os.path.exists(path_config):
        for p in ["work/blueprint_config.json","work/config.json","config.json"]:
            if os.path.exists(p): path_config=p; break
        else: print("ERRO sem config"); sys.exit(1)
    with open(path_config, encoding="utf-8") as f: raw=json.load(f)
    variaveis={}; dados=[]
    if isinstance(raw, list): dados=raw
    elif isinstance(raw, dict):
        variaveis=raw.get("variables",{}) or raw.get("variaveis",{}) or {}
        if "cards" in raw: dados=raw["cards"]
        elif "segmentos" in raw: dados=raw["segmentos"]
    norm=[]
    for d in dados:
        tipo_raw=d.get("type") or d.get("tipo") or "nenhum"
        if isinstance(tipo_raw, dict): tipo_raw=tipo_raw.get("type") or "nenhum"
        selo_raw=d.get("seal") or d.get("selo") or ""
        texto=resolver_vars(d.get("text") or d.get("texto") or "", variaveis)
        selo=resolver_vars(str(selo_raw), variaveis)
        if selo.startswith("{{"): selo=""
        norm.append({"start":float(d.get("start",0)),"end":float(d.get("end",0)),"text":texto,"tipo":str(tipo_raw).lower(),"selo":selo})
    norm=[n for n in norm if n["end"]>n["start"]]; norm.sort(key=lambda x: x["start"])
    print(f"[DEBUG] {len(norm)} segmentos:")
    for n in norm: print(f"  -> {n['start']:.1f}-{n['end']:.1f} tipo={n['tipo']} selo={n['selo']} | {n['text'][:50]}...")
    return norm, variaveis

def achar_fonte():
    for c in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf","C:/Windows/Fonts/arialbd.ttf"]:
        if os.path.exists(c): return c
    return None

def fazer_painel_karaoke(texto, selo_texto, tipo, W, H, palavra_ativa=-1):
    # Desenha painel com karaoke: palavra ativa amarela e maior (1.22x), ja faladas brancas, futuras apagadas
    from PIL import Image, ImageDraw, ImageFont
    img=Image.new("RGB",(W,H),(10,10,10)); draw=ImageDraw.Draw(img)
    fp=achar_fonte()
    def fonte(tam):
        try: return ImageFont.truetype(fp,tam)
        except: return ImageFont.load_default()
    y=int(H*0.08)
    draw.text((int(W*0.08),y),"CLUBE PREV",fill=(255,255,255),font=fonte(int(H*0.022))); y+=int(H*0.06)
    if selo_texto.strip()!="" and tipo in ("selo","legenda","grafico_linha","seta_cima","seta_baixo","destaque"):
        f_selo=fonte(int(H*0.045)); selo=selo_texto.strip()
        bbox=draw.textbbox((0,0),selo,font=f_selo); tw=bbox[2]-bbox[0]; th=bbox[3]-bbox[1]
        x0=int(W*0.08); y0=y; x1=x0+tw+56; y1=y0+th+28
        draw.rounded_rectangle([x0,y0,x1,y1],radius=28,fill=(255,215,0)); draw.text((x0+28,y0+12),selo,fill=(0,0,0),font=f_selo); y=y1+int(H*0.04)
    if tipo in ("seta_cima","seta_baixo"):
        seta="↑" if tipo=="seta_cima" else "↓"; cor=(255,215,0) if tipo=="seta_cima" else (0,255,136)
        try: f_seta=ImageFont.truetype(fp,int(H*0.14))
        except: f_seta=fonte(int(H*0.14))
        draw.text((int(W*0.08),y),seta,fill=cor,font=f_seta); y+=int(H*0.18)
    # Karaoke: divide texto em palavras, palavra_ativa = indice da palavra sendo falada
    palavras = texto.replace("\n"," ").split()
    # Quebra em linhas de ~5 palavras para caber
    f_base = fonte(int(H*0.048)) if H>600 else fonte(int(H*0.06))
    f_ativa = fonte(int(int(H*0.048)*1.22)) if H>600 else fonte(int(int(H*0.06)*1.22))
    # Layout simples: desenha linha por linha, 5 palavras por linha
    palavras_por_linha = 5 if W<400 else 6
    linhas=[]
    for i in range(0, len(palavras), palavras_por_linha):
        linhas.append(palavras[i:i+palavras_por_linha])
    idx_global=0
    for linha in linhas:
        x=int(W*0.08)
        for palavra in linha:
            is_ativa = (idx_global==palavra_ativa)
            is_passada = (idx_global < palavra_ativa) if palavra_ativa>=0 else False
            if is_ativa:
                cor=(255,215,0); f=f_ativa
            elif is_passada:
                cor=(255,255,255); f=f_base
            else:
                # Futura: apagada se karaoke ativo, senao branca (quando palavra_ativa==-1 mostra tudo branco)
                cor=(255,255,255) if palavra_ativa==-1 else (120,120,120)
                f=f_base
            draw.text((x,y),palavra+" ",fill=cor,font=f)
            try: w_pal=draw.textlength(palavra+" ",font=f)
            except: w_pal=len(palavra)*18
            x+=int(w_pal)
            idx_global+=1
        y+=int(H*0.062)
        if y>H*0.92: break
    return img

def ajustar_video_cover(sub, target_w, target_h):
    # FIX TELA PRETA: usa resize + crop com x1/y1 calculados, nao x_center que falha no MoviePy 2.x
    # Escala para cobrir target
    escala = max(target_w / sub.w, target_h / sub.h) * 1.25
    v = sub.resized(escala)
    # Calcula crop central com viés para cima (rosto)
    # Garante que nao corta alem do tamanho
    cw = min(target_w, int(v.w))
    ch = min(target_h, int(v.h))
    x1 = max(0, int((v.w - cw)/2))
    # y1 com viés 35% do topo (centro-topo) em vez de 50%
    y1 = max(0, int((v.h - ch)*0.35))
    x2 = x1 + cw
    y2 = y1 + ch
    # Se ainda menor que target, deixa como está (vai ser centralizado com fundo preto, nao preto total)
    v2 = v.cropped(x1=x1, y1=y1, x2=x2, y2=y2)
    return v2

def render_um_formato(video_path, segmentos, formato, qualidade, out_path):
    print(f"\n=== Render {formato} {qualidade} -> {out_path} ===")
    from moviepy import VideoFileClip, ImageClip, CompositeVideoClip
    import numpy as np
    clip_orig=VideoFileClip(video_path); print(f"Video orig: {clip_orig.w}x{clip_orig.h} dur {clip_orig.duration:.1f}s")
    if formato=="16:9":
        W,H=(854,480) if qualidade=="480p" else (1280,720); painel_w=int(W*0.45); video_w=W-painel_w
    else:
        W,H=(480,854) if qualidade=="480p" else (720,1280); painel_w=W; video_w=W
    print(f"Saida: {W}x{H}")
    clips=[]
    for i,seg in enumerate(segmentos):
        s=max(0,seg["start"]); e=min(clip_orig.duration,seg["end"])
        if e<=s: continue
        dur=e-s
        print(f" Bloco {i+1}: {s:.1f}-{e:.1f} tipo={seg['tipo']} selo={seg['selo']}")
        if seg["tipo"] in ("nenhum","sem_destaque",""):
            sub=clip_orig.subclipped(s,e)
            v=ajustar_video_cover(sub, W, H)
            v=v.with_position(("center","center"))
            clips.append(CompositeVideoClip([v],size=(W,H)).with_duration(dur))
        else:
            # KARAOKE: divide segmento em palavras, cada palavra um sub-clip com painel destacando ela
            palavras = seg["text"].replace("\n"," ").split()
            if len(palavras)==0: palavras=[""]
            # Tempo por palavra proporcional ao tamanho
            total_letras = sum(len(p) for p in palavras) or 1
            tempos=[]
            t_atual=s
            for p in palavras:
                d_pal = dur * (len(p)/total_letras)
                tempos.append((t_atual, t_atual+d_pal))
                t_atual+=d_pal
            # Ajusta ultimo para terminar no fim do segmento
            if tempos: tempos[-1]=(tempos[-1][0], e)
            for idx_pal, (ps, pe) in enumerate(tempos):
                if pe<=ps: continue
                d_pal=pe-ps
                sub=clip_orig.subclipped(ps, pe)
                if formato=="16:9":
                    v=ajustar_video_cover(sub, video_w, H); v=v.with_position((painel_w,0))
                    painel_img=fazer_painel_karaoke(seg["text"], seg["selo"], seg["tipo"], painel_w, H, palavra_ativa=idx_pal)
                    painel_clip=ImageClip(np.array(painel_img)).with_duration(d_pal).with_position((0,0))
                    clips.append(CompositeVideoClip([painel_clip, v],size=(W,H)).with_duration(d_pal))
                else:
                    video_h=int(H*0.60); painel_h=H-video_h
                    v=ajustar_video_cover(sub, W, video_h); v=v.with_position((0,0))
                    painel_img=fazer_painel_karaoke(seg["text"], seg["selo"], seg["tipo"], W, painel_h, palavra_ativa=idx_pal)
                    painel_clip=ImageClip(np.array(painel_img)).with_duration(d_pal).with_position((0,video_h))
                    clips.append(CompositeVideoClip([v, painel_clip],size=(W,H)).with_duration(d_pal))
    from moviepy import concatenate_videoclips
    final=concatenate_videoclips(clips,method="compose")
    os.makedirs(os.path.dirname(out_path) or ".",exist_ok=True)
    fps=18 if qualidade=="480p" else 24
    final.write_videofile(out_path,fps=fps,codec="libx264",audio_codec="aac",preset="ultrafast",threads=4,logger=None)
    clip_orig.close(); final.close()
    print(f"PRONTO: {out_path} {os.path.getsize(out_path)/1024/1024:.1f} MB {W}x{H}")
    return out_path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--video",default="raw/bloco3.mp4"); ap.add_argument("--config",default="work/blueprint_config.json")
    ap.add_argument("--formato",default="9:16",choices=["16:9","9:16","ambos"]); ap.add_argument("--qualidade",default="480p",choices=["480p","720p"])
    args=ap.parse_args()
    if not os.path.exists(args.video): print(f"ERRO video {args.video}"); sys.exit(1)
    segmentos,_=carregar_config(args.config)
    base=os.path.splitext(os.path.basename(args.video))[0]
    if args.formato in ("16:9","ambos"): render_um_formato(args.video,segmentos,"16:9",args.qualidade,f"final/{base}_16x9_{args.qualidade}.mp4")
    if args.formato in ("9:16","ambos"): render_um_formato(args.video,segmentos,"9:16",args.qualidade,f"final/{base}_9x16_{args.qualidade}.mp4")
    print("\nFIM - V4 com fix tela preta + karaoke")

if __name__=="__main__": main()