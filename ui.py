from __future__ import annotations

import os
import sys
from pathlib import Path

from PySide6.QtCore import QProcess
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from .config import _t
from .exporter import LuxCoreExporter


class IGZLuxCorePanel(QWidget):
    """Panel lateral de PySide6 para controlar la exportación de LuxCore."""

    def __init__(self, app) -> None:
        super().__init__()
        self.app = app
        self.process: QProcess | None = None
        self._init_ui()
        self.refresh()

    def _init_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(4, 4, 4, 4)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(10)

        # 1. Configuración del Motor
        group_engine = QGroupBox(_t("Engine Setup"))
        form_engine = QFormLayout(group_engine)

        self.exe_path_input = QLineEdit()
        self.exe_path_input.setPlaceholderText("Ruta a luxcoreui...")
        btn_browse_exe = QPushButton(_t("Browse..."))
        btn_browse_exe.clicked.connect(self._browse_executable)

        row_exe = QHBoxLayout()
        row_exe.addWidget(self.exe_path_input)
        row_exe.addWidget(btn_browse_exe)
        form_engine.addRow(_t("Executable Path:"), row_exe)

        self.combo_device = QComboBox()
        self.combo_device.addItems(["CPU (PATHCPU)", "GPU / OpenCL (PATHOCL)", "BiDirectional CPU (BIDIRCPU)"])
        form_engine.addRow(_t("Compute Device:"), self.combo_device)

        self.combo_sampler = QComboBox()
        self.combo_sampler.addItems(["SOBOL", "RANDOM", "METROPOLIS"])
        form_engine.addRow("Sampler:", self.combo_sampler)

        layout.addWidget(group_engine)

        # 2. Halt Conditions
        group_halt = QGroupBox(_t("Halt Conditions"))
        form_halt = QFormLayout(group_halt)

        self.chk_use_time = QCheckBox(_t("Use Time (seconds)"))
        self.chk_use_time.setChecked(True)
        self.spin_halt_time = QSpinBox()
        self.spin_halt_time.setRange(1, 86400)
        self.spin_halt_time.setValue(60)
        form_halt.addRow(self.chk_use_time, self.spin_halt_time)

        self.chk_use_samples = QCheckBox(_t("Use Samples (Spp)"))
        self.chk_use_samples.setChecked(True)
        self.spin_halt_samples = QSpinBox()
        self.spin_halt_samples.setRange(1, 100000)
        self.spin_halt_samples.setValue(20)
        form_halt.addRow(self.chk_use_samples, self.spin_halt_samples)

        layout.addWidget(group_halt)

        # 3. Resolución y Denoiser
        group_film = QGroupBox(_t("Image & Denoising"))
        form_film = QFormLayout(group_film)

        self.spin_width = QSpinBox()
        self.spin_width.setRange(16, 8192)
        self.spin_width.setValue(1280)

        self.spin_height = QSpinBox()
        self.spin_height.setRange(16, 8192)
        self.spin_height.setValue(720)

        row_res = QHBoxLayout()
        row_res.addWidget(QLabel("W:"))
        row_res.addWidget(self.spin_width)
        row_res.addWidget(QLabel("H:"))
        row_res.addWidget(self.spin_height)
        form_film.addRow(_t("Resolution:"), row_res)

        self.chk_denoiser = QCheckBox(_t("Enable OIDN Denoiser"))
        form_film.addRow(self.chk_denoiser)

        layout.addWidget(group_film)

        # 4. Estado y Salida
        group_status = QGroupBox(_t("Status & Output"))
        form_status = QFormLayout(group_status)

        self.lbl_output_path = QLabel("-")
        self.lbl_output_path.setWordWrap(True)
        self.lbl_output_path.setStyleSheet("color: #7f8c8d; font-size: 11px;")
        form_status.addRow(_t("Output Folder:"), self.lbl_output_path)

        self.lbl_status = QLabel(_t("Ready"))
        form_status.addRow(_t("Status:"), self.lbl_status)
        layout.addWidget(group_status)

        # Botón Render
        self.btn_render = QPushButton(_t("Export & Render"))
        self.btn_render.setStyleSheet("font-weight: bold; padding: 8px; background-color: #27ae60; color: white;")
        self.btn_render.clicked.connect(self._export_and_render)
        layout.addWidget(self.btn_render)

        layout.addStretch()
        scroll.setWidget(container)
        main_layout.addWidget(scroll)

    def _browse_executable(self) -> None:
        filter_str = (
            "LuxCore Executable (luxcoreui.exe luxcoreui);;All Files (*)"
            if sys.platform == "win32"
            else "LuxCore Executable (luxcoreui);;All Files (*)"
        )
        file_path, _ = QFileDialog.getOpenFileName(self, _t("Select LuxCore Executable"), "", filter_str)
        if file_path:
            self.exe_path_input.setText(file_path)

    def _get_settings(self) -> dict:
        engine_type = "PATHCPU"
        if "PATHOCL" in self.combo_device.currentText():
            engine_type = "PATHOCL"
        elif "BIDIRCPU" in self.combo_device.currentText():
            engine_type = "BIDIRCPU"

        return {
            "engine_type": engine_type,
            "sampler_type": self.combo_sampler.currentText(),
            "use_time": self.chk_use_time.isChecked(),
            "halt_time": self.spin_halt_time.value(),
            "use_samples": self.chk_use_samples.isChecked(),
            "halt_samples": self.spin_halt_samples.value(),
            "width": self.spin_width.value(),
            "height": self.spin_height.value(),
            "use_denoiser": self.chk_denoiser.isChecked(),
        }

    def _export_and_render(self) -> None:
        exe_path = self.exe_path_input.text().strip()
        if not exe_path or not os.path.exists(exe_path):
            self.lbl_status.setText(_t("Error: Invalid executable path"))
            QMessageBox.critical(self, "Error", "Por favor selecciona la ruta correcta a luxcoreui.")
            return

        self.lbl_status.setText(_t("Exporting scene..."))
        render_dir = LuxCoreExporter.get_render_output_dir(self.app)
        cfg_path, _ = LuxCoreExporter.generate_scene_files(render_dir, self._get_settings())

        self.lbl_status.setText(_t("Rendering started..."))

        self.process = QProcess(self)
        self.process.finished.connect(self._on_render_finished)
        self.process.start(exe_path, [str(cfg_path)])

    def _on_render_finished(self) -> None:
        self.lbl_status.setText(_t("Render finished"))

    def refresh(self) -> None:
        render_dir = LuxCoreExporter.get_render_output_dir(self.app)
        self.lbl_output_path.setText(str(render_dir))