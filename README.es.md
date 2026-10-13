# 🎬 UGC con agente — video promocional hecho por un agente de IA

[![Video UGC con agente](guia/assets/banner-es.jpg)](https://inematds.github.io/ugc-agente/guia/es/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## Qué es

Este proyecto cuenta cómo un agente de IA (Claude Code) produjo un video promocional de 15 segundos de INEMA.CLUB en estilo UGC, ese video "de gente real hablándole a la cámara" de las redes sociales. Sirve para quien crea contenido y quiere delegar la producción a un agente. Muestra la idea, los pasos con los comandos usados, los consejos que marcaron la diferencia y los problemas que surgieron en el camino. Para repetirlo necesitas una suscripción de Kling AI, una cuenta de ElevenLabs, ffmpeg, Python y un navegador con sesión iniciada en Kling.

## 📖 Guía de uso

Guía completa (idea, consejos, problemas y paso a paso): **https://inematds.github.io/ugc-agente/guia/es/**

## El consejo principal

**Usa tu suscripción y dale al agente la capacidad de operar el sitio.**

- Las escenas salieron de la suscripción Pro de Kling con la CLI oficial (`kling`): 120 créditos, sin clave de API.
- El Lip Sync de Kling solo existe en el sitio. El agente abrió un Chromium con la sesión ya iniciada (`--remote-debugging-port`) y, mediante Playwright, envió las escenas, revisó el costo en el botón y descargó el resultado: 10 créditos más.

## Cómo se hizo

| Etapa | Herramienta | Resultado |
|---|---|---|
| Escenas | `kling omni_ref_video` (v3.0 Omni, 15 s, 9:16, 1080p, sin audio) | 3 tomas a partir de la imagen de referencia |
| Voz | ElevenLabs `eleven_multilingual_v2`, voz Amanda Kelly, velocidad 1,12 | 13,3 s, verificada con Whisper |
| Textos | `scripts/overlay.py` (Pillow) | 450 cuadros PNG sincronizados con la voz |
| Lipsync | sitio de Kling + `scripts/kling_lipsync_*.mjs` | escenas 1 y 3 con la boca sincronizada |
| Montaje | `scripts/montar.sh` (ffmpeg) | 15,000 s, sin marca de agua, −14 LUFS |
| Publicación | [yt-pubx](https://github.com/inematds/yt-pubx) | [Short en YouTube](https://www.youtube.com/watch?v=XOyI6dT6ioQ) |

## Archivos

```
scripts/
  tts_elevenlabs.py          narración (clave en ELEVENLABS_API_KEY)
  overlay.py                 capa de textos 1080x1920, 30 fps
  kling_lipsync_enviar.mjs   envía video + audio al Lip Sync del sitio (revisa el costo antes)
  kling_lipsync_baixar.mjs   descarga solo los resultados pedidos
  montar.sh                  cortes, cambio por las escenas con lipsync y montaje final
guia/                        página de la guía (PT, EN, ES)
```

## Problemas que surgieron

Lipsync olvidado en la 1.ª versión, CLI de Kling sin audio, envío "sin confirmación" que sí había entrado, descarga de trabajos antiguos, marca de agua, formato de audio rechazado (403), mp3 vacío, narración larga, cuadro 0 vacío, texto sin contraste y hoja de cuadros fuera de orden. La corrección de cada uno está en la [guía](https://inematds.github.io/ugc-agente/guia/es/#problemas).

---

[INEMA.CLUB](https://inema.club) · contenido abierto y gratuito
