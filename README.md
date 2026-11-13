# Clube Prev - Autoedit (LIMPO)

Só 2 coisas. Nada mais.

## Estrutura
```
clube-prev-autoedit/
  script1_minutagem.py          -> extrai minutagem
  gravar_playwright_9x16.js     -> grava 9:16, CONGELADO, nao mexer
  package.json
  blueprint/blueprint_padrao.html  -> COLE O SEU AQUI
  raw/      -> coloque video.mp4 / bloco2.mp4 aqui
  work/     -> sai bloco2.json / transcricao.json
  final/    -> sai bloco2_9x16.mp4
```

## Fluxo (2 comandos)
1. Minutagem:
```
python script1_minutagem.py raw/bloco2.mp4
# ou no bash: python3 script1_minutagem.py raw/bloco2.mp4
```

2. Gravar:
```
node gravar_playwright_9x16.js --bloco bloco2 --formato 9:16
```

## O que foi removido
- script2_render.py, script2_render_v4_backup.py
- scripts/automacao.js (substituido por gravar_playwright_9x16.js)
- blueprint_config.json, comandos_playwright.txt
- node_modules/, __pycache__/ (reinstala com npm install)

## Instalar (1x)
```
npm install
npx playwright install chromium
pip install openai-whisper moviepy
# ffmpeg precisa estar no PATH
```

## Regras
- Nao copiar codigo do chat com o mouse: a palavra whisper vira chip e quebra o Python.
  Se der SyntaxError com [ , apague a linha e digite na mao.
- CAPTION_ADVANCE = 0.22 ja calibrado. Nao mexer sem testar bloco2 inteiro.
- Automacao CONGELADA.
