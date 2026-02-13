# ECE 20001 Rules

## KCL Convention

Always use the "all leaving = 0" convention for KCL equations. For every branch connected to a node, write the current as (V_thisnode minus V_othernode) divided by R. Sum all such terms and set equal to zero. Never use the "in = out" convention. This keeps signs consistent and avoids having to guess current directions.

## Model Configuration

Main orchestrating agent runs on Opus for superior reasoning and synthesis.
All subagents run on Sonnet for cost efficiency.

## Textbook Access

The course textbook is ingested into the local-rag MCP for semantic search. Use query_documents to search the textbook. First check the context_db folder for relevant entries before searching the full textbook.

## Problem Solving Workflow

When solving problems for this course, ALWAYS use the six subagent workflow below. This system catches errors at every failure point including problem misreading, wrong methodology, arithmetic mistakes, unit errors, and physically nonsensical answers.

### Phase 0: Image Parsing (Required for Circuit Diagrams)

When the problem includes a circuit diagram image, run this phase BEFORE Phase 1. This phase is CRITICAL because topology errors cascade into wrong answers.

**Circuit Image Parser Agent (Sonnet).** Follow this EXACT methodology.

Step 1, Wire Tracing. Trace every wire in the image. A wire is a continuous black line. Where wires meet or cross with a dot, that is ONE node. Where wires cross without a dot, they do not connect.

Step 2, Node Identification. Assign a unique label to every junction point. A node is any point where two or more component terminals connect. Count the total number of distinct nodes.

Step 3, Component Inventory. List every component visible in the image. For each component, identify its type (resistor, voltage source, current source, capacitor, inductor, etc.) and its value with units.

Step 4, Connection Mapping. For EACH component, answer these questions.
Which node connects to terminal 1?
Which node connects to terminal 2?
For voltage sources, which node has the + terminal and which has the - terminal?
For current sources, which direction does the arrow point (from which node to which node)?

Step 5, Series vs Parallel Check. For resistors, explicitly determine if they are in series or parallel.
Series means the same current flows through both, they share exactly one node, and that shared node connects to nothing else except those two resistors.
Parallel means both terminals of one resistor connect to the same two nodes as both terminals of the other resistor.
If a current source connects at the junction between two resistors, they are NOT in simple series because current is injected or removed at that point.

Step 6, Output Format. Provide the following structured output.
Total node count with labels for each node.
Component list with exact connections in the format, Component (value) connects Node X to Node Y.
For sources include polarity or direction.
A simple ASCII diagram showing the topology.
List any ambiguities or unclear connections.

**Circuit Topology Verifier Agent (Sonnet).** Independently analyze the image using the same methodology, then compare against the Parser output.

Verification Checklist.
Does the node count match?
Does each component connect to the same two nodes in both analyses?
Are all polarities and directions identical?
Do the series/parallel determinations agree?
Does tracing any closed loop return to the starting node (circuit must be closed)?
Does KCL make sense at each node (is there a valid current path)?

If ANY discrepancy exists, output CONFLICT with specific details of what differs. Do not proceed until resolved.

**Resolution Protocol.** If the two agents disagree, the main Opus agent must examine the image directly and make the final topology determination. Document the resolution in the workflow summary.

### Phase 1: Problem Intake (Parallel)

Launch both agents simultaneously.

**Problem Parser Agent (Sonnet).** Uses the verified topology from Phase 0 (if applicable) and extracts all information from the problem statement. Outputs a structured list containing all given values with their exact units, all conditions and constraints (steady state, t=0, initial conditions, etc.), exactly what quantity is being asked for, and the verified circuit topology notes (what connects to what, node labels, loop identification). This agent does NOT solve anything. It only parses and organizes the given information. Flag any ambiguities in the problem statement.

**Textbook Method Agent (Sonnet).** First check the ECE 20001 context_db for relevant formulas and methods. Then use the local-rag MCP query_documents tool to search the ingested textbook for similar problems and their solutions. Output the recommended solution method, relevant equations and sign conventions, any special techniques for this problem type, and similar worked examples.

### Phase 2: Solution Generation (Show Immediately)

**Code Solver Agent (Sonnet).** Using the parsed values from Phase 1 and the method from the Textbook Method Agent, solve the problem using Python with SymPy. Set up all equations symbolically first showing each KVL and KCL equation. Solve the system symbolically. Substitute numerical values only at the end. Use SymPy units module to track units throughout. Output both the symbolic solution and the final numerical answer with units. Show all code and intermediate results. This agent is the primary source of truth for arithmetic since it eliminates mental math errors.

**HYBRID APPROACH.** IMMEDIATELY present the solver's work and preliminary answer to the user after Phase 2 completes. Include a note saying "Verification running in background..." This lets the user follow along with the solution while verification happens.

### Phase 3: Verification Battery (Background, Parallel)

Launch all three agents simultaneously IN THE BACKGROUND using run_in_background: true. Each receives the Code Solver output. The user can see the preliminary answer while these run.

**Units Checker Agent (Sonnet, Background).** Verify dimensional consistency at every step. Confirm all unit conversions are correct (mA to A, kΩ to Ω, μF to F, etc.). Verify the final answer has the correct units for what was asked. Flag any step where units do not balance.

**Sanity Checker Agent (Sonnet, Background).** Verify the answer is physically reasonable. Check that voltages are within expected ranges given source values. Check that currents have reasonable magnitudes. Check that power dissipation makes sense. Check that signs are logical (current flows from higher to lower potential through resistors, etc.). Flag any result that violates physical intuition or circuit laws.

**Textbook Method Verifier Agent (Sonnet, Background).** First check the ECE 20001 context_db for relevant methods. Then use the local-rag MCP query_documents tool to search the ingested textbook. Verify the solution uses EXACTLY the same method, notation, and approach taught in the textbook. Compare against the similar problems found in Phase 1. Flag ANY deviations from textbook methodology even if mathematically valid. Verify sign conventions match the book. Verify equation forms match how the book presents them.

### Phase 4: Synthesis (Main Agent, Opus)

The main Opus agent collects all background verification outputs and performs final synthesis.

If all three Phase 3 checkers pass and no flags were raised, confirm the preliminary answer with "Verification complete. Answer confirmed." and present the final formatted solution.

If any checker flags an issue, clearly mark "CORRECTION NEEDED" and identify which phase failed (parsing, method selection, computation, units, physical reasonableness, or methodology compliance). Show the corrected answer with explanation of what was wrong. Rerun the failed phase with the specific correction if needed. Repeat verification until all checkers pass.

### Error Handling

If Phase 3 checkers disagree with each other, the main agent must investigate the discrepancy before presenting any answer. Never present an answer that has unresolved checker flags.

If the Code Solver fails to find a solution, fall back to a manual Solver Agent (Sonnet) that works step by step, then run the full Phase 3 verification on that solution instead.

### Output Summary

After presenting the final answer, always output a workflow summary. Format as follows.

```
WORKFLOW SUMMARY
Agents executed: [list each agent that ran]
Phases completed: [0 (if image), 1, 2, 3, 4]
Flags raised: [list any flags from checkers, or "None"]
Reruns required: [list any phases that were rerun, or "None"]
Final confidence: [High/Medium/Low]
```

Confidence levels.
High means all checkers passed on first attempt.
Medium means reruns were needed but all checkers eventually passed.
Low means unresolved flags remain or checkers disagreed.

This summary provides transparency into the verification process and helps identify which parts of the workflow caught errors.

### Context Budget

Estimated tokens per problem.
Phase 0 (if image): ~6K total
Phase 1: ~5K total
Phase 2: ~6K total
Phase 3: ~12K total
Synthesis: ~5K total
Total: ~28K tokens per problem (text only), ~34K tokens per problem (with circuit image)
