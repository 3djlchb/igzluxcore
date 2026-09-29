# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 José Chamba and IngeTrazo contributors.

from __future__ import annotations

from pathlib import Path


class LuxCoreExporter:

    @staticmethod
    def get_render_output_dir(app) -> Path:
        """Obtiene la carpeta donde se guardarán la escena y los renders."""
        output_dir = Path.home() / "IngeTrazo_Renders"
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir

    @staticmethod
    def generate_scene_files(output_dir: Path, settings: dict) -> tuple[Path, Path]:
        output_dir.mkdir(parents=True, exist_ok=True)

        cfg_path = output_dir / "render.cfg"
        scn_path = output_dir / "scene.scn"
        png_path = output_dir / "render_output.png"

        # 1. Crear un archivo .scn básico si no existe
        if not scn_path.exists():
            scn_content = """# Escena básica de prueba para LuxCore
scene.materials.whitediff.type = matte
scene.materials.whitediff.kd = 0.75 0.75 0.75

scene.objects.box.material = whitediff
scene.objects.box.ply = plane.ply
"""
            scn_path.write_text(scn_content, encoding="utf-8")

        # 2. Configurar el .cfg con RUTAS RELATIVAS (evita errores en luxcoreui)
        # Usamos solo el nombre del archivo o ruta relativa con '/'
        cfg_lines = [
            f"renderengine.type = {settings.get('engine_type', 'PATHCPU')}",
            f"sampler.type = {settings.get('sampler_type', 'SOBOL')}",
            f'scene.file = "{scn_path.name}"',  # Solo el nombre del archivo en la misma carpeta
            f"film.width = {settings.get('width', 1280)}",
            f"film.height = {settings.get('height', 720)}",
            # Salida del PNG
            "film.outputs.1.type = RGB_IMAGEPIPELINE",
            f'film.outputs.1.filename = "{png_path.name}"',
            "periodicsave.film.outputs.period = 5",
        ]

        if settings.get("use_time"):
            cfg_lines.append(f"halttime = {settings.get('halt_time', 60)}")

        if settings.get("use_samples"):
            cfg_lines.append(f"haltpp = {settings.get('halt_samples', 20)}")

        if settings.get("use_denoiser"):
            cfg_lines.append("film.imagepipelines.1.0.type = BIDIR_OIDN")

        cfg_path.write_text("\n".join(cfg_lines), encoding="utf-8")

        return cfg_path, png_path