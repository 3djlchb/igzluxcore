# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 José Chamba and IngeTrazo contributors.

from __future__ import annotations

import locale

try:
    from core.i18n import current_language
except ImportError:
    def current_language() -> str:
        try:
            lang, _ = locale.getlocale()
        except Exception:
            lang = None
        if not lang:
            return "es"
        # Normalizar códigos como 'pt_BR' a 'pt-BR' o 'es_EC' a 'es'
        lang_code = lang.replace("_", "-")
        return lang_code


_TEXTS = {
    "es": {
        "LuxCore Render": "LuxCore Render",
        "Engine Setup": "Configuración del Motor",
        "Executable Path:": "Ejecutable:",
        "Browse...": "Buscar...",
        "Compute Device:": "Dispositivo de Cómputo:",
        "Halt Conditions": "Condiciones de Parada",
        "Use Time (seconds)": "Usar Tiempo (segundos)",
        "Use Samples (Spp)": "Usar Muestras (Spp)",
        "Image & Denoising": "Imagen y Denoiser",
        "Resolution:": "Resolución:",
        "Enable OIDN Denoiser": "Habilitar OIDN Denoiser",
        "Status & Output": "Estado y Salida",
        "Output Folder:": "Carpeta de Salida:",
        "Status:": "Estado:",
        "Ready": "Listo",
        "Export & Render": "Exportar .cfg y Renderizar",
        "Exporting scene...": "Exportando escena...",
        "Rendering started...": "Renderizado iniciado...",
        "Render finished": "Renderizado finalizado",
        "Error: Invalid executable path": "Error: Ruta no válida",
        "Select LuxCore Executable": "Seleccionar ejecutable de LuxCore",
        "Select Output Folder": "Seleccionar carpeta de salida",
    },
    "pt-BR": {
        "LuxCore Render": "LuxCore Render",
        "Engine Setup": "Configuração do Motor",
        "Executable Path:": "Executável:",
        "Browse...": "Navegar...",
        "Compute Device:": "Dispositivo de Computação:",
        "Halt Conditions": "Condições de Parada",
        "Use Time (seconds)": "Usar Tempo (segundos)",
        "Use Samples (Spp)": "Usar Amostras (Spp)",
        "Image & Denoising": "Imagem e Denoiser",
        "Resolution:": "Resolução:",
        "Enable OIDN Denoiser": "Habilitar OIDN Denoiser",
        "Status & Output": "Status e Saída",
        "Output Folder:": "Pasta de Saída:",
        "Status:": "Status:",
        "Ready": "Pronto",
        "Export & Render": "Exportar .cfg e Renderizar",
        "Exporting scene...": "Exportando cena...",
        "Rendering started...": "Renderização iniciada...",
        "Render finished": "Renderização finalizada",
        "Error: Invalid executable path": "Erro: Caminho inválido",
        "Select LuxCore Executable": "Selecionar executável do LuxCore",
        "Select Output Folder": "Selecionar pasta de saída",
    },
}


def _t(text: str, **kw) -> str:
    lang = current_language()

    # Intentar obtener traducción directa o variante simplificada (ej: 'es-EC' -> 'es')
    lang_key = lang if lang in _TEXTS else lang.split("-")[0]
    
    translations = _TEXTS.get(lang_key, _TEXTS.get("es", {}))
    out = translations.get(text, _TEXTS.get("es", {}).get(text, text))

    return out.format(**kw) if kw else out