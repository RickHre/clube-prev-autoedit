
# Clube Prev - AutoEdit
## Como usar no VS Code Web (github.dev)
1. Abra github.dev e abra este repositorio
2. Edite style/STYLE.json (efeitos, cores, tamanho seta, tipo grafico)
3. Coloque video em raw/bloco1.mp4
4. Rode no terminal do Codespaces: python script1_minutagem.py
5. Rode: python script_gerador_blueprint.py
6. Abra blueprint.html no navegador, edite timeline, exporte JSON
7. No PC local: python script2_render.py --modo preview_480p
8. Aprovou? Rode --modo final_720p e jogue no CapCut para exportar 1080p

## Fluxo leve
VS Code Web = edita blueprint e JSON (0% CPU local)
PC local = so renderiza final (2 min por bloco)
## Gatilhos disponiveis
push_direita, push_esquerda, zoom_in, zoom_out, grafico_linha, grafico_barras, grafico_pizza, seta_cima, seta_baixo, contador, pulso_numero, selo_desconto, wipe, blur_fundo, legenda_digitando
