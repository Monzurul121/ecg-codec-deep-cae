# Deep Convolutional Autoencoder for ECG Compression (Deep-CAE)

A learned, flexible-rate ECG codec: a single-encoder, multi-decoder convolutional autoencoder that adapts its compression rate to a distortion bound.

> **Status: preview.** This repository documents the method and its interface. The implementation and pretrained checkpoints will be released later.

## Overview

Learned codecs use neural networks to find compact representations of a signal. A convolutional autoencoder squeezes each ECG frame into a short latent code (the encoder) and rebuilds the frame from that code (the decoder).

Most autoencoder codecs offer a single compression rate. This one uses one encoder with several decoders, one for each latent size, so a single model offers several rates. For each record, the codec picks the most compact rate that keeps the reconstruction within a chosen distortion bound. The result is a flexible rate with a controlled error, following the constant-error idea of the source method.

## How it works

1. **Normalization.** The record is scaled to the range −1 to 1 by its peak absolute amplitude. The scale factor is stored so the decoder can undo it.
2. **Framing.** The signal is split into frames of 1024 samples, and the last frame is zero-padded.
3. **Cascaded encoding.** Three convolutional encoder stages run one after another. They shorten each frame to latents of 256, 128 and 64 values, which are 4, 8 and 16 times shorter than the frame.
4. **Rate selection.** Starting from the most compact latent, the codec reconstructs the record and checks its PRD against the distortion bound. It keeps the most compact latent that stays within the bound, and uses the largest latent if none does.
5. **Quantization.** The selected latent code is symmetrically quantized to the chosen bit depth. Its scale is stored with the payload.
6. **Entropy coding.** The quantized code is delta coded and then Huffman coded.
7. **Decoding.** The decoder reverses the entropy coding and the quantization, passes the code through the decoder that matches its latent size, and rescales the result.

## Architecture overview

| Component | Input | Output |
|---|---|---|
| Encoder stage 1 | 1024-sample frame | latent of 256 values |
| Encoder stage 2 | latent of 256 | latent of 128 values |
| Encoder stage 3 | latent of 128 | latent of 64 values |
| Decoders 1–3 | latent of 256, 128 or 64 | reconstructed 1024-sample frame |

All stages are 1-D convolutional; the decoders use transposed convolutions and end with a tanh output. The model is trained to reproduce its input frames. The full layer specification will be released with the code.

## Key properties

- **Several rates from one model:** no need to train a separate network for each compression level.
- **Error-controlled rate selection:** the rate adapts to each record to stay within the distortion bound.
- **Two settings:** the distortion bound and the bit depth of the latent code.
- **Self-contained payload:** all side information needed for decoding is stored in the payload and counted in the compression ratio. The decoder needs the same checkpoint as the encoder.
- **CPU or GPU:** the model is small enough to run on a CPU.

## Measuring performance

- **Compression ratio (CR):** the size of the signal stored as 16-bit samples, divided by the size of the compressed payload, side information included.
- **Percent root-mean-square difference (PRD):** the root-mean-square reconstruction error as a percentage of the root-mean-square value of the original signal.

## Limitations

- The codec needs pretrained weights. Like any learned model, it works best on signals similar to its training data.
- It expects ECG sampled at 360 Hz.
- It needs more computation than classical transform codecs.

## Typical uses

ECG compression in remote-monitoring systems that need high compression ratios with a controlled reconstruction error.

## Interface (preview)

```python
from deep_cae_codec import load_checkpoint, compress, decompress, compression_ratio, prd

load_checkpoint("checkpoint.pt")                       # pretrained weights
payload = compress(x, max_prd=max_prd, quant_bits=quant_bits)   # x: ECG at 360 Hz
x_hat = decompress(payload)

print(compression_ratio(x, payload))    # 16-bit original size / payload size
print(prd(x, x_hat))                    # reconstruction error in percent
```

In this preview, these functions raise `NotImplementedError`. They show the interface that the released code will provide.

## Roadmap

- Release the implementation and pretrained checkpoints.
- Add usage examples and documentation.

## Reference

This codec adapts the method of:

> T. Bekiryazıcı, G. Aydemir, and H. Gürkan, "Electrocardiogram signal compression using deep convolutional autoencoder with constant error and flexible compression rate," *IRBM*, vol. 45, no. 6, p. 100859, 2024. doi: [10.1016/j.irbm.2024.100859](https://doi.org/10.1016/j.irbm.2024.100859)

If you use this method, please cite the original paper.

## Copyright

Copyright © 2026 Md Monzurul Islam Rabu. All rights reserved.

No permission is granted to use, copy, modify or redistribute the contents of this repository. An open-source license will be added when the code is released.
