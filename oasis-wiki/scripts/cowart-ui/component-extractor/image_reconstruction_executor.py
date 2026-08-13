from __future__ import annotations

import importlib
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


UNAVAILABLE_CODE = "LAYER_RECONSTRUCTION_UNAVAILABLE"


class ReconstructionUnavailable(RuntimeError):
    pass


class ImageReconstructionExecutor(ABC):
    """Provider-neutral image edit/inpainting executor contract."""

    executor_id = "unconfigured"

    @abstractmethod
    def capabilities(self) -> set[str]:
        raise NotImplementedError

    @abstractmethod
    def reconstruct(self, job: dict[str, Any], source_root: Path, output_root: Path) -> dict[str, Any]:
        raise NotImplementedError


def load_executor(spec: str | None) -> ImageReconstructionExecutor:
    if not spec:
        raise ReconstructionUnavailable(UNAVAILABLE_CODE)
    if ":" not in spec:
        raise ReconstructionUnavailable(f"{UNAVAILABLE_CODE}: executor must use module:Class")
    module_name, class_name = spec.split(":", 1)
    try:
        executor_class = getattr(importlib.import_module(module_name), class_name)
        executor = executor_class()
    except (ImportError, AttributeError, TypeError) as error:
        raise ReconstructionUnavailable(f"{UNAVAILABLE_CODE}: {error}") from error
    if not isinstance(executor, ImageReconstructionExecutor):
        raise ReconstructionUnavailable(f"{UNAVAILABLE_CODE}: executor does not implement ImageReconstructionExecutor")
    if "image_edit_inpainting" not in executor.capabilities():
        raise ReconstructionUnavailable(f"{UNAVAILABLE_CODE}: executor lacks image_edit_inpainting")
    return executor
