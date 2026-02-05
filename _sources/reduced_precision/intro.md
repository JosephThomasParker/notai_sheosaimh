# Representation of numbers

Real numbers can be represented as

$$
x = (-1)^{\mathrm{sign}} \times (1.\mathrm{mantissa}) \times 2^{\mathrm{exponent}}.
$$

In a computer, the sign, mantissa and exponent are all expressed in binary. 
The sign is always one bit, while the mantissa and exponent use a different number of bits, depending on the precision.

## Single Precision, FP32

In single precision, the mantissa has 23 bits, and the exponent has 8 bits.
The numbers that can be expressed in FP32 are

$$
x = (-1)^S \times (1.b_1b_2\ldots b_{23}) \times 2^{(E-127)}
$$

where $S$ is the sign, $\{b_i\}$ are the mantissa bits, and $E$ is the exponent, with _exponent bias_ 127.
With 8 bits, $E$ can represent 256 integers ($2^8=256$), but two of these (0 and 255) are special exponents reserved for subnormal, infinite and NaN numbers.
Therefore, $E$ can take the values $1, 2, \dots, 254$, so that with the bias of 127, the total exponent covers the range from -126 to 127.

Since the mantissa is between 1 and 2, the range of positive numbers that FP32 is between

$$
1.0 \times 2^{-126} \approx 1.175 \times 10^{-38}
$$

and

$$
1.111\ldots111_2 \times 2^{127} \approx 3.403 \times 10^{38}.
$$

The mantissa has 23 bits, so the precision is 

$$
2^{-24}\approx 6\times 10^{-8}.
$$

## Other precision types

| Representation    | Exponent bits | Mantissa bits | Exponent bias | Min positive | Max        | Precision     |
| ----------------- | ------------- | ------------- | ------------- | ------------ | ---------- | ------------- |
| **FP16 (half)**   | 5             | 10            | 15            | $6.10 \times 10^{-05}$     | $6.55\times10^4$     | $9.8\times10^{-4}$        |
| **bfloat16 (bf16)**      | 8             | 7             | 127           | $1.18 \times 10^{-38}$     | $3.40\times10^{38}$    | $7.8\times10^{-3}$        |
| **FP32 (single)** | 8             | 23            | 127           | $1.175 \times 10^{-38}$    | $3.403\times10^{38}$   | $5.96\times10^{-8}$       |
| **FP64 (double)** | 11            | 52            | 1023          | $2.225 \times 10^{-308}$   | $1.798\times10^{308}$  | $1.11\times10^{-16}$      |
| **FP128 (quad)**  | 15            | 112           | 16383         | $3.362 \times 10^{-4932}$  | $1.189\times10^{4932}$ | $1.93\times10^{-34}$      |

**Notes.**

1. This table shows values for normalized numbers, which have the form discussed above. It ignores _subnormal_ numbers. These numbers drop the implicit leading one in the significand and use the smallest exponent. For example in FP32, subnormal numbers have the form $(0.\mathrm{mantissa})\times 2^{-126}$. This allows a greater range of small numbers, at the cost of reduced precision.
2. bfloat16 is designed for use in mixed precision with FP32; bf16 has exponent bits chosen so that it matches the range of FP32, but with much reduced precision. The idea is that arithmetic can be done quickly in low precision using bf16, with results accumulated using FP32. 
