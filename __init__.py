# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 José Chamba and IngeTrazo contributors.

from .config import _t
from .ui import IGZLuxCorePanel


def setup(app) -> None:
    """Punto de entrada de la extensión al cargarse en IngeTrazo."""
    panel = IGZLuxCorePanel(app)
    app.add_panel(_t("LuxCore Render"), panel)
    app.on_document_changed(panel.refresh)