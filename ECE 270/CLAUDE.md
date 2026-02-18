# ECE 270 Digital System Design

## Course Overview
ECE 270 covers digital system design fundamentals including number systems, logic gates, Boolean algebra, CMOS circuits, combinational circuits, sequential circuits, and arithmetic circuits.

## How to Help Me

### Primary Focus
Create interactive lecture content that helps me understand and retain course material. Transform dense lecture PDFs into engaging visual explanations.

### Creating Interactive HTML Explanations

CRITICAL REQUIREMENT. When creating HTML explanation files, focus primarily on WORKED EXAMPLES. The user prefers fewer text heavy explanations and more practical application. Include at least 5 to 10 detailed worked examples per concept. The text should be concise and supportive, not the main focus. Breakdown complex diagrams and steps visually. Still reference specific textbook sections and page numbers. The goal is to learn by doing and seeing examples, not by reading long paragraphs.

### Using the Textbook

The Wakerly textbook (Digital Design Principles and Practices 4th Edition) is located at the ECE 270 root folder. When creating explanations or answering questions, ALWAYS search the textbook for relevant content. Search for specific terms, chapter headings, and figure references. Extract worked examples from the textbook to supplement lecture content. Use textbook explanations when they provide clearer or more detailed coverage than lectures. Reference specific page numbers and sections so I can read more if needed.

### Practice Problems and Quizzes

NEVER make up practice problems. ALWAYS pull from actual course materials in this priority order.
1. Practice exams and past exams
2. Homeworks
3. PCQs
4. Recitations
5. Lectures themselves (iClicker questions)

ALWAYS cite the source of every practice problem. For example, "From Fall 24 Exam 1, Question 3" or "From HW2, Problem 5" or "From Lecture 1.4a iClicker". This lets me know where the question came from and find similar problems.

When presenting problems, show the problem first without the answer. Let me attempt it or ask for hints. Only reveal the full solution when I ask or after I provide my attempt.

### Formatting Rules
Follow the main CLAUDE.md formatting rules. No arrows, dashes, colons, bullets, emojis, or tables in responses.

## Course Structure

### Module 1 Fundamentals (Exam 1)
1.1 Number Systems
1.2 Logic Gates
1.3 Boolean Algebra (Part I and Part II)
1.4 CMOS Circuits (Part I and Part II)

### Module 2 Combinational Circuit Analysis and Design (Exam 2)
Content to be added as lectures are uploaded

### Module 3 Sequential Circuit Analysis and Design (Final)
Content to be added as lectures are uploaded

### Module 4 Arithmetic Circuit Analysis and Design (Final)
Content to be added as lectures are uploaded

## Folder Structure

lectures/ contains lecture PDFs named by topic (lec1.1, lec1.2, etc.)
recitations:review/ contains weekly review and recitation materials
weeklyreview:recitation/ contains additional weekly materials organized by week
student-labs-main/ contains lab assignments and SystemVerilog reference files
Exams/ contains exam learning objectives and past exams

## Labs

### Syncing Labs from GitHub

NEVER use git pull directly on the student-labs-main folder. This will overwrite completed work.

Use the `/sync-ece270-labs` skill to safely pull new labs. This only adds NEW labs that don't exist locally and never touches existing lab folders or files.

### Lab Environment

Labs use SystemVerilog and simulate on FPGA hardware.
Lab reference files are in student-labs-main/refs/ including datasheets for 74HC series chips.

### Lab Wiring Help

When starting a new lab that involves breadboard circuit construction, ALWAYS read the full lab document first and then provide a wiring guide. This should include the wire color to length mapping from the wire kit, the exact chip pin connections based on datasheets, the DIO pin assignments for the AD2, and the test combinations for verifying each subcircuit. Do this before any wiring begins.

The wire kit uses a color = length system. Each color corresponds to a specific wire length. When chips are placed at the right breadboard positions, the correct color wire will span exactly between the two holes. Wires should lay flat against the breadboard, no arching. The lab docs sometimes suggest specific colors for specific connections based on chip placement (e.g. gray for short runs, purple for medium, white for pairing gate inputs, green and orange for long runs). Always check the lab images and placement instructions to determine what lengths are needed.

Be smart about color mapping. Assign colors so that related signals use the same color (e.g. all carry signals one color, all sum signals another, inputs grouped by function). This makes debugging much easier since you can visually trace signal groups. After presenting the color mapping, ALWAYS ask the user if it looks good or if they want to change any of the color assignments before they start wiring.

### Key SystemVerilog Concepts
Structural modeling uses primitive gates and module instances.
Behavioral modeling uses always_comb for combinational and always_ff for sequential circuits.
Vector notation uses [7:0] for bit ranges and {} for concatenation.

## Textbook
Digital Design Principles and Practices (4th Edition) by John F. Wakerly
The textbook PDF is located in the ECE 270 root folder.

### MCP Setup for Textbook Access
The local-rag MCP server is configured to enable semantic search through the textbook without hitting token limits.

To ingest the textbook (first time only), ingest the PDF file located in this course folder.

To search the textbook:
"What does the textbook say about [topic]?"
"Search for [concept] in the textbook"
"Find the section on [topic]"

If the MCP is not working, reinstall with:
claude mcp add local-rag --scope user -- npx -y mcp-local-rag

## Interactive Explanations Created
explanations/cmos-explained.html covers CMOS transistors, inverter, NAND, NOR, electrical characteristics, timing, and power with practice questions from lectures 1.4a and 1.4b
