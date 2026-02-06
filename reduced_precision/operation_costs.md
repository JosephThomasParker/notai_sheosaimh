---
title: Bits, bytes and operation costs
layout: post
---

# Operation Costs

In this section, we discuss the cost of doing operations with different precision types.
"Cost" can mean many things - run time, energy consumption, area required on the chip - but here we are interested in code performance, so focus on the time for operations to complete.
We focus on two kinds of operations: memory transfers and arithmetic operations. 

## Memory transfers

### Memory Footprint
Each 0 or 1 in a number's representation is a _bit_.
So FP16 and bf16 are 16 bit, FP32 is 32 bit, and FP64 is 64 bit.

There are 8 bits in a byte, so FP16 and bf16 are 2 bytes, FP32 is 4 bytes and FP64 is 8 bytes.

### Memory transfers

As a first approximation, memory transfers happen at a constant rate, proportional to the amount of data to be transferred.
Therefore, FP32 are transferred twice as fast as FP64, and twice as slow as FP16/bf16. 
At lower precisions, the speed-up can be even greater, owing to vectorization and better cache efficiency.
In memory bandwidth limited codes, this is a huge effect!

## Computation Cost

It is tempting to treat arithmetic operations like they are algorithms, and count their computational complexity.
For example, to add two numbers in floating point, we compare their exponents, shift the smaller number's mantissa accordingly, add the shifted mantissae, normalize the result (adjust the exponent and mantissa so it’s in proper floating-point form), and round.
This whole operation takes $O(E + 3M)$, where $E$ and $M$ are the number of bits in the exponents and mantissa of the precision type respectively. 
Similarly, multiplication takes $O(M^2)$ operations, and fused add multiply (FMA, $a*b+c$ in a single operation) also takes $O(M^2)$.

This is interesting - and details like rounding will become important later - but for now, the more important point is that the performance of code is determined by how these operations are implemented in hardware.
There are two aspects that determine speed: latency and throughput. 
Latency is the initial overhead of performing an operation,
while throughput is the rate at which operations are performed (in units of operations per clock cycle per compute unit).
In a sufficiently compute-bound code where operations can be pipelined, latency can be neglected, and "speed" is determined by throughput.

By this metric, all three of add, multiply and FMA take the same number of clock cycles, and the real difference in speed comes down to how different hardware handles difference precision types.

### Hardware

| Precision    | CPU throughput (per cycle per SIMD unit)                                                     | GPU throughput (per cycle per CUDA core)                                            | Notes                                                                             |
| ------------ | -------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| FP16         | Often emulated in FP32, little benefit; sometimes 2× FP32 if AVX-512 BF16/F16 support exists | Tensor cores can do 2–8× FP32 rate for GEMM; otherwise ~2× FP32                     | Lower precision can pack multiple values per register; limited dynamic range                |
| BF16         | Emulated in FP32 (1× FP32 speed)                                                             | Often same as FP16: hardware accumulates in FP32, so very fast                      | Exponent matches FP32 → safe for mixed-precision matmuls                                    |
| FP32         | 1× (baseline)                                                                                | 1× per standard CUDA core; tensor cores can use 2× speed if packing multiple values | Standard single-precision                                                                   |
| FP64         | 0.5–1× FP32 (desktop CPU often same as FP32 with AVX-512)                                    | 1/2 to 1/32 × FP32 depending on GPU generation                                      | Many consumer GPUs have far fewer FP64 units than FP32; pro cards (A100, MI100) much better |
| FP128 / Quad | Rare on CPU; huge slowdowns                                                                  | Almost never supported                                                              | Mostly used in scientific CPU libraries; very high latency and low throughput               |


## Summary

* **Memory-bound codes:** Throughput varies linearly with bits (e.g., FP32 transfers 2x FP64, FP16 0.5x FP32).

* **Compute-bound codes:** GPU hardware dominates; FP32 is usually fastest in terms of real wall-clock per scalar op, but FP16/BF16 GEMM can be much faster if tensor cores are used.

* **CPU vs GPU:** CPUs tend to treat FP32 and FP64 more similarly in vectorized code; GPUs have extreme differences in FP64/FP32 throughput.

* **Mixed precision:** Doing FP16 multiply + FP32 accumulation lets you keep FP32 dynamic range but get FP16 memory/compute speedups.
