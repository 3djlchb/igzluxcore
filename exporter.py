from __future__ import annotations

from datetime import datetime
from pathlib import Path


class LuxCoreExporter:
    """Módulo encargado de determinar rutas y generar los archivos .ply, .scn y .cfg."""

    @staticmethod
    def get_render_output_dir(app) -> Path:
        """Obtiene la carpeta 'luxcore_renders' en la ubicación del documento .igz activo."""
        doc_path = None
        if hasattr(app, "current_document_path") and app.current_document_path:
            doc_path = Path(app.current_document_path)
        elif hasattr(app, "active_document") and getattr(app.active_document, "path", None):
            doc_path = Path(app.active_document.path)

        if doc_path and doc_path.exists():
            target_dir = doc_path.parent / "luxcore_renders"
        else:
            target_dir = Path.home() / ".ingetrazo" / "luxcore_renders"

        target_dir.mkdir(parents=True, exist_ok=True)
        return target_dir

    @classmethod
    def generate_scene_files(cls, render_dir: Path, settings: dict) -> tuple[Path, Path]:
        mesh_ply_path = render_dir / "ingetrazo_mesh.ply"
        scn_path = render_dir / "scene.scn"
        cfg_path = render_dir / "scene.cfg"

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_png_path = render_dir / f"img_{timestamp}.png"

        # 1. Geometría PLY base
        with open(mesh_ply_path, "w", encoding="utf-8") as f:
            f.write("""ply
format ascii 1.0
element vertex 4
property float x
property float y
property float z
element face 2
property list uchar int vertex_indices
end_header
-2.0 -2.0 0.0
2.0 -2.0 0.0
2.0 2.0 0.0
-2.0 2.0 0.0
3 0 1 2
3 0 2 3
""")

        # 2. Definición de Escena SCN
        with open(scn_path, "w", encoding="utf-8") as f:
            f.write(f"""
scene.materials.mat_ground.type = matte
scene.materials.mat_ground.kd = 0.8 0.8 0.8

scene.objects.ground.ply = {mesh_ply_path.as_posix()}
scene.objects.ground.material = mat_ground

scene.camera.lookat.orig = 0 -5 5
scene.camera.lookat.target = 0 0 0
scene.camera.up = 0 0 1
scene.camera.fieldofview = 45

scene.lights.dist_light.type = sun
scene.lights.dist_light.dir = 0.5 0.5 -1.0
scene.lights.dist_light.gain = 1.0 1.0 1.0
""")

        # 3. Configuración CFG dinámica
        cfg_lines = [
            f"renderengine.type = {settings.get('engine_type', 'PATHCPU')}",
            f"sampler.type = {settings.get('sampler_type', 'SOBOL')}",
            f"scene.file = {scn_path.as_posix()}",
            f"film.width = {settings.get('width', 1280)}",
            f"film.height = {settings.get('height', 720)}",
            f"film.outputs.1.type = RGB_IMAGEPIPELINE",
            f"film.outputs.1.filename = {image_png_path.as_posix()}",
            "periodicsave.film.outputs.period = 5",
        ]

        if settings.get("use_time"):
            cfg_lines.append(f"halttime = {settings.get('halt_time', 60)}")
        if settings.get("use_samples"):
            cfg_lines.append(f"haltpp = {settings.get('halt_samples', 20)}")
        if settings.get("use_denoiser"):
            cfg_lines.append("film.imagepipelines.1.0.type = BIDIR_OIDN")

        with open(cfg_path, "w", encoding="utf-8") as f:
            f.write("\n".join(cfg_lines))

        return cfg_path, image_png_path