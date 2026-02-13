# SystemVerilog for ECE 270 Exam 1

Everything below comes directly from the Spring 2023, Fall 2023, Spring 2024, and Fall 2024 practice exams.


## What is SystemVerilog?

SystemVerilog is a language that describes digital circuits in text form. Instead of drawing gates on paper, you type code that tells a computer what gates to use, how to wire them together, and what the circuit should do.

There are three ways to describe a circuit in SystemVerilog. Structural modeling (gate level), dataflow modeling (assign statements), and behavioral modeling (always blocks). The exam tests all three.


## Modules

A module is a box with inputs and outputs. Every circuit you write in SystemVerilog lives inside a module. Think of it like a function in Python or Java, but instead of computing a value, it describes a piece of hardware.

```
module my_circuit (input wire A,
                   input wire B,
                   output wire Y);

    // circuit description goes here

endmodule
```

`input wire` means a signal coming IN to the module. `output wire` means a signal going OUT. The names A, B, Y are whatever you want to call them. These are the module's PORTS, which are the connection points to the outside world.

You can also use `logic` instead of `wire`. In ECE 270 you'll see both.

```
module my_circuit (input logic A,
                   input logic B,
                   output logic Y);
```


## Structural Modeling (Gate Level)

This is where you literally place gates and wire them together, like building a circuit on a breadboard.

### Primitive Gates

SystemVerilog has built in gates you can use directly. `and`, `or`, `nand`, `nor`, `xor`, `xnor`, `not`, `buf`.

The syntax is:

```
gate_type instance_name (OUTPUT, input1, input2);
```

THE OUTPUT IS ALWAYS THE FIRST ARGUMENT. This is the single most tested fact on every exam. Everything after the first argument is an input.

Examples:

```
and  a0 (Y, A, B);      // Y = A AND B
or   o0 (Y, A, B);      // Y = A OR B
nand n0 (Y, A, B);      // Y = (A AND B)'
nor  r0 (Y, A, B);      // Y = (A OR B)'
xor  x0 (Y, A, B);      // Y = A XOR B
not  i0 (Y, A);         // Y = NOT A (only one input)
buf  b0 (Y, A);         // Y = A (buffer, only one input)
```

You can have more than 2 inputs:

```
and a0 (Y, A, B, C);    // Y = A AND B AND C (3 inputs)
nand n0 (Y, A, B, C);   // Y = (A AND B AND C)'
```

The instance name (a0, o0, n0, etc.) is just a label. You pick any name you want. It's like naming a variable.

### Exam example (Spring 2023 Q19)

```
nand u0 ( a, b, c );
```

What does this mean? Since output is FIRST, `a` is the output. `b` and `c` are inputs. This is a NAND gate with b,c as inputs and a as output. Answer D.

### Exam example (Fall 2023 Q19)

```
nor n0 ( a, b, c);
```

Same idea. `a` is output, `b` and `c` are inputs. NOR gate with b,c as inputs, a as output. Answer D.

### Wires (Internal Signals)

When you connect one gate's output to another gate's input, you need a wire to carry that signal. Wires are declared with `wire` or `logic`.

### Exam example (Spring 2024 Q12)

Given a circuit where an OR gate takes A,B and produces signal M. A NOT gate takes C and produces signal N. An AND gate takes M,N and produces output Y.

```
wire M;
wire N;
or  or_0 (M, A, B);     // M = A OR B
not not_0(N, C);         // N = NOT C
and and_0(Y, M, N);     // Y = M AND N = (A+B) * C'
```

M and N are internal signals. They don't leave the module, they just connect gates to each other. You MUST declare them as wires before using them.


## Module Instantiation

Once you've built a module, you can use it inside another module. This is like calling a function. There are two ways to do this.

### Named Port Mapping (the exam's favorite)

```
module_name instance_name (.module_port(your_signal), .module_port(your_signal));
```

The DOT goes before the MODULE's port name. The PARENTHESES hold YOUR external signal. Think of it as saying "connect the module's port called X to my signal called Y."

### Exam example (Spring 2024 Q20)

You have a half_adder module defined as:

```
module half_adder (input logic A,
                   input logic B,
                   output logic S,
                   output logic C);
```

The module has 4 ports called A, B, S, C. Now you want to use it inside a full_adder where your signals are named X, Y, w0, c0.

```
half_adder h1 (.A(X), .B(Y), .S(w0), .C(c0));
```

Reading this out loud: "Create a half_adder called h1. Connect its A port to my signal X. Connect its B port to my signal Y. Connect its S port to my signal w0. Connect its C port to my signal c0."

The order doesn't matter with named ports. You could write `.C(c0), .A(X), .B(Y), .S(w0)` and it would be identical.

### Exam example (Spring 2023 Q20)

Module ha_270 has ports (input wire x, input wire y, output wire c, output wire s). You want to connect external signals s0, cin, c1, sum to it.

From the schematic: s0 goes to x, cin goes to y, c1 comes from c, sum comes from s.

```
ha_270 inst1 (.x(s0), .y(cin), .c(c1), .s(sum));
```

### Common Trap

Option A on Spring 2024 Q20 wrote `.X(A)` instead of `.A(X)`. This is WRONG because the dot must go on the MODULE's port name. The module's port is called A, so it must be `.A(something)`. This trap appears on multiple exams.

### Positional Port Mapping

```
module_name instance_name (signal1, signal2, signal3, signal4);
```

No dots, no port names. The signals are matched to ports purely by ORDER. The first signal connects to the first port in the module declaration, second to second, etc.

If the module is `module ha_270 (input wire x, input wire y, output wire c, output wire s)` then:

```
ha_270 inst1 (s0, cin, c1, sum);
```

This connects s0 to x, cin to y, c1 to c, sum to s. If you get the order wrong, the circuit is wrong. Named mapping is safer because order doesn't matter.


## Dataflow Modeling (assign statements)

Instead of placing individual gates, you write a single equation for the output.

```
assign output_signal = expression;
```

The operators:

```
&    AND
|    OR
^    XOR
~    NOT (bitwise, goes before the signal)
~&   NAND
~|   NOR
~^   XNOR (also ^~)
```

### Exam example (Spring 2024 Q19)

XOR gate with inputs a, b and output "out":

```
assign out = a ^ b;
```

That's it. One line replaces an entire gate instantiation.

### Exam example (Fall 2024 Q9)

A circuit shows A,B into an AND gate, then that result and C into a NAND. The dataflow options included things like:

```
A. assign OUT = ((A & B) == C) ? 0 : 1;
B. assign OUT = (A and B) xnor C;
C. assign OUT = ~(A & B) ^ ~C;
D. assign OUT = (A & B & C) | (~(A & B) & ~C);
```

Option A uses the TERNARY OPERATOR. The `?` works like if/else in one line. `(condition) ? value_if_true : value_if_false`. This is valid SystemVerilog.

Option B uses the word `and` which is a gate name, not a dataflow operator. You cannot use `and` inside an assign statement. You must use `&`.

### Full adder in dataflow

This comes from Fall 2023 Q20. The structural version uses xor and and and or gates. The equivalent dataflow is:

```
assign sum = A ^ B ^ Cin;
assign Cout = (A & B) | (Cin & (A ^ B));
```

XOR gives the sum bit. The carry is generated when both inputs are 1 (A&B) OR when the carry in and the partial sum are both 1.


## Behavioral Modeling (always_comb)

This describes what the circuit DOES rather than how it's built. You write logic like a program with if/else statements.

```
always_comb begin
    if (condition)
        out = expression1;
    else
        out = expression2;
end
```

`always_comb` means "this block describes combinational logic." The simulator re-evaluates it whenever any input changes.

Use `=` (blocking assignment) inside always_comb. Do NOT use `<=` (that's for sequential logic in always_ff).

### Exam example (Fall 2024 Q10)

```
module unknown_logic (input logic A,
                      input logic B,
                      input logic C,
                      output logic out);

    always_comb
        if (A)
            out = B | C;
        else
            out = B & C;
endmodule
```

To find the Boolean function, think about what happens for each value of A:

When A=1, out = B|C = B+C.
When A=0, out = B&C = BC.

Combine these: out = A(B+C) + A'(BC) = AB + AC + A'BC.

You can verify with a truth table. Plug in all 8 combinations of A,B,C and check. The answer is C, out = AB + BC + AC.

The key insight is that if/else in hardware is a multiplexer. A selects which expression drives the output.


## The Full Adder (appears on 3 of 4 exams)

### Half Adder
Takes two 1 bit inputs, produces a sum and carry.

```
S = A ^ B        (XOR)
C = A & B        (AND)
```

### Full Adder from Two Half Adders
Takes three inputs (A, B, carry in), produces sum and carry out.

First half adder: XOR A and B to get partial sum (w0). AND A and B to get first carry (c0).
Second half adder: XOR w0 and Cin to get final Sum. AND w0 and Cin to get second carry (c1).
OR gate: Cout = c0 | c1.

In named port instantiation (Spring 2024 Q20, answer D):

```
half_adder h1(.A(X),  .B(Y),   .S(w0),  .C(c0));
half_adder h2(.A(w0), .B(Cin), .S(Sum), .C(c1));
or o0(Cout, c0, c1);
```


## Crib Sheet (just the essentials)

```
PRIMITIVES: gate inst(OUTPUT, in1, in2);   ← OUTPUT FIRST

DATAFLOW:   assign out = a & b;   (& | ^ ~ ~^ ~& ~|)

NAMED:      mod inst(.port(sig), .port(sig));  ← dot on MODULE port

POSITIONAL: mod inst(sig1, sig2, sig3);  ← must match declaration order

BEHAVIORAL: always_comb if(A) out=B|C; else out=B&C;  ← use = not <=

WIRES:      wire M; (declare internals before use)

HALF ADDER: S = A^B,  C = A&B
FULL ADDER: sum = A^B^Cin,  Cout = (A&B)|(Cin&(A^B))
```
