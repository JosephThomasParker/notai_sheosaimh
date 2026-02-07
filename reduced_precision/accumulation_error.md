---
title: Accumualation Error
layout: post
---

# Representation Error

Representation error is the error that arises from representing a number using
a finite number of binary digits. 
Floating-point numbers store a number as a sign, exponent, and mantissa, which
allows exact representation of only certain values (like powers of two). 
Numbers such as 1.0 are represented exactly in binary, but most decimal fractions, e.g. 0.1,
must be rounded to the nearest representable value. 
The difference between the true number and its floating-point representation is
the representation error, which is typically on the order of the machine
epsilon for the given precision.
For example, in double precision, the mantissa has 53 binary bits, corresponding to around
16 decimal places of accuracy. Therefore a number like $10^{-3}$ is only accurate up to $\sim 10^{-19}$,
that is, it has an error in its 16th decimal place.

Representation is usually negligible by itself, but becomes significant when repeated operations accumulate it,
leading to the much larger _accumulation error_.

# Accumulation Error

Accumulation error is the error that results from repeatedly rounding numbers
during numerical operations.  Floating-point arithmetic is not exact: each
operation produces a result that is rounded to the nearest representable value,
introducing an error on the order of machine epsilon, which characterizes the
relative spacing between representable numbers at a given precision.  When such
operations are performed many times in sequence, these small rounding errors
can accumulate, and can grow into the dominant error.

## Double Precision

Consider this code:

```
import numpy as np

# -----------------------------
# Parameters
# -----------------------------
N = 10_000_000       # number of additions
x0 = 1.0             # starting value
dx = 1e-3            # increment

# -----------------------------
# FP64
# -----------------------------
x = np.float64(x0)
for _ in range(N):
    x += np.float64(dx)
error_fp64 = x - (x0 + N*dx)
print(f"FP64 final value: {x:.12f}, accumulated error: {error_fp64:.3e}")
```

This takes the number $x_0 = 1$, and adds $dx=10^{-3}$ to it 10 million times in double precision.

While $x_0=1$ is exact in binary ($1\times 2^0$), both $dx$ and the running sum $x$ will have a **representation error**.
This error accumulates as the loop is iterated, leading to the _accumulation error_.

Let us consider the $k$th iteration of the loop.
In that iteration, we have the $k$th partial sum, $x_k$ and the increment $dx$, both of which are only accurate up to their representation error.
That is, as stored in the computer, $x_k$ and $dx$ are really

$$
(1+\varepsilon_{64}) x_k 
~~~~ \mathrm{and}
~~~~
(1+\varepsilon_{64}) dx  
$$

containing an error proportional to their size.
The error in the increment is constant, and accumulates over every iteration to give a total error

$$
N\varepsilon_{64} dx
$$ 

which increases linearly with loop iterations $N$.

The error in the accumulated sum $x_k$ depends on the value of the sum itself, and is

$$
\sum_{k=1}^{N} \varepsilon_{64} x_k = 
\sum_{k=1}^{N} \varepsilon_{64} (x_0 + k\ dx) = 
\varepsilon_{64} \left(N x_0 + \frac{N(N+1)}{2}\ dx\right).
$$

This contains an $O(N^2)$ term which dominates for a large number of iterations $N$.
Note that for small $N$, the linear term $\varepsilon_{64}N x_0$ can dominate if $x_0\gg dx$.

Note also that while these errors are specific to a constant increment, they are representative of the behaviour of accumulation errors more generally. 
In any case, the representation error $\varepsilon$ is not really a constant, but rather an unknown term with that order of magnitude.
In more general algorithms, we would make estimates for order of magnitude of all terms.

### Results

Executing the code above, we obtain

```
FP64 final value: 10001.000001578721, accumulated error: 1.579e-06
```
instead of the exact result 10001.

Using the parameters $x_0=1$, $N=10,000,000$, $dx=0.001$ and $\varepsilon_{64}=1\times 10^{-16}$, the three error terms are approximately

$$
N\varepsilon_{64} dx = 10^8 . 10^{-16} . 10^{-3} &= 10^{-11},\\
N \varepsilon_{64} x_0 &= 10^{-8}\\
\varepsilon_{64} \frac{N(N+1)}{2} dx = 10^{-16} \frac{10^8}{2} 10^{-3} &= 5\times 10^{-4}. 
$$

This gives an overall estimate of $5\times10^{-4}$. 
While this value is a few orders-of-magnitude too large, it is roughly correct:
the above argument assumes that all errors accumulate, while in practice the error is not of fixed sign
and there would be some degree of cancellation.

## Single Precision

Now consider performing the same operation in single precision:

```
# -----------------------------
# FP32
# -----------------------------
x = np.float32(x0)
for _ in range(N):
    x += np.float32(dx)
error_fp32 = x - np.float64(x0 + N*dx)
print(f"FP32 final value: {x:.12f}, accumulated error: {error_fp32:.3e}")
```

The only thing that changes in the preceding argument is that the representation error is now in the 8th decimal place rather than the 16th.
The accumulation errors are

$$
N\varepsilon_{32} dx
~~~~
\mathrm{and}
~~~~
\varepsilon_{32} \left(N x_0 + \frac{N(N+1)}{2}\ dx\right)
$$ 

which are exactly the same, except that are $\varepsilon_{32}/\varepsilon_{64} = 6\times 10^8$ times larger.
This error is significant, and limits the usefulness of single precision in calculations.
This is why domain specialists will say that using double precision is necessary in their applications.

### Results

Executing the code in single precision, we obtain

```
FP32 final value: 9781.180664062500, accumulated error: -2.198e+02
```
instead of the exact result 10001.
Note that this is indeed $\sim10^8$ times larger than the accumulation error in the corresponding double precision calculation.
Note also that the sign of the error is negative, and the accumulation error can accumulate in either direction.

## Mixed Precision



