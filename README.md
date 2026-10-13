# 🎬 UGC com agente — vídeo promocional feito por um agente de IA

[![Vídeo UGC com agente](guia/assets/banner.jpg)](https://inematds.github.io/ugc-agente/guia/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## O que é

Este projeto conta como um agente de IA (o Claude Code) produziu um vídeo promocional de 15 segundos do INEMA.CLUB no estilo UGC, aquele vídeo "de gente real falando com a câmera" das redes sociais. Serve para quem cria conteúdo e quer delegar a produção a um agente. Mostra a ideia, os passos com os comandos usados, as dicas que fizeram diferença e os problemas que apareceram no caminho. Para repetir, você precisa de assinatura do Kling AI, uma conta ElevenLabs, ffmpeg, Python e um navegador logado no Kling.

## 📖 Guia de uso

Guia completo (ideia, dicas, problemas e passo a passo): **https://inematds.github.io/ugc-agente/guia/**

## A dica principal

**Use a sua assinatura e dê ao agente a capacidade de operar o site.**

- As cenas saíram da assinatura Pro do Kling pela CLI oficial (`kling`): 120 créditos, sem chave de API.
- O Lip Sync do Kling só existe no site. O agente abriu um Chromium já logado (`--remote-debugging-port`) e, pelo Playwright, enviou as cenas, conferiu o custo no botão e baixou o resultado: mais 10 créditos.

## Como foi feito

| Etapa | Ferramenta | Resultado |
|---|---|---|
| Cenas | `kling omni_ref_video` (v3.0 Omni, 15 s, 9:16, 1080p, sem áudio) | 3 tomadas a partir da arte de referência |
| Voz | ElevenLabs `eleven_multilingual_v2`, voz Amanda Kelly, velocidade 1,12 | 13,3 s, conferida pelo Whisper |
| Textos | `scripts/overlay.py` (Pillow) | 450 quadros PNG sincronizados com a fala |
| Lipsync | site do Kling + `scripts/kling_lipsync_*.mjs` | cenas 1 e 3 com a boca sincronizada |
| Montagem | `scripts/montar.sh` (ffmpeg) | 15,000 s, sem marca d'água, −14 LUFS |
| Publicação | [yt-pubx](https://github.com/inematds/yt-pubx) | [Short no YouTube](https://www.youtube.com/watch?v=XOyI6dT6ioQ) |

## Arquivos

```
scripts/
  tts_elevenlabs.py          narração (chave em ELEVENLABS_API_KEY)
  overlay.py                 camada de textos 1080x1920, 30 fps
  kling_lipsync_enviar.mjs   envia vídeo + áudio ao Lip Sync do site (confere o custo antes)
  kling_lipsync_baixar.mjs   baixa só os resultados pedidos
  montar.sh                  cortes, troca pelas cenas com lipsync e montagem final
guia/                        página do guia (PT, EN, ES)
```

## Problemas que apareceram

Lipsync esquecido na 1ª versão, CLI do Kling sem áudio, envio "sem confirmação" que tinha entrado, download de trabalhos antigos, marca d'água, formato de áudio recusado (403), mp3 vazio, narração longa, quadro 0 vazio, texto sem contraste e folha de quadros fora de ordem. A correção de cada um está no [guia](https://inematds.github.io/ugc-agente/guia/#problemas).

---

[INEMA.CLUB](https://inema.club) · conteúdo aberto e gratuito
