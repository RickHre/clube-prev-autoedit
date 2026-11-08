
# SCRIPT GERADOR - Cria blueprint editavel a partir de STYLE.json + transcricao + gatilhos escolhidos
# Uso: python script_gerador_blueprint.py --gatilhos push_direita,painel_preto,legenda_digitando,destaque_9_12
# Saida: blueprint.html + work/blueprint_config.json
# Campos editaveis: tipo_grafico (linha/barras/pizza), tamanho_seta (40-120), duracao, cor
import json, pathlib
print("SCRIPT GERADOR - Blueprint")
print("Le STYLE.json + transcricao.json + gatilhos escolhidos")
print("Gera blueprint.html editavel com timeline clicavel")
