# Week 2: Problem Identification Assignment

## GRAND CHALLENGE: Healthcare Affordability in the United States

Americans pay the highest healthcare costs in the world while health benefits lag behind other developed nations. Medical debt is the leading cause of bankruptcy in the US.

---

## TOP-DOWN APPROACH: Narrowing the Problem

- **Level 1:** Healthcare Affordability Crisis
- **Level 2:** High out of pocket costs for patients
- **Level 3:** Hospital bills are unpredictable and inflated
- **Level 4:** 80% of medical bills contain errors and overcharges
- **Level 5:** Patients don't know how to identify or dispute billing errors

---

## 5-WHYS ROOT CAUSE ANALYSIS

**Observed Problem:** Americans are drowning in medical debt they shouldn't owe.

### WHY #1: Why do people pay inflated medical bills?
- They don't know the bills contain errors.

### WHY #2: Why don't they know?
- Medical billing is intentionally opaque. CPT codes, bundled charges, insurance adjustments are incomprehensible to average patients.

### WHY #3: Why is billing so opaque?
- Hospitals benefit financially from patients not understanding what they're charged. There's no incentive for transparency.

### WHY #4: Why hasn't this been solved?
- Bill review requires specialized knowledge. Medical coding, insurance contracts, and legal compliance rules that take years to learn.

### WHY #5: Why don't patients have access to that specialized knowledge?
- No consumer friendly tool exists that can automatically audit medical bills and identify errors at scale.

**ROOT CAUSE IDENTIFIED:**  
Patients lack the specialized knowledge to identify billing errors, and no accessible, automated tool exists to audit bills and negotiate on their behalf.

---

## SUPPORTING DATA

- 80% of medical bills contain errors (duplicate charges, wrong codes, illegal bundling)
- Medical debt affects 100+ million Americans
- The average American cannot identify CPT code errors or Medicare billing violations
- One patient used AI to reduce a $195,000 hospital bill to $33,000 (83% reduction) by identifying duplicate codes and illegal double billing

---

## REFRAMING THE PROBLEM

**Original Framing:** "Healthcare is too expensive"  
This frames the problem as a policy issue requiring systemic change

**Reframed:** "Patients are overcharged due to billing errors they cannot detect"  
This frames the problem as a knowledge/tool gap that can be solved with technology

---

## PROBLEM STATEMENT

80% of hospital bills contain errors. Duplicate charges, incorrect procedure codes, and illegal bundling, but patients pay them anyway because they lack the specialized medical billing knowledge to identify and dispute overcharges, resulting in over $200 billion in unnecessary medical debt annually.

---

## FEASIBILITY CHECK

**Do I understand the problem?**  
✓ Yes. Well documented with 80% error rate statistics

**Am I solving the right problem?**  
✓ Yes. Root cause is knowledge gap, not healthcare policy

**Large enough to matter?**  
✓ Yes. Affects 100+ million Americans, $200B+ in unnecessary debt

**Small enough to solve?**  
✓ Yes. Can start with one bill type (like hospital stays)

**Feasible with current technology?**  
✓ Yes. LLMs can parse itemized bills and cite specific billing violations

---

## POTENTIAL SOLUTION DIRECTION

**A "GoodRx for Medical Bills":** An AI-powered tool that:

1. Scans itemized hospital bills
2. Identifies errors (duplicate charges, wrong codes, bundling violations)
3. Generates dispute letters citing specific Medicare/insurance rules
4. Helps patients negotiate reductions or access charity care programs
