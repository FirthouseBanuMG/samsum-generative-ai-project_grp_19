"""Test inference-device selection without loading model weights."""

from types import SimpleNamespace

import pytest

from structured_output import run_structured_output


def test_cpu_device_is_available_by_default():
    assert run_structured_output.resolve_inference_device() == "cpu"


def test_auto_device_uses_cpu_when_cuda_is_unavailable(monkeypatch):
    monkeypatch.setattr(
        run_structured_output.torch,
        "cuda",
        SimpleNamespace(is_available=lambda: False),
        raising=False,
    )

    assert run_structured_output.resolve_inference_device("auto") == "cpu"


def test_cuda_request_fails_clearly_when_cuda_is_unavailable(monkeypatch):
    monkeypatch.setattr(
        run_structured_output.torch,
        "cuda",
        SimpleNamespace(is_available=lambda: False),
        raising=False,
    )

    with pytest.raises(RuntimeError, match="no CUDA device is available"):
        run_structured_output.resolve_inference_device("cuda")


def test_unknown_device_is_rejected():
    with pytest.raises(ValueError, match="device must be one of"):
        run_structured_output.resolve_inference_device("tpu")
