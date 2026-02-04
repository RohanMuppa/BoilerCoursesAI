import sympy as sp

print("="*60)
print("EXHAUSTIVE MESH ANALYSIS - ALL EQUATION COMBINATIONS")
print("="*60)

I1, I2 = sp.symbols('I1 I2', real=True)

# All possible mesh equations
equations = {
    "eq1a": sp.Eq(36*I1 - 24*I2, 0),            # Mesh 1: 12*I1 + 24*(I1-I2) = 0
    "eq1b": sp.Eq(24*I1 - 36*I2, 0),            # Alternative sign
    "eq2a": sp.Eq(-24*I1 + 33*I2, 36),          # Mesh 2: 24*(I2-I1) + 3*I2 + 6*I2 - 36 = 0
    "eq2b": sp.Eq(24*I1 - 33*I2, -36),          # Same but rearranged
    "eq2c": sp.Eq(-24*I1 + 33*I2, -36),         # Opposite voltage polarity
    "eq2d": sp.Eq(24*I1 - 33*I2, 36),           # Both signs flipped
}

# All possible dependent source constraints
constraints = {
    "c1": ("I2 - I1 = 3*I1", sp.Eq(I2 - I1, 3*I1)),
    "c2": ("I1 - I2 = 3*I1", sp.Eq(I1 - I2, 3*I1)),
    "c3": ("I2 - I1 = 3*I2", sp.Eq(I2 - I1, 3*I2)),
    "c4": ("I1 - I2 = 3*I2", sp.Eq(I1 - I2, 3*I2)),
    "c5": ("I2 - I1 = 3*(I2-I1)", sp.Eq(I2 - I1, 3*(I2-I1))),
    "c6": ("I2 - I1 = 3*(I1-I2)", sp.Eq(I2 - I1, 3*(I1-I2))),
    "c7": ("I1 - I2 = -3*I1", sp.Eq(I1 - I2, -3*I1)),
    "c8": ("I2 - I1 = -3*I1", sp.Eq(I2 - I1, -3*I1)),
}

# Io definitions to test
io_defs = [
    ("Io = I1", lambda s: s[I1]),
    ("Io = I2", lambda s: s[I2]),
    ("Io = I1 - I2", lambda s: s[I1] - s[I2]),
    ("Io = I2 - I1", lambda s: s[I2] - s[I1]),
]

answers = [
    (2.75, 253.5),
    (1, 253.5),
    (2.75, 6),
    (-2.75, 121.5),
    (5.5, 45.375),
    (-1, 45.375),
    (1, 6)
]

print("Answer choices:")
for i, (io, p) in enumerate(answers, 1):
    print(f"{i}. Io = {io} A, P = {p} W")

print("\n" + "="*60)
print("SEARCHING ALL COMBINATIONS")
print("="*60)

match_count = 0

for eq1_name, eq1 in equations.items():
    for eq2_name, eq2 in equations.items():
        if eq1_name == eq2_name:
            continue

        for const_name, (const_desc, const_eq) in constraints.items():
            # Try solving with eq1 and constraint
            try:
                sol = sp.solve([eq1, const_eq], [I1, I2])
                if not sol or sol[I1] is sp.nan or sol[I2] is sp.nan:
                    continue

                # Test all Io definitions
                for io_desc, io_func in io_defs:
                    io_val = io_func(sol)
                    P_val = sol[I2]**2 * 6

                    for idx, (io_ans, p_ans) in enumerate(answers, 1):
                        if abs(float(io_val) - io_ans) < 0.01 and abs(float(P_val) - p_ans) < 0.01:
                            match_count += 1
                            print(f"\n*** MATCH {match_count} with answer {idx} ***")
                            print(f"Equations: {eq1_name} + {const_name}")
                            print(f"{eq1}")
                            print(f"{const_desc}")
                            print(f"Solution: I1 = {float(sol[I1]):.4f} A, I2 = {float(sol[I2]):.4f} A")
                            print(f"{io_desc}: {float(io_val):.4f} A")
                            print(f"P = {float(P_val):.4f} W")
            except:
                pass

            # Try solving with eq2 and constraint
            try:
                sol = sp.solve([eq2, const_eq], [I1, I2])
                if not sol or sol[I1] is sp.nan or sol[I2] is sp.nan:
                    continue

                # Test all Io definitions
                for io_desc, io_func in io_defs:
                    io_val = io_func(sol)
                    P_val = sol[I2]**2 * 6

                    for idx, (io_ans, p_ans) in enumerate(answers, 1):
                        if abs(float(io_val) - io_ans) < 0.01 and abs(float(P_val) - p_ans) < 0.01:
                            match_count += 1
                            print(f"\n*** MATCH {match_count} with answer {idx} ***")
                            print(f"Equations: {eq2_name} + {const_name}")
                            print(f"{eq2}")
                            print(f"{const_desc}")
                            print(f"Solution: I1 = {float(sol[I1]):.4f} A, I2 = {float(sol[I2]):.4f} A")
                            print(f"{io_desc}: {float(io_val):.4f} A")
                            print(f"P = {float(P_val):.4f} W")
            except:
                pass

if match_count == 0:
    print("\nNo matches found with these equation/constraint combinations")
    print("The circuit topology may be different than assumed")

print("\n" + "="*60)
