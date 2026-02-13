import sympy as sp

print("="*60)
print("THREE MESH ANALYSIS")
print("="*60)

print("\nMaybe there are 3 meshes in the circuit")
print("Testing different current combinations through 6 ohm resistor")
print("")

I1, I2, I3 = sp.symbols('I1 I2 I3', real=True)

# From the answers, we need specific I_6ohm values
target_I_6ohm_values = [
    6.5,    # for P = 253.5 W
    1.0,    # for P = 6 W
    4.5,    # for P = 121.5 W
    2.75,   # for P = 45.375 W
]

print("Target currents through 6 ohm resistor:")
for P in [253.5, 6, 121.5, 45.375]:
    I_6 = (P / 6) ** 0.5
    print(f"P = {P} W => I_6ohm = {I_6} A")

print("\n" + "="*60)
print("SCENARIO: Current through 6 ohm = I2 + I3 (two mesh currents)")
print("="*60)

# If 6 ohm has I2 + I3 flowing through it
# For P = 253.5: I2 + I3 = 6.5
# If Io = I1, and some constraint exists

# Let's say:
# I1 = 2.75, I2 + I3 = 6.5
# Constraint: I2 - I1 = 3*I1 => I2 = 4*I1 = 11
# Then I3 = 6.5 - 11 = -4.5

print("\nTest: Io = I1 = 2.75, I2 = 4*I1 = 11, I3 = 6.5 - I2 = -4.5")
print("This gives I_6ohm = I2 + I3 = 6.5")
print("But these values seem arbitrary without KVL validation")

print("\n" + "="*60)
print("SCENARIO: Current through 6 ohm = I2 - I3")
print("="*60)

# If 6 ohm has I2 - I3
# For P = 253.5: I2 - I3 = 6.5 or -6.5

# If Io = I1 = 2.75, and I2 = 4*I1 = 11
# Then I3 = I2 - 6.5 = 4.5 or I3 = I2 + 6.5 = 17.5

print("\nTest: Io = I1 = 2.75, I2 = 4*I1 = 11")
print("If I_6ohm = I2 - I3 = 6.5, then I3 = 4.5")
print("If I_6ohm = I2 - I3 = -6.5, then I3 = 17.5")

print("\n" + "="*60)
print("NEW APPROACH: What if there's only ONE mesh?")
print("="*60)

# Single mesh with all resistors in series
# Total resistance = 12 + 24 + 3 + 6 = 45 ohm
# Voltage = 36 V
# Current I = 36/45 = 0.8 A
# Power in 6 ohm = 0.8^2 * 6 = 3.84 W

I_single = 36 / 45
P_single = I_single**2 * 6
print(f"Single mesh: I = {I_single} A, P = {P_single} W")
print("Doesn't match")

print("\n" + "="*60)
print("RETHINKING: Maybe resistor values are wrong")
print("="*60)

# What if the 6 ohm is actually different?
# For P = 253.5 and I = 2.75: R = P/I^2 = 253.5/2.75^2 = 33.5 ohm

print("\nIf Io = 2.75 A flows through resistor with P = 253.5 W:")
R_calc = 253.5 / (2.75**2)
print(f"R = P/I^2 = {R_calc} ohm")

print("\nIf Io = 1 A flows through resistor with P = 253.5 W:")
R_calc2 = 253.5 / (1**2)
print(f"R = P/I^2 = {R_calc2} ohm")

print("\n" + "="*60)
print("HYPOTHESIS: The 6 ohm is correct, but Io does NOT flow through it")
print("="*60)

# Maybe Io is a branch current and I_6ohm is a different mesh current
# For instance:
# Io = 2.75 A (some branch)
# I_6ohm = 6.5 A (mesh current through 6 ohm)
# P = 6.5^2 * 6 = 253.5 W

# From standard mesh: I1 = 1.4118, I2 = 2.1176
# These don't equal 2.75 or 6.5

# What if we use supermesh or modified nodal analysis?

print("\nStandard mesh (no constraint) gives:")
print("I1 = 1.4118 A, I2 = 2.1176 A")
print("Neither matches our target values")

print("\nMaybe the circuit needs to be re-examined with")
print("different component connections")

print("\n" + "="*60)
print("TRYING: What if answer 5 or 6 is correct?")
print("Io = 5.5 or -1, P = 45.375")
print("="*60)

# For P = 45.375: I_6ohm = 2.75 A
# If Io = 5.5 and I_6ohm = 2.75
# Relationship: I_6ohm = Io/2

print("\nIf I_6ohm = Io/2:")
print("Io = 5.5 => I_6ohm = 2.75, P = 2.75^2 * 6 = 45.375")
print("This matches answer 5")

print("\nIf I_6ohm = -Io/2 (with absolute value for power):")
print("Io = -1 => I_6ohm = 0.5, P = 0.25 * 6 = 1.5")
print("Doesn't work")

print("\nIf I_6ohm = |Io| * 2.75:")
print("Io = -1 => I_6ohm = 2.75, P = 45.375")
print("This matches answer 6")

print("\n" + "="*60)
print("TESTING: I_6ohm = |Io/2| for all answers")
print("="*60)

answers = [
    (2.75, 253.5),
    (1, 253.5),
    (2.75, 6),
    (-2.75, 121.5),
    (5.5, 45.375),
    (-1, 45.375),
    (1, 6)
]

for i, (io, p_expected) in enumerate(answers, 1):
    I_6_calc = abs(io / 2)
    P_calc = I_6_calc**2 * 6
    match = "MATCH" if abs(P_calc - p_expected) < 0.1 else "no match"
    print(f"{i}. Io = {io}, I_6ohm = {I_6_calc}, P_calc = {P_calc}, P_expected = {p_expected} - {match}")

print("\n" + "="*60)
print("FOUND PATTERN: I_6ohm = |Io/2| works for answer 5")
print("Let me find the mesh equations that give this")
print("="*60)

# If Io = 5.5 and I_6ohm = 2.75 = I2
# And if Io = I1, then I1 = 5.5, I2 = 2.75
# Relationship: I2 = I1/2

# Check mesh equations with this:
# Mesh 1: 36*I1 - 24*I2 = 36*5.5 - 24*2.75 = 198 - 66 = 132 (not 0)
# Mesh 2: -24*I1 + 33*I2 = -24*5.5 + 33*2.75 = -132 + 90.75 = -41.25 (not 36)

# These don't satisfy standard mesh equations
# The circuit must be different

print("="*60)
