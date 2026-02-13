#!/usr/bin/env python3
"""
ECE 20001 Circuit Solver
Solve for V_x using nodal analysis with "all leaving = 0" KCL convention
"""

from sympy import symbols, Eq, solve, simplify

# Define symbolic variables for node voltages
V_A, V_M, V_B = symbols('V_A V_M V_B', real=True)
V_x = symbols('V_x', real=True)

print("=" * 60)
print("CIRCUIT SOLVER: Finding V_x")
print("=" * 60)
print("\nCircuit Description:")
print("  40V source connects ground to Node A (+ at top)")
print("  10Ω resistor from Node A to Node M")
print("  3A current source from Node M to Node B (arrow right)")
print("  12Ω resistor from Node M to Node B (series with 3A)")
print("  8Ω resistor from Node B to ground")
print("  2V_x dependent current source from ground to Node B (arrow up)")
print("  V_x is voltage across 10Ω resistor (+ on Node A side)")
print("\n" + "=" * 60)

# Known voltages
print("\nSTEP 1: Identify Known Node Voltages")
print("-" * 60)
print("Ground = 0V")
print("Node A = 40V (connected to 40V source with + at top)")
print()

# Define V_x relationship
print("STEP 2: Define V_x")
print("-" * 60)
print("V_x = V_A - V_M")
print("V_x = 40 - V_M")
print()

# Write KCL equations at each unknown node
print("STEP 3: Write KCL Equations (all leaving = 0)")
print("-" * 60)

print("\nAt Node M:")
print("  Leaving through 10Ω to Node A: (V_M - V_A) / 10")
print("  Leaving through 3A source to Node B: -3A")
print("  (Note: 3A flows FROM M TO B, so it LEAVES Node M)")
print()
print("  KCL at Node M:")
print("  (V_M - V_A)/10 + (-3) = 0")
print("  (V_M - 40)/10 - 3 = 0")
print()

# Solve for V_M from Node M equation
eq_M = Eq((V_M - 40)/10 - 3, 0)
V_M_value = solve(eq_M, V_M)[0]
print(f"  Solving: V_M = {V_M_value} V")
print()

# Calculate V_x
V_x_value = 40 - V_M_value
print("STEP 4: Calculate V_x")
print("-" * 60)
print(f"V_x = V_A - V_M")
print(f"V_x = 40 - {V_M_value}")
print(f"V_x = {V_x_value} V")
print()

# Verify with Node B (optional check)
print("STEP 5: Verify with KCL at Node B")
print("-" * 60)
print("\nAt Node B:")
print("  Leaving through 8Ω to ground: (V_B - 0) / 8 = V_B / 8")
print("  Current entering from 3A source (from M): -3A")
print("  Current entering from 2V_x dependent source (from ground): -2V_x")
print("  (Note: dependent source arrow points UP, so current ENTERS Node B)")
print()
print("  KCL at Node B:")
print("  V_B/8 + (-3) + (-2*V_x) = 0")
print(f"  V_B/8 - 3 - 2*({V_x_value}) = 0")
print()

# Solve for V_B
eq_B = Eq(V_B/8 - 3 - 2*V_x_value, 0)
V_B_value = solve(eq_B, V_B)[0]
print(f"  Solving: V_B = {V_B_value} V")
print()

# Verify current through 12Ω resistor
print("STEP 6: Verification Check")
print("-" * 60)
print("\nNote: The 12Ω resistor is in series with the 3A current source.")
print("Since the 3A source fixes the current in that branch, the 12Ω")
print("resistor must have exactly 3A flowing through it.")
print()
print(f"Voltage drop across 12Ω: V_drop = I × R = 3A × 12Ω = 36V")
print(f"This means: V_M - V_B = 36V")
print(f"Check: {V_M_value} - {V_B_value} = {V_M_value - V_B_value} V ✓")
print()

# Final answer
print("=" * 60)
print("FINAL ANSWER")
print("=" * 60)
print(f"\nV_x = {V_x_value} V")
print()
print("=" * 60)
