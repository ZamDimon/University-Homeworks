from scipy.special import binom
import numpy as np

n = 3
p = 1/6

def prob(k: int) -> float:
    return binom(4,3-k)*binom(4,k) / binom(8,3)

elems = [prob(j) for j in range(4)]
print("distribution:", elems)
print("sum of p =", np.sum(elems))
Ex = np.sum([prob(j)*j for j in range(4)])
print("E[X] =", Ex)
Exx = np.sum([prob(j)*(j**2) for j in range(4)])
print("E[X^2] =", Exx)
print("Var[X]=", Exx - Ex**2)
