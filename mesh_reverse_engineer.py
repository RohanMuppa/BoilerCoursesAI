import sympy as sp

print("="*60)
print("REVERSE ENGINEERING FROM ANSWERS")
print("="*60)

# Given answers - let's work backwards
answers = [
    (2.75, 253.5),
    (1, 253.5),
    (2.75, 6),
    (-2.75, 121.5),
    (5.5, 45.375),
    (-1, 45.375),
    (1, 6)
]

print("\nFrom P = I^2 * R for 6 ohm resistor")
print("I = sqrt(P/6)")
print("")

for i, (io, p) in enumerate(answers, 1):
    I_6ohm = (p / 6) ** 0.5
    print(f"{i}. Io = {io} A, P = {p} W => I_6ohm = {I_6ohm:.4f} A")

print("\n" + "="*60)
print("Testing if different circuit topology matches")
print("="*60)

# What if the circuit has different structure?
# Let's try: I2 through 6 ohm = sqrt(253.5/6) = 6.5 A

target_I_6ohm = (253.5 / 6) ** 0.5
print(f"\nTarget current through 6 ohm = {target_I_6ohm} A")

I1, I2 = sp.symbols('I1 I2', real=True)

# If I2 = 6.5 A and Io = 2.75 or 1, what's the relationship?
# If Io = I1:
#   I1 = 2.75, I2 = 6.5
#   or I1 = 1, I2 = 6.5

# If Io = I1 and I2 - I1 = 3*I1, then I2 = 4*I1
# So I1 = I2/4 = 6.5/4 = 1.625 (doesn't match 2.75 or 1)

# If Io = I2 - I1 (branch current):
#   Io = 2.75, I2 = 6.5 => I1 = 3.75
#   Io = 1, I2 = 6.5 => I1 = 5.5

print("\n" + "="*60)
print("SCENARIO: Io = I2 - I1 = 2.75 A, I2 = 6.5 A")
print("="*60)

I1_val = 6.5 - 2.75
I2_val = 6.5
print(f"I1 = {I1_val} A, I2 = {I2_val} A")

# Check if I2 - I1 = 3*Io
# 6.5 - 3.75 = 2.75
# 3*Io = 3*2.75 = 8.25
# 2.75 != 8.25, so this constraint doesn't work

# What if: I1 - I2 = 3*Io where Io = I2 - I1 ?
# I1 - I2 = 3*(I2 - I1) = 3*I2 - 3*I1
# I1 - I2 = 3*I2 - 3*I1
# 4*I1 = 4*I2
# I1 = I2 (contradiction)

print("\n" + "="*60)
print("SCENARIO: Maybe constraint is I2 - I1 = 3*I1 but Io != I1")
print("="*60)

# If I2 - I1 = 3*I1, then I2 = 4*I1
# If I2 = 6.5, then I1 = 1.625
# But answers show Io = 2.75 or 1, not 1.625

# What if Io is related differently?
# Io = 2*I1? Then 2.75 = 2*1.375 (doesn't work)
# Io = I1 + 1? Then 2.75 = 1.75 + 1 (works!)

# But this seems arbitrary...

print("\n" + "="*60)
print("ALTERNATIVE: What if current through 6 ohm is NOT I2?")
print("="*60)

# What if I2 goes through 3 ohm and another path,
# and the 6 ohm has a different current?

# Try P = 6 W for 6 ohm
I_6ohm_alt = (6 / 6) ** 0.5
print(f"If P = 6 W, then I_6ohm = {I_6ohm_alt} A")

# Io = 2.75 A corresponds to P = 6 W or P = 253.5 W
# Io = 1 A corresponds to P = 6 W or P = 253.5 W

print("\n" + "="*60)
print("NEW APPROACH: Consider all mesh current combinations")
print("="*60)

# Let's test: What values of I1 and I2 with constraint I2 - I1 = 3*I1
# would give us the target answers?

print("\nIf I2 - I1 = 3*I1 (i.e., I2 = 4*I1):")
for io_target, p_target in answers:
    # Case 1: Io = I1
    I1_test = io_target
    I2_test = 4 * I1_test
    I_6_test = I2_test
    P_test = I_6_test ** 2 * 6

    if abs(P_test - p_target) < 0.1:
        print(f"  MATCH: Io=I1={I1_test} A gives I2={I2_test} A, P={P_test} W")

print("\nIf I2 - I1 = -3*I1 (i.e., I2 = -2*I1):")
for io_target, p_target in answers:
    I1_test = io_target
    I2_test = -2 * I1_test
    I_6_test = I2_test
    P_test = I_6_test ** 2 * 6

    if abs(P_test - p_target) < 0.1:
        print(f"  MATCH: Io=I1={I1_test} A gives I2={I2_test} A, P={P_test} W")

print("\nIf I2 = I1/4 (constraint I1 = 4*I2):")
for io_target, p_target in answers:
    I1_test = io_target
    I2_test = I1_test / 4
    I_6_test = I2_test
    P_test = I_6_test ** 2 * 6

    if abs(P_test - p_target) < 0.1:
        print(f"  MATCH: Io=I1={I1_test} A gives I2={I2_test} A, P={P_test} W")

print("\nTrying different relationship: I2 = -I1/2")
for io_target, p_target in answers:
    I1_test = io_target
    I2_test = -I1_test / 2
    I_6_test = I2_test
    P_test = I_6_test ** 2 * 6

    if abs(P_test - p_target) < 0.1:
        print(f"  MATCH: Io=I1={I1_test} A gives I2={I2_test} A, P={P_test} W")

print("="*60)
