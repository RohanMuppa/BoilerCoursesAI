"""
Final Solution Summary with Numerical Values
"""

import sympy as sp

print("="*70)
print("MESH ANALYSIS SOLUTION SUMMARY")
print("="*70)

# Solution values (exact fractions)
I1 = sp.Rational(12, 13)
I2 = sp.Rational(48, 13)
Io = I1

print("\nMesh Currents:")
print(f"I1 = {I1} A = {float(I1):.6f} A")
print(f"I2 = {I2} A = {float(I2):.6f} A")

print("\nRequired Values:")
print(f"Io = {Io} A = {float(Io):.6f} A")

# Current through 6 Ohm resistor
I_6ohm = I1 - I2
print(f"\nCurrent through 6Ω resistor = {I_6ohm} A = {float(I_6ohm):.6f} A")

# Power in 6 Ohm resistor
R6 = 6
P_6ohm = R6 * I_6ohm**2
print(f"\nPower absorbed by 6Ω resistor:")
print(f"P = {P_6ohm} W = {float(P_6ohm):.6f} W")

# Convert to decimal for easier reading
print("\n" + "="*70)
print("FINAL ANSWERS (DECIMAL)")
print("="*70)
print(f"\nIo = {float(Io):.6f} A (or {Io} A)")
print(f"Power in 6Ω resistor = {float(P_6ohm):.6f} W (or {P_6ohm} W)")

print("\n" + "="*70)
print("KEY EQUATIONS USED")
print("="*70)
print("\n1. Current source constraint: I2 - I1 = 3*Io = 3*I1")
print("   Simplifies to: I2 = 4*I1")
print("\n2. Supermesh KVL: 39*I1 - 36 = 0")
print("   From: 12*I1 + 3*I1 + 24*I1 - 36 = 0")
print("\n3. Solving: I1 = 36/39 = 12/13 A")
print("   Therefore: I2 = 4*(12/13) = 48/13 A")
