"""
Mesh Analysis Problem Solver
Circuit with dependent current source requiring supermesh technique

Circuit Topology (5 nodes: A, B, C, D, E):
- 12Ω connects A to B (Io flows downward from B to A)
- 3Ω connects B to C (horizontal, top)
- 24Ω connects A to D (horizontal)
- 6Ω connects D to C (horizontal)
- 3Io dependent current source connects E to D (arrow pointing UP, from E toward D)
- 36V voltage source connects E to C (+ at C, - at E)

Find: Io and power absorbed by 6Ω resistor
"""

import sympy as sp

# Define symbolic variables
I1, I2, Io = sp.symbols('I1 I2 Io', real=True)

print("="*70)
print("MESH ANALYSIS WITH DEPENDENT CURRENT SOURCE (SUPERMESH)")
print("="*70)

# Circuit component values
R12 = 12  # Ohms, A to B
R3_top = 3  # Ohms, B to C
R24 = 24  # Ohms, A to D
R6 = 6  # Ohms, D to C
V36 = 36  # Volts, E to C (+ at C, - at E)

print("\nCircuit Components:")
print(f"R(A to B) = {R12} Ohms")
print(f"R(B to C) = {R3_top} Ohms")
print(f"R(A to D) = {R24} Ohms")
print(f"R(D to C) = {R6} Ohms")
print(f"Voltage source = {V36}V (+ at C, - at E)")
print(f"Dependent current source = 3*Io (arrow points UP from E to D)")

print("\n" + "="*70)
print("STEP 1: DEFINE MESH CURRENTS (CLOCKWISE)")
print("="*70)
print("\nMesh 1 (I1): A -> B -> C -> D -> A (clockwise)")
print("Mesh 2 (I2): E -> D -> C -> E (clockwise)")
print("\nNote: The dependent current source 3*Io is shared between meshes")
print("This requires SUPERMESH analysis")

print("\n" + "="*70)
print("STEP 2: IDENTIFY Io")
print("="*70)
print("\nIo flows downward from B to A through the 12 Ohm resistor")
print("In Mesh 1, I1 flows clockwise: A -> B")
print("Therefore: Io = I1 (same direction)")

# Define Io in terms of mesh currents
eq_Io = sp.Eq(Io, I1)
print(f"\nEquation: {eq_Io}")

print("\n" + "="*70)
print("STEP 3: CURRENT SOURCE CONSTRAINT")
print("="*70)
print("\nThe dependent current source 3*Io has arrow pointing UP (E to D)")
print("Current flows from E toward D")
print("\nAnalyzing mesh currents through the current source:")
print("  - Mesh 2 (I2) flows clockwise: E -> D (upward, same as source)")
print("  - Mesh 1 (I1) flows clockwise: D -> E (downward, opposite to source)")
print("\nThe current through the source (upward) = I2 - I1")
print("This must equal 3*Io = 3*I1")
print("\nConstraint equation: I2 - I1 = 3*I1")

# Current source constraint equation
eq_constraint = sp.Eq(I2 - I1, 3*I1)
print(f"\nEquation: {eq_constraint}")
print(f"Simplified: I2 = 4*I1")

print("\n" + "="*70)
print("STEP 4: KVL FOR SUPERMESH")
print("="*70)
print("\nSupermesh: Combine Mesh 1 and Mesh 2, excluding the current source")
print("Path: A -> B -> C -> E -> D -> A")
print("\nGoing clockwise around the supermesh:")
print("  1. A to B: +12*I1 (I1 flows this direction)")
print("  2. B to C: +3*I1 (I1 flows this direction)")
print("  3. C to E: -36V (going from + to -, voltage drop is negative)")
print("  4. E to D: 0V (current source, no voltage in KVL)")
print("  5. D to A: -24*I1 (I1 flows opposite direction, A to D)")
print("\nNote: At node C, current splits:")
print("  - From B to C: I1 flows in")
print("  - From C to D: (I1 - I2) flows out through 6 Ohm resistor")
print("Wait, let me reconsider the path...")

print("\nActually, for supermesh, I need to go around BOTH meshes:")
print("Starting at A, going through Mesh 1 path and Mesh 2 path")
print("\nLet me use the outer perimeter of the supermesh:")
print("A -> B -> C -> E -> D -> A")
print("\nBut we also need to include internal resistor (6 Ohm from D to C)")

print("\nAlternative approach: Write KVL for the supermesh carefully")
print("The supermesh includes:")
print("  - All components in Mesh 1 EXCEPT the shared current source")
print("  - All components in Mesh 2 EXCEPT the shared current source")

print("\nLet me trace the supermesh boundary:")
print("A -> B -> C (through mesh 1 components)")
print("C -> E (through voltage source, shared)")
print("E -> D is the current source (excluded)")
print("D -> A (through 24 Ohm)")

print("\nActually, I need to carefully consider which components are where:")
print("\nFrom circuit topology:")
print("  - 12Ω: A-B")
print("  - 3Ω: B-C")
print("  - 24Ω: A-D")
print("  - 6Ω: D-C")
print("  - 3Io source: E-D")
print("  - 36V source: E-C")

print("\nMesh 1 path (A -> B -> C -> D -> A):")
print("  A -> B: 12Ω")
print("  B -> C: 3Ω")
print("  C -> D: 6Ω")
print("  D -> A: 24Ω")

print("\nMesh 2 path (E -> D -> C -> E):")
print("  E -> D: 3Io source")
print("  D -> C: 6Ω (shared with Mesh 1)")
print("  C -> E: 36V source")

print("\nFor supermesh KVL, go around outer boundary:")
print("A -> B -> C -> E -> D -> A (skipping the current source E-D)")

print("\nKVL equation:")
print("  +12*I1 (A to B, I1 direction)")
print("  +3*I1 (B to C, I1 direction)")
print("  -36 (C to E, going from + to -)")
print("  +0 (E to D is current source, skip)")
print("  -24*I1 (D to A, opposite to I1)")
print("  = 0")

# KVL for supermesh
# Outer path: A -> B -> C -> E -> (skip current source) -> D -> A
# But wait, we need to account for the 6 Ohm resistor properly

print("\n" + "-"*70)
print("Let me reconsider the complete circuit layout:")
print("-"*70)

print("\nNodes: A, B, C, D, E")
print("Mesh 1: A -> B -> C -> D -> A")
print("  - Current I1 flows through: 12Ω (A-B), 3Ω (B-C), 6Ω (C-D), 24Ω (D-A)")

print("\nMesh 2: E -> D -> C -> E")
print("  - Current I2 flows through: 3Io source (E-D), 6Ω (D-C), 36V (C-E)")

print("\nNote: 6Ω resistor (D-C) is shared between meshes")
print("  - I1 flows from C to D")
print("  - I2 flows from D to C")
print("  - Net current in 6Ω = I1 - I2 (from C to D)")

print("\nSupermesh KVL (combining both meshes, excluding current source):")
print("Path: A -> B -> C -> E -> (back to A through D)")
print("\nGoing clockwise:")
print("  A to B: +12*I1")
print("  B to C: +3*I1")
print("  C to E: -36V (+ at C, going to - at E)")
print("  E to D: SKIP (current source)")
print("  D to A: -24*I1")
print("\nBut I'm missing the 6 Ohm resistor. Let me think again...")

print("\n" + "-"*70)
print("Correct approach for supermesh:")
print("-"*70)

print("\nWrite separate KVL for Mesh 1 and Mesh 2, then combine")
print("\nMesh 1 KVL (A -> B -> C -> D -> A):")
print("  +12*I1 + 3*I1 + 6*(I1-I2) + 24*I1 = 0")
print("  where 6*(I1-I2) is voltage across 6Ω with current (I1-I2)")

print("\nMesh 2 KVL (E -> D -> C -> E):")
print("  V_source + 6*(I2-I1) - 36 = 0")
print("  where V_source is voltage across current source (unknown)")
print("\nBut we eliminate V_source using supermesh")

print("\nSupermesh: Add Mesh 1 and Mesh 2 KVL equations")
print("This eliminates the current source voltage")

print("\nMesh 1: 12*I1 + 3*I1 + 6*(I1-I2) + 24*I1 = 0")
print("Mesh 2: 6*(I2-I1) - 36 = 0")
print("\nAdding them:")
print("12*I1 + 3*I1 + 6*(I1-I2) + 24*I1 + 6*(I2-I1) - 36 = 0")
print("12*I1 + 3*I1 + 24*I1 - 36 = 0")
print("39*I1 - 36 = 0")

# Corrected KVL for supermesh
eq_kvl = sp.Eq(12*I1 + 3*I1 + 24*I1 - 36, 0)
print(f"\nSupermesh KVL equation: {eq_kvl}")

print("\n" + "="*70)
print("STEP 5: SOLVE THE SYSTEM")
print("="*70)

# System of equations
print("\nSystem of equations:")
print(f"1. Current source constraint: {eq_constraint}")
print(f"2. Supermesh KVL: {eq_kvl}")

# Solve for I1 and I2
solution = sp.solve([eq_constraint, eq_kvl], [I1, I2])
print(f"\nSolution:")
print(f"I1 = {solution[I1]} A")
print(f"I2 = {solution[I2]} A")

# Calculate Io
Io_value = solution[I1]
print(f"\nIo = I1 = {Io_value} A")

print("\n" + "="*70)
print("STEP 6: CALCULATE POWER IN 6Ω RESISTOR")
print("="*70)

# Current through 6 Ohm resistor
I_6ohm = solution[I1] - solution[I2]
print(f"\nCurrent through 6Ω resistor = I1 - I2 = {I_6ohm} A")

# Power absorbed by 6 Ohm resistor
P_6ohm = R6 * I_6ohm**2
print(f"\nPower absorbed by 6Ω resistor:")
print(f"P = R * I^2 = {R6} * ({I_6ohm})^2")
print(f"P = {P_6ohm} W")

print("\n" + "="*70)
print("FINAL ANSWERS")
print("="*70)
print(f"\nIo = {Io_value} A")
print(f"Power absorbed by 6Ω resistor = {P_6ohm} W")
print("\n" + "="*70)

# Verification
print("\n" + "="*70)
print("VERIFICATION")
print("="*70)

print("\nChecking constraint equation:")
print(f"I2 - I1 = {solution[I2]} - {solution[I1]} = {solution[I2] - solution[I1]}")
print(f"3*Io = 3*{Io_value} = {3*Io_value}")
print(f"Constraint satisfied: {solution[I2] - solution[I1] == 3*Io_value}")

print("\nChecking supermesh KVL:")
kvl_check = 12*solution[I1] + 3*solution[I1] + 24*solution[I1] - 36
print(f"12*I1 + 3*I1 + 24*I1 - 36 = {kvl_check}")
print(f"KVL satisfied: {kvl_check == 0}")

print("\n" + "="*70)
