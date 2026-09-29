from __future__ import annotations

try:
    from core.i18n import current_language
except ImportError:
    import locale
    def current_language() -> str:
        lang, _ = locale.getdefaultlocale()
        return lang.split("_")[0] if lang else "es"

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
    },
}


def _t(text: str, **kw) -> str:
    out = _TEXTS.get(current_language(), {}).get(text, text)
    return out.format(**kw) if kw else out