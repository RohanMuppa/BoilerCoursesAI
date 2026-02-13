# Interactive HTML Template for ECE 270 Concepts

## Core Pattern

Every interactive explanation follows the same three part structure.

**1. State** (what the user controls)
**2. Logic** (what the circuit does)
**3. Visuals** (what lights up)

## Template Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Concept Name</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  background: #0a0a0a;
  color: #e0e0e0;
  font-family: 'Courier New', monospace;
  padding: 20px;
}
h1 { text-align: center; margin-bottom: 10px; color: #fff; }
.subtitle { text-align: center; margin-bottom: 30px; color: #888; font-size: 14px; }

/* Controls */
.controls {
  display: flex;
  gap: 20px;
  justify-content: center;
  margin-bottom: 40px;
  flex-wrap: wrap;
}
.btn {
  width: 50px;
  height: 50px;
  background: #1a1a2e;
  border: 3px solid #555;
  color: #888;
  font-family: 'Courier New', monospace;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.2s;
}
.btn.on {
  background: #00ff88;
  color: #000;
  border-color: #00ff88;
  box-shadow: 0 0 20px rgba(0,255,136,0.5);
}

/* Circuit elements */
.wire {
  stroke: #333;
  stroke-width: 2;
  fill: none;
  transition: stroke 0.3s;
}
.wire.active {
  stroke: #00ff88;
  stroke-width: 3;
  filter: drop-shadow(0 0 4px #00ff88);
}
.gate {
  fill: #1a1a2e;
  stroke: #4a9eff;
  stroke-width: 2;
  transition: fill 0.3s;
}
.gate.active {
  fill: #2a4a6e;
}
.gate-label {
  fill: #4a9eff;
  font-size: 12px;
  font-weight: bold;
  text-anchor: middle;
}
.io-label {
  font-size: 13px;
  font-weight: bold;
  fill: #888;
  transition: fill 0.3s;
}
.io-label.active { fill: #00ff88; }
.led {
  fill: #2a2a2a;
  stroke: #555;
  stroke-width: 2;
  transition: fill 0.3s;
}
.led.on {
  fill: #ff9f43;
  filter: drop-shadow(0 0 8px #ff9f43);
}
</style>
</head>
<body>

<h1>Concept Title</h1>
<p class="subtitle">Click to interact and watch signals propagate</p>

<div class="controls">
  <button class="btn" id="input1">A</button>
  <button class="btn" id="input2">B</button>
</div>

<svg width="800" height="400" viewBox="0 0 800 400">
  <!-- Input wires -->
  <line x1="50" y1="100" x2="150" y2="100" class="wire" id="wire-input1"/>

  <!-- Gate -->
  <rect x="150" y="80" width="80" height="60" rx="8" class="gate" id="gate1"/>
  <text x="190" y="115" class="gate-label">GATE</text>

  <!-- Output wire -->
  <line x1="230" y1="110" x2="330" y2="110" class="wire" id="wire-output"/>

  <!-- LED -->
  <circle cx="350" cy="110" r="12" class="led" id="led-output"/>
  <text x="380" y="115" class="io-label" id="lbl-output">OUT</text>
</svg>

<script>
// 1. STATE (what the user controls)
const state = {
  input1: 0,
  input2: 0
};

// 2. LOGIC (what the circuit does)
function compute() {
  const { input1, input2 } = state;

  // Calculate intermediate signals
  const gate1_out = input1 & input2;  // AND logic example

  // Calculate final outputs
  const output = gate1_out;

  // Update LED displays
  document.getElementById('led-output').classList.toggle('on', output);

  // Update wire/gate highlighting
  updateVisuals({ input1, input2, gate1_out, output });
}

// 3. VISUALS (what lights up)
function updateVisuals(signals) {
  // Clear all highlights
  document.querySelectorAll('.wire, .gate, .io-label').forEach(el => {
    el.classList.remove('active');
  });

  // Highlight active paths
  if (signals.input1) {
    activate('wire-input1', 'lbl-input1');
  }

  if (signals.input1 || signals.input2) {
    activate('gate1');
  }

  if (signals.output) {
    activate('wire-output', 'lbl-output');
  }
}

function activate(...ids) {
  ids.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.classList.add('active');
  });
}

// Wire up button clicks
['input1', 'input2'].forEach(id => {
  const btn = document.getElementById(id);
  btn.addEventListener('click', () => {
    state[id] = state[id] ? 0 : 1;
    btn.classList.toggle('on', state[id]);
    compute();
  });
});

// Initial render
compute();
</script>

</body>
</html>
```

## Key Requirements

**Every wire and gate needs a unique ID**
```html
<line x1="50" y1="100" x2="150" y2="100" class="wire" id="w-a-to-gate1"/>
<rect x="150" y="80" width="80" height="60" class="gate" id="g-and1"/>
```

**Track all intermediate signals, not just final outputs**
```javascript
const xor_out = xor(a, b);
const and_out = and(a, b);
const final = or(xor_out, and_out);
```

**Highlight shows active signal flow, not just high signals**
Some concepts need to show "this gate is processing" even if output is 0.

**Use actual gate logic functions**
```javascript
function and(a, b) { return a & b; }
function or(a, b) { return a | b; }
function xor(a, b) { return a ^ b; }
function not(a) { return a ? 0 : 1; }
function nand(a, b) { return (a & b) ? 0 : 1; }
function nor(a, b) { return (a | b) ? 0 : 1; }
```

## Works Great For

### Combinational Logic
NAND/NOR gates, XOR chains, multiplexers, decoders, adders. Click inputs, watch signals propagate through gates, see outputs light up.

### CMOS Circuits
Show PMOS pullup network and NMOS pulldown network. Highlight conducting transistors based on inputs. Show VDD to output path or output to GND path.

### Karnaugh Maps
Grid of clickable cells. Each cell corresponds to a minterm. Highlight grouped terms in different colors. Show simplified SOP expression update live.

### Sequential Circuits
Flip flops with clock input. Show current state, next state logic, and state transitions. Animate clock edge triggering state change.

### Timing Diagrams
Horizontal timeline with signal traces. Scrub through time, circuit state updates. Show setup time, hold time, propagation delay visually.

### Boolean Algebra
Expression tree visualization. Toggle inputs, intermediate nodes light up showing true/false. Final output updates. Show equivalent expressions side by side.

## Color Scheme

```css
Background: #0a0a0a (black)
Text: #e0e0e0 (light gray)
Inputs: #00ff88 (bright green when active)
Outputs: #ff9f43 (orange)
Gates: #4a9eff (blue outline)
Wires inactive: #333 (dark gray)
Wires active: #00ff88 (bright green with glow)
LEDs off: #2a2a2a (dark)
LEDs on: #ff9f43 (orange with glow)
```

## Example Adaptations

### CMOS Inverter
State: input A
Logic: pmos_on = !A, nmos_on = A, output = pmos_on ? 1 : 0
Visuals: highlight conducting path from VDD or to GND

### D Flip Flop
State: D input, CLK edge
Logic: on rising CLK, Q = D
Visuals: show data path gating, highlight active latch

### 4 to 1 Mux
State: 4 data inputs, 2 select inputs
Logic: output = data[select]
Visuals: highlight selected input path to output

### Full Adder (already done)
State: A, B, Cin
Logic: sum = A XOR B XOR Cin, cout = majority(A, B, Cin)
Visuals: show XOR and NAND gate activation, carry propagation

## Tips

Keep SVG coordinates simple. Use a grid mentally. Space gates 100 to 150 units apart horizontally.

Use rounded rectangles for gates (rx="8"). Looks cleaner than sharp corners.

Add glow effects with CSS filter drop-shadow for active elements. Makes signal flow obvious.

Transition timing of 0.3s feels responsive without being jarring.

Group related wires in comments. Easier to find and modify later.

Use meaningful IDs. `w-a-xor1` beats `wire37`.

Test with all input combinations. Make sure highlighting logic is correct.

Add a result display at top showing current calculation in human terms. "2 + 3 = 5" for adder, "A AND B = 1" for gates.

## When To Use This

User asks "how does X work" for any visual digital logic concept.

Creating study materials before an exam on combinational or sequential circuits.

Explaining a complex lab circuit before building it physically.

Debugging breadboard circuits by comparing expected vs actual signal flow.

Answering "why does the output do that when inputs change" questions.

## When NOT To Use This

Pure text explanations (definitions, theory, proofs). Just write markdown.

Math heavy derivations (Boolean algebra simplification steps). Use LaTeX in markdown.

Datasheets or reference tables. Plain HTML table or markdown table is fine.

Code examples (Verilog). Use syntax highlighted code blocks.

Anything that's not inherently visual or interactive.
