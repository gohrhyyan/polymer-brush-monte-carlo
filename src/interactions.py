"""
1) $E_{spring}(ij) = {1\over2} \,k\, d_{ij}^2$, where $d_{ij}$ is the distance between particle $i$ and particle $j$ (or particle $1$ and the grafting point $r_0$ on the surface, in case of the first particle).

Furthermore, each particle interact with each other particle in the system (both those belonging to the same polymer or to other polymers) with the following energy function:

2) $E_{int}(ij) = C_{int} \cos( \pi / 2 \, d_{ij} / R )$ for $d_{ij} < R$, $0$ if $d_{ij} \le R$ 

Each particle also interact with the grafting surface via the following potential:

3) $E_{surf}(i) = 10^9 for $d_{i} \lt 0$ and $0$ if $d_{i} > 0$, where $d_i$ is the $z$ coordinate of the particle, and the surface is supposed to be the plane $z=0$

The total energy of the system is given by:

$E_{tot} = \sum_i E_{surf}(i) + \sum_i \sum_j \left(E_{int}(ij) + E_{spring}(ij)\right)$
"""