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
