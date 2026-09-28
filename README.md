# GmE 205 Laboratory 5 — Object-Oriented Spatial Modeling with UML

The main objective of this laboratory activity is to design a parcel development assessment system using object-oriented analysis and design (OOAD). A UML class diagram is created before implementation to show the classes, their responsibilities, and their relationships. The design is then translated into Python.

This laboratory builds on the `SpatialObject` and `Parcel` ideas from previous laboratories. Independent rule objects evaluate a parcel’s area, zoning classification, and intersection with a hazard zone. A `ParcelAssessment` coordinates the rules and collects their results. The system is designed so that new rules can be added without changing the assessment loop.

## Objectives

The objectives of this laboratory are to:

- Analyze a parcel development problem and identify requirements before coding.
- Identify candidate classes, attributes, operations, and responsibilities.
- Create a UML class diagram showing inheritance, composition or association, multiplicity, and an abstract operation.
- Translate the UML design into modular Python classes.
- Demonstrate encapsulation, abstraction, inheritance, and polymorphism.
- Evaluate parcels through independent rule objects and produce consistent rule results.
- Add a new rule without rewriting the assessment loop.
- Produce a JSON assessment report and verify the implementation with focused tests.

## Tools and Technologies

The following tools were used:

- Python 3.x
- Visual Studio Code
- Git
- GitHub
- Shapely
- pytest
- diagrams.net (draw.io) or another UML diagramming tool
- JSON

### How to set up the virtual environment

1. Open the project folder (`gme205-lab5`) in VS Code.
2. Open the terminal (`Terminal -> New Terminal`) and create the virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

3. Confirm that the terminal prompt shows `(.venv)`.
4. Select the interpreter inside `.venv` using `Ctrl + Shift + P` → `Python: Select Interpreter`.
5. Install the required packages and update `requirements.txt`:

```powershell
python -m pip install shapely pytest
python -m pip freeze > requirements.txt
```

## Part B — Problem Analysis
 
### Problem statement
 
A local planning team wants a small program that screens land parcels against several independent development rules. Every parcel carries an identifier, a geometry, a zoning classification, and a recorded area in square meters. The first version applies three rules: the parcel must meet a minimum area, its zone must belong to an allowed set, and it must not intersect a mapped hazard zone.
 
Each rule reports its own name, whether the parcel passed, and a short explanation. The program runs every rule on a parcel, collects the results into one report, and decides whether the parcel passes overall. Because policies change, the design must let a future rule (for example, road-access proximity) be added without rewriting the code that runs the rules.
 
### Requirements
 
- Represent a `Parcel` with an identifier, geometry, zone, and `area_sqm`.
- Represent a `HazardZone` with an identifier, geometry, hazard type, and severity.
- Evaluate a parcel against several independent rules.
- Return the same `RuleResult` shape (rule name, passed flag, message) from every rule.
- Derive one overall pass/fail decision from the collected results.
- Let a new rule join the assessment without editing the assessment loop.

### Analysis and design
 
**Analysis** asks what the system must represent and do. The domain concepts are parcels, hazard zones, rules, rule results, and assessments.
 
**Design** decides which class owns each responsibility. A rule object decides one criterion. `ParcelAssessment` owns the loop that runs all rules and gathers their results. `Parcel` owns its state and its spatial behavior.
 
**What changes frequently:** individual policy rules (thresholds, allowed zones, new criteria).
 
**What should stay stable:** the assessment process — for each rule, evaluate this parcel and collect the result.
 
**Implementation** comes last: the design is translated into Python only after the UML diagram is complete.
 
### Candidate classes
 
| Phrase from the problem | Initial interpretation | Keep as a class? | Reason |
|---|---|---|---|
| Planning team | Actor / stakeholder | No | The team uses the program but is not part of the domain being modeled. |
| Parcel | Spatial domain entity | Yes | It has identity, state, and geometry behavior (`intersects`) that other objects rely on. |
| Parcel identifier | Parcel attribute | No | A value stored inside `Parcel` with no behavior of its own. |
| Zoning classification | Parcel attribute | No | A string carried by `Parcel`; the policy about which zones are acceptable belongs to a rule. |
| Recorded area | Parcel attribute | No | `area_sqm` is a number stored by `Parcel`. |
| Hazard zone | Spatial domain entity | Yes | It has its own identity, geometry, hazard type, and severity. |
| Assessment rule | Behavioral abstraction | Yes | `AssessmentRule` defines the `evaluate(parcel)` contract shared by every rule. |
| Minimum area rule | Specialized rule | Yes | `MinimumAreaRule` owns the area threshold and the behavior that checks it. |
| Allowed zone rule | Specialized rule | Yes | `AllowedZoneRule` owns the set of allowed zones and the behavior that checks a parcel's zone. |
| Hazard intersection rule | Specialized rule | Yes | `NoHazardOverlapRule` uses a `HazardZone` and passes only when the parcel does not intersect it. |
| Rule result | Value object | Yes | `RuleResult` gives every rule one consistent way to return its name, decision, and explanation. |
| Parcel assessment | Coordinator | Yes | It is discovered from the phrase "runs every rule" and keeps the loop out of the rules and the runner. |
| Report | Output representation | Not yet | A dictionary written to JSON is enough; a `Report` class would add little responsibility. |
 
### Actions and responsibilities
 
| Action from the problem | Likely owner | Design consequence |
|---|---|---|
| Check whether a parcel intersects a hazard zone | `Parcel` | Provide a reusable `intersects(other)` so rules do not repeat geometry calls. |
| Evaluate one development condition | A subclass of `AssessmentRule` | Each rule implements `evaluate(parcel)` for its own criterion. |
| Run every rule for a parcel | `ParcelAssessment` | It owns the iteration and combines the results. |
| Store a decision and its explanation | `RuleResult` | Holds the rule name, passed flag, and message returned by a rule. |
| Add a new development condition | A new `AssessmentRule` subclass | It follows the same `evaluate(parcel)` contract, so the assessment loop is unchanged. |