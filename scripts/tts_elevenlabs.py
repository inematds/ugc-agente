#!/usr/bin/env python3
"""Narração no ElevenLabs (PT-BR). A chave vem da variável ELEVENLABS_API_KEY; nunca é impressa.

Uso:
  ELEVENLABS_API_KEY=... python3 tts_elevenlabs.py <voice_id> <saida.mp3> "<texto>" [velocidade]

Exemplo do promo INEMA: voz "Amanda Kelly" (oi8rgjIfLgJRsQ6rbZh3), velocidade 1.12, saiu com 13,3 s.
"""
import json
import os
import sys
import urllib.error
import urllib.request

key = os.environ.get('ELEVENLABS_API_KEY')
if not key:
    sys.exit('defina ELEVENLABS_API_KEY')
vid, out, txt = sys.argv[1], sys.argv[2], sys.argv[3]
speed = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0

body = json.dumps({
    'text': txt,
    'model_id': 'eleven_multilingual_v2',
    'voice_settings': {'stability': 0.45, 'similarity_boost': 0.8, 'style': 0.35,
                       'use_speaker_boost': True, 'speed': speed},
}).encode()
# mp3_44100_192 exige plano Creator; 128 kbps funciona em qualquer plano
req = urllib.request.Request(
    f'https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128',
    data=body, headers={'xi-api-key': key, 'Content-Type': 'application/json'})
try:
    data = urllib.request.urlopen(req).read()  # ler ANTES de abrir o arquivo: erro não deixa mp3 vazio
except urllib.error.HTTPError as e:
    sys.exit(f'erro {e.code}: {e.read()[:300]!r}')
with open(out, 'wb') as f:
    f.write(data)
print('ok', out)
