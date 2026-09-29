# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 José Chamba and IngeTrazo contributors.

from __future__ import annotations

from .config import _t
from .ui import IGZLuxCorePanel

__version__ = "0.1.0"
__author__ = "José Chamba"
__description__ = "Extensión de renderizado interactivo con LuxCoreRender para IngeTrazo"

__all__ = ["setup", "IGZLuxCorePanel"]


def setup(app) -> None:
    """Punto de entrada de la extensión al cargarse en IngeTrazo."""
    panel = IGZLuxCorePanel(app)
    app.add_panel(_t("LuxCore Render"), panel)

    if hasattr(app, "on_document_changed"):
        app.on_document_changed(panel.refresh)