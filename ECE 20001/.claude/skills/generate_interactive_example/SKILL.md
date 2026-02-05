---
user_invocable: true
description: Generate interactive HTML circuit explanations
---

# Generate Interactive Explanation

Generate an interactive HTML explanation for an ECE 20001 circuit analysis problem with visual diagrams, collapsible steps, and verification.

## Required Information (3 Requirements)

Before generating, the user MUST provide ALL THREE of the following. If any are missing, ask for them before proceeding.

### 1. Problem Source
Source type and identifier for the problem.

Options.
Textbook with chapter and problem number (e.g. Chapter 4 Problem 23)
Homework with assignment and question (e.g. HW3 Q2)
Exam with exam number and problem (e.g. Exam 2 Problem 3)
Lecture with date or topic (e.g. Lecture 10/15 Example)
Practice problem description

### 2. Context Level
Choose the level of detail for the explanation.

**High Context**
Detailed explanations with extensive text at each step.
Queries the ECE 20001 context_db for relevant formulas and concepts.
Searches textbook for similar examples and methods.
Includes theory background and multiple verification methods.
Best for learning new concepts or exam preparation.

**Low Context**
Barebones construction with minimal text.
Shows equations and calculations only.
Single verification step.
No database or textbook queries.
Best for quick reference or when concept is already understood.

### 3. Model Selection
Choose the model to use for generation.

**Opus** for complex multi step problems requiring deep reasoning.
**Sonnet** for standard problems with moderate complexity.
**Haiku** for simple problems or when speed is priority.

## File Organization

Create a folder structure organized by analysis topic.

```
ECE 20001/
└── topic_name/
    └── explanation/
        └── descriptive_filename.html
```

## Naming Conventions

### Topic Folder Names
Use lowercase with underscores. Name should describe the analysis method or concept.

Examples.
mesh_analysis
nodal_analysis
thevenin_equivalent
norton_equivalent
superposition
source_transformation
kirchhoffs_laws
op_amp_circuits
rc_transients
rl_transients
ac_steady_state
phasors
power_analysis

### File Names
Use lowercase with underscores. Name should describe what the problem asks for.

Format. find_[variable]_[method].html or solve_[concept]_[identifier].html

Examples.
find_io_mesh_analysis.html
find_vth_thevenin.html
find_req_series_parallel.html
solve_rc_transient_ch7p15.html
find_power_superposition.html
find_vx_nodal_hw3q2.html

## Required Features

Each interactive explanation must include.

1. Visual Diagrams. SVG circuit diagrams with labeled components, voltage polarities, and current directions
2. Collapsible Steps. Click to expand or collapse solution steps for easier navigation
3. Clean Equations. Monospace font with proper formatting and highlighting for key results
4. Verification Section. Show KCL, KVL, power balance, or other verification methods
5. Final Answer Box. Prominently displayed with green background and explanation
6. Responsive Design. Works on different screen sizes
7. Problem Source. Display ECE 20001 and source at the top of the page

## HTML Structure Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Problem Title</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5; }
        .container { max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .source { color: #666; font-size: 14px; margin-bottom: 10px; }
        h1 { color: #2c3e50; margin-bottom: 25px; font-size: 28px; }
        h2 { color: #34495e; margin: 25px 0 15px; font-size: 20px; cursor: pointer; user-select: none; padding: 10px; background: #ecf0f1; border-radius: 4px; }
        h2:hover { background: #dfe6e9; }
        h2::before { content: '▼ '; font-size: 14px; display: inline-block; transition: transform 0.3s; }
        h2.collapsed::before { transform: rotate(-90deg); }
        .step { margin-bottom: 20px; padding: 15px; background: #f8f9fa; border-left: 4px solid #3498db; border-radius: 4px; }
        .step.hidden { display: none; }
        .equation { font-family: 'Courier New', monospace; background: #fff; padding: 12px; margin: 10px 0; border-radius: 4px; border: 1px solid #ddd; font-size: 16px; }
        .highlight { background: #fff3cd; padding: 2px 6px; border-radius: 3px; font-weight: bold; }
        .answer { background: #d4edda; border-left: 4px solid #28a745; padding: 20px; margin: 25px 0; border-radius: 4px; font-size: 18px; font-weight: bold; }
        .circuit { background: white; padding: 20px; border-radius: 8px; border: 2px solid #ddd; margin: 20px 0; }
        svg { max-width: 100%; height: auto; }
        .component { fill: none; stroke: #2c3e50; stroke-width: 2; }
        .wire { stroke: #34495e; stroke-width: 2; fill: none; }
        text { font-family: Arial; font-size: 14px; fill: #2c3e50; }
        .label { font-size: 16px; font-weight: bold; }
        ul { margin-left: 20px; line-height: 1.8; }
        li { margin: 8px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="source">ECE 20001 | Source Type | Problem ID</div>
        <h1>Find Variable Using Method</h1>
        <div class="circuit">
            <!-- SVG circuit diagram -->
        </div>
        <h2 onclick="toggleStep(1)">Step 1. Define Variables</h2>
        <div id="step1" class="step">
            <!-- Mesh currents, node voltages, etc. -->
        </div>
        <h2 onclick="toggleStep(2)">Step 2. Write Equations</h2>
        <div id="step2" class="step">
            <!-- KVL, KCL, Ohm's Law equations -->
        </div>
        <h2 onclick="toggleStep(3)">Step 3. Solve System</h2>
        <div id="step3" class="step">
            <!-- Algebraic solution -->
        </div>
        <h2 onclick="toggleStep(4)">Step 4. Calculate Result</h2>
        <div id="step4" class="step">
            <!-- Final calculation -->
        </div>
        <h2 onclick="toggleStep(5)">Step 5. Verify Solution</h2>
        <div id="step5" class="step">
            <!-- KCL, KVL, or power verification -->
        </div>
        <div class="answer">
            Variable = Value
            <div style="font-size: 14px; margin-top: 10px; font-weight: normal;">
                Explanation of result and direction if applicable
            </div>
        </div>
    </div>
    <script>
        function toggleStep(num) {
            const step = document.getElementById('step' + num);
            const header = step.previousElementSibling;
            step.classList.toggle('hidden');
            header.classList.toggle('collapsed');
        }
    </script>
</body>
</html>
```

## SVG Circuit Diagram Guidelines

Label all components with values (5Ω, 12V, 2A).
Use consistent stroke widths (2px for components and wires).
Color code mesh currents in red (#e74c3c).
Include arrows showing assumed current direction.
Show voltage polarity with + and symbols.
Use circles for sources, rectangles for resistors.
Make diagrams large enough to read (viewBox of at least 500x350).

## ECE 20001 Analysis Methods

Mesh Analysis. Define clockwise mesh currents, write KVL for each mesh, handle current sources with supermesh or constraint equations.

Nodal Analysis. Define node voltages with reference node at ground, write KCL at each node, handle voltage sources with supernode or constraint equations.

Thevenin and Norton. Find open circuit voltage and short circuit current, calculate equivalent resistance.

Superposition. Analyze each independent source separately, sum contributions.

## Usage

$ARGUMENTS contains the problem to solve.

If all 3 requirements are provided, proceed with generation.
If any requirement is missing, ask the user to specify.

Example with all requirements.
/generate_interactive_explanation Textbook Ch4 P23, high context, opus

Example prompting for missing info.
User. /generate_interactive_explanation solve this mesh problem
Assistant. Before I generate the explanation, I need 3 things.
1. Problem source (textbook/homework/exam with identifier)
2. Context level (high or low)
3. Model preference (opus/sonnet/haiku)
