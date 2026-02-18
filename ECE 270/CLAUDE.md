# ECE 270: Digital System Design - Agent Rules

## 1. Core Instructions
**Primary Goal**: Create interactive, visually engaging HTML explanations from dense lecture PDFs.
**Key Rule**: Focus on **WORKED EXAMPLES**.
*   User learns by doing.
*   Provide 5-10 detailed examples per concept.
*   Keep text concise and supportive; avoid long paragraphs.
*   Break down complex diagrams visually.

## 2. Resources & Authority
**Textbook**: *Digital Design Principles and Practices (4th Ed)* by Wakerly.
*   **Location**: Root `ECE 270` folder.
*   **Usage**: ALWAYS search this first using `local-rag` MCP.
    *   *Prompt*: "Search for [concept] in the textbook".

**Practice Problems**:
*   **Source Priority** (Strict):
    1.  Practice/Past Exams
    2.  Homeworks
    3.  PCQs
    4.  Recitations
    5.  Lectures (iClicker)
*   **Citation**: ALWAYS cite the source (e.g., "From Fall 24 Exam 1, Q3").
*   **Presentation**: Show problem -> Wait for user attempt -> Reveal solution.

## 3. Formatting Rules
*   **Restricted**: No arrows, dashes, colons, bullets, emojis, or tables in responses.
*   **Style**: Clean, paragraph-based or numbered lists where appropriate.

## 4. Lab Workflow
**Syncing**:
*   Use the `/sync-ece270-labs` skill.
*   **NEVER** use `git pull` directly on `student-labs-main` (overwrites work).

**Wiring & Hardware**:
*   **Wiring Guide**: BEFORE wiring, provide a color-coded guide (Color = Length).
    *   Group signals by color (e.g., all carries = blue).
    *   Verify pin connections with datasheets (`refs/` folder).
*   **Images**: Look in the lab's `src/` folder for notebook images (attachment:image.png).

**SystemVerilog**:
*   **Structural**: Primitive gates, module instances.
*   **Behavioral**: `always_comb` (combinational), `always_ff` (sequential).
*   **Vectors**: `[7:0]` for ranges, `{}` for concatenation.

## 5. Course Modules
*   **Module 1**: Fundamentals (Number Systems, Logic Gates, Boolean Algebra, CMOS) - *Exam 1*
*   **Module 2**: Combinational Circuit Analysis - *Exam 2*
*   **Module 3**: Sequential Circuit Analysis - *Final*
*   **Module 4**: Arithmetic Circuits - *Final*

## 6. Directory Structure
*   `lectures/`: Lecture PDFs (e.g., `lec1.1.pdf`).
*   `student-labs-main/`: Labs, scripts, and reference sheets.
*   `explanations/`: Generated HTML files.
*   `Exams/`: Past exams and learning objectives.

## 7. Interactive Explanations Log
*   `explanations/cmos-explained.html`: CMOS transistors, inverters, NAND/NOR, logic levels.
