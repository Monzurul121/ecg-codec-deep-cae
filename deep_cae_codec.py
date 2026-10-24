"""Deep convolutional autoencoder for ECG compression (Deep-CAE): public
interface (preview).

The implementation and pretrained checkpoints will be released later. Until
then, every function below raises NotImplementedError.

Copyright (c) 2026 Md Monzurul Islam Rabu. All rights reserved.
"""
from __future__ import annotations

import numpy as np

__all__ = ["load_checkpoint", "compress", "decompress", "compression_ratio",
           "prd"]

RELEASE_MESSAGE = (
    "This is a preview of the interface. The implementation and pretrained "
    "checkpoints will be released later. See README.md."
)


def load_checkpoint(path: str, device: str = "cpu") -> None:
    """Load pretrained autoencoder weights used by :func:`compress` and
    :func:`decompress`.

    Parameters
    ----------
    path : str
        Path to a checkpoint file.
    device : str
        Device to run the model on, for example ``"cpu"`` or ``"cuda"``.
    """
    raise NotImplementedError(RELEASE_MESSAGE)


def compress(x: np.ndarray, max_prd: float, quant_bits: int) -> bytes:
    """Compress a single-lead ECG sampled at 360 Hz.

    Parameters
    ----------
    x : np.ndarray
        1-D float array: single-lead ECG sampled at 360 Hz.
    max_prd : float
        Distortion bound, as PRD in percent, used to select the compression
        rate (latent size).
    quant_bits : int
        Number of bits used to quantize the latent code.

    Returns
    -------
    bytes
        Self-contained payload, including all side information needed to
        decode it with the same checkpoint.
    """
    raise NotImplementedError(RELEASE_MESSAGE)


def decompress(payload: bytes) -> np.ndarray:
    """Reconstruct the ECG from a payload produced by :func:`compress`.

    Returns
    -------
    np.ndarray
        1-D float array with the same length as the original signal.
    """
    raise NotImplementedError(RELEASE_MESSAGE)


def compression_ratio(x: np.ndarray, payload: bytes) -> float:
    """Compression ratio of ``payload`` relative to ``x``.

    Defined as the size of a 16-bit uncompressed signal (2 bytes per sample)
    divided by the payload size in bytes, side information included.
    """
    raise NotImplementedError(RELEASE_MESSAGE)


def prd(x: np.ndarray, x_hat: np.ndarray) -> float:
    """Percent root-mean-square difference (PRD, %) between the original
    signal ``x`` and the reconstruction ``x_hat``."""
    raise NotImplementedError(RELEASE_MESSAGE)
