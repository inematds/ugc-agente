#!/usr/bin/env bash
# Monta o promo 9:16 de 15 s: cenas do Kling (com as de frente trocadas pelo Lip Sync),
# camada de textos (overlay.py), narração e música. Comandos exatamente como no promo INEMA.
#
# Entradas na pasta atual:
#   kling.mp4      vídeo de 15 s do Kling (omni_ref_video, 9:16, 1080p, sem áudio)
#   vo.mp3         narração (tts_elevenlabs.py), ≤ 14 s
#   musica.wav     trilha (fica em loop, volume baixo)
#   ls/ks91.mp4    Lip Sync da cena 1  (opcional)
#   ls/ks93.mp4    Lip Sync da cena 3  (opcional)
# Cortes das cenas: medir com
#   ffmpeg -i kling.mp4 -vf "select='gt(scene,0.25)',showinfo" -f null - 2>&1 | grep -o "pts_time:[0-9.]*"
set -euo pipefail
C1=${C1:-4.625}   # fim da cena 1
C2=${C2:-9.917}   # fim da cena 2
OFF=${OFF:-0.2}   # atraso da narração
D=$(dirname "$0")

# 1) cortar cenas e o trecho da narração de cada uma (para o Lip Sync no site)
mkdir -p ls
ffmpeg -v error -y -i vo.mp3 -af "adelay=$(python3 -c "print(int($OFF*1000))"):all=1,apad=whole_dur=15.1" -ar 44100 ls/vo_full.wav
ffmpeg -v error -y -i kling.mp4 -t "$C1" -c:v libx264 -crf 14 -an ls/v91.mp4
ffmpeg -v error -y -ss "$C2" -i kling.mp4 -t 5.0 -c:v libx264 -crf 14 -an ls/v93.mp4   # 5,0 s = 5 créditos; 5,1 s já cobra 10
ffmpeg -v error -y -i ls/vo_full.wav -t "$C1" -b:a 192k ls/a91.mp3
ffmpeg -v error -y -ss "$C2" -i ls/vo_full.wav -t 5.0 -b:a 192k ls/a93.mp3
echo "Agora: node $D/kling_lipsync_enviar.mjs \$PWD/ls 91:5 93:5  e depois  node $D/kling_lipsync_baixar.mjs \$PWD/ls 91 93"

# 2) fundo: cenas com lipsync no lugar das originais (se já baixadas)
BG=kling.mp4
if [ -f ls/ks91.mp4 ] && [ -f ls/ks93.mp4 ]; then
  ffmpeg -v error -y -i ls/ks91.mp4 -i kling.mp4 -i ls/ks93.mp4 -filter_complex \
    "[0:v]scale=1080:1920,setsar=1,fps=30,tpad=stop_mode=clone:stop_duration=0.1,trim=0:$C1,setpts=PTS-STARTPTS[a];\
     [1:v]fps=30,trim=$C1:$C2,setpts=PTS-STARTPTS,setsar=1[b];\
     [2:v]scale=1080:1920,setsar=1,fps=30,tpad=stop_mode=clone:stop_duration=0.2,trim=0:$(python3 -c "print(15-$C2)"),setpts=PTS-STARTPTS[c];\
     [a][b][c]concat=n=3:v=1:a=0[v]" -map "[v]" -c:v libx264 -crf 14 -r 30 bg.mp4
  BG=bg.mp4
fi

# 3) textos por cima (PNG por quadro, 30 fps)
[ -d ov ] || python3 "$D/overlay.py" ov

# 4) final: zoom de ~6% tira a marca d'água do canto, textos, voz, música com fade, -14 LUFS
ffmpeg -v error -y -i "$BG" -framerate 30 -i ov/f%04d.png -itsoffset "$OFF" -i vo.mp3 -stream_loop -1 -i musica.wav \
  -filter_complex "[0:v]fps=30,crop=1012:1800:34:0,scale=1080:1920:flags=lanczos,setsar=1[bg];\
[bg][1:v]overlay=0:0:format=auto,format=yuv420p[v];[2:a]volume=1.0[vo];\
[3:a]volume=0.16,afade=t=in:d=0.5,afade=t=out:st=13.5:d=1.5[m];\
[vo][m]amix=inputs=2:duration=longest:normalize=0,atrim=0:15,loudnorm=I=-14:TP=-1.5[a]" \
  -map "[v]" -map "[a]" -t 15 -c:v libx264 -crf 18 -preset slow -c:a aac -b:a 192k -movflags +faststart promo-9x16.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 promo-9x16.mp4
