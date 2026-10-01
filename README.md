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
| Hazard intersection rule | Specialized rule | Yes | `NoHazardOverlapRule` uses one `HazardZone` and passes only when the parcel does not intersect it. |
| Rule result | Value object | Yes | `RuleResult` gives every rule one consistent way to return its name, decision, and explanation. |
| Parcel assessment | Coordinator | Yes | It is discovered from the phrase "runs every rule" and keeps the loop out of the rules and the runner. |
| Geometry | Spatial attribute | No new class | `Parcel` and `HazardZone` store Shapely geometry objects; this exercise does not require a new geometry class. |
| Minimum area threshold | Rule configuration | No | It is a number stored by `MinimumAreaRule`, while the rule class owns the evaluation behavior. |
| Allowed zones | Rule configuration | No | They form a set stored by `AllowedZoneRule`, rather than a separate object with its own responsibility. |
| Report | Output representation | Not yet | A dictionary written to JSON is enough; a `Report` class would add little responsibility. |
 
### Actions and responsibilities
 
| Action from the problem | Likely owner | Design consequence |
|---|---|---|
| Check whether a parcel intersects a hazard zone | `Parcel` | Provide a reusable `intersects(other)` so rules do not repeat geometry calls. |
| Evaluate one development condition | A subclass of `AssessmentRule` | Each rule implements `evaluate(parcel)` for its own criterion. |
| Run every rule for a parcel | `ParcelAssessment` | It owns the iteration and combines the results. |
| Store a decision and its explanation | `RuleResult` | Holds the rule name, passed flag, and message returned by a rule. |
| Add a new development condition | A new `AssessmentRule` subclass | It follows the same `evaluate(parcel)` contract, so the assessment loop is unchanged. |

## Extension without coordinator rewrite

The original assessment used three independent rules:

```python
rules = [
    MinimumAreaRule(5000),
    AllowedZoneRule({"Residential", "Commercial"}),
    NoHazardOverlapRule(hazard),
]
```

Following the laboratory's recommended extension, I added a `Road` class and a `RoadAccessRule` subclass. `Road` stores an identifier and a Shapely `LineString` geometry. `RoadAccessRule` stores one road and a maximum distance, and passes when the shortest distance between the parcel and the road is less than or equal to that threshold.

The extended rules list is:

```python
rules = [
    MinimumAreaRule(5000),
    AllowedZoneRule({"Residential", "Commercial"}),
    NoHazardOverlapRule(hazard),
    RoadAccessRule(road, 30),
]
```

The assessment loop remained unchanged:

```python
def evaluate(self):
    results = []
    for rule in self._rules:
        result = rule.evaluate(self._parcel)
        results.append(result)
    return results
```

This works because every concrete rule follows the `AssessmentRule` contract: it implements `evaluate(parcel)` and returns a `RuleResult`. `ParcelAssessment` makes the same method call on each rule object, while each object supplies its own evaluation behavior.

For the extension scenario, the road runs from `(0, -20)` to `(200, -20)`, and the maximum distance is 30 coordinate units. Both parcels are 20 units from the road and pass the road-access rule. These road coordinates and the threshold were chosen for this implementation; the original parcel and hazard inputs follow the laboratory's fixed scenario.

The final UML was updated to include `Road`, `RoadAccessRule`, the inheritance relationship to `AssessmentRule`, and the association showing that each `RoadAccessRule` uses one `Road`.

### Weak alternative

A weaker design would select the screening behavior through a central conditional:

```python
if rule_type == "minimum_area":
    ...
elif rule_type == "allowed_zone":
    ...
elif rule_type == "hazard_overlap":
    ...
elif rule_type == "road_access":
    ...
```

Every new rule would require another branch and a change to the coordinator. In the implemented design, the new behavior belongs to a new rule subclass. Adding its object to the rules list extends the assessment without rewriting `ParcelAssessment.evaluate()`.

## OOP Pillar Evidence

| Pillar | Evidence in the implementation | Purpose |
|---|---|---|
| Encapsulation | `Parcel` stores state in attributes such as `_area_sqm`, validates constructor inputs, and exposes read-only properties. | Keeps state management inside the object and prevents invalid initial values and assignment through properties without setters. |
| Abstraction | `AssessmentRule` inherits from `ABC` and declares `evaluate(parcel)` with `@abstractmethod`. | Defines the common operation that every concrete rule must implement. |
| Inheritance | `MinimumAreaRule`, `AllowedZoneRule`, `NoHazardOverlapRule`, and `RoadAccessRule` inherit from `AssessmentRule`. | Shares the rule-name initialization, `name` property, and evaluation contract. |
| Polymorphism | `ParcelAssessment.evaluate()` calls `rule.evaluate(self._parcel)` on every rule object. | Runs different screening behaviors through one interface without branching on concrete rule types. |

Python's leading underscore marks an attribute as internal by convention; it does not make the attribute inaccessible. The read-only properties provide the intended public interface, while constructor validation rejects a missing parcel identifier, an empty zone, and a non-positive recorded area.

### Object Relationships

`ParcelAssessment` has one parcel and a collection of rules. It stores these objects as references in `_parcel` and `_rules`, corresponding to the has-a relationships shown in the UML. An assessment is neither a parcel nor a rule, so inheritance would not express its responsibility correctly.

`NoHazardOverlapRule` stores a reference to one `HazardZone`, while `RoadAccessRule` stores a reference to one `Road`. These associations provide the spatial objects needed by each rule.

`RuleResult` is a frozen dataclass containing the rule name, passed flag, and explanation. It provides a consistent result structure for all rules.

### Separation of Responsibilities

- `spatial.py` represents parcels, hazard zones, and roads and provides parcel intersection behavior.
- `rules.py` implements the individual screening conditions and the common result structure.
- `assessment.py` coordinates the rules and determines whether an assessment passes.
- `run_lab5.py` constructs the scenario, runs assessments, assembles the report, and writes JSON.
- `demo.py` contains small experiments used to check object behavior.

The runner leaves the area, zoning, hazard, and road-distance decisions inside their respective rule classes.

## Reflection

### 1. OOAD: What changed in your thinking when you modeled the problem before writing the class implementations?

Modeling first helped me distinguish the information that the system stores from the responsibilities it performs. Instead of placing all screening conditions in the runner, I assigned each condition to a rule class and assigned the assessment loop to `ParcelAssessment`. The UML provided me a clear structure to follow when implementing these classes.

### 2. Candidate classes: Name one noun from the problem statement that you intentionally did not make into a class. Why?

I did not create a separate class for zoning classification. As shown in the UML, zoning is stored as a string attribute on `Parcel`, while the decision about whether a zone is acceptable belongs to `AllowedZoneRule`. Creating a separate zoning class was unnecessary for the requirements of this laboratory and would have added unnecessary structure without providing additional responsibility.

### 3. Encapsulation: Which Parcel state is protected by its interface, and what invalid state does the constructor prevent?

`Parcel` stores its identifier, geometry, zone, and recorded area in internal attributes and exposes them through read-only properties. Its constructor rejects a missing identifier, an empty zone, or a non-positive area. Assigning directly to `parcel.area_sqm` raises an `AttributeError` because the property has no setter. This underscore convention marks internal attributes but does not make them inaccessible in Python.

### 4. Abstraction: What does AssessmentRule promise without knowing the details of a specific rule?

`AssessmentRule` defines the common `evaluate(parcel)` operation that concrete rules must implement. The design requires each implementation to return a `RuleResult` containing its name, decision, and explanation. The abstract class does not specify how an area, zoning, hazard intersection, or road distance should be evaluated.

### 5. Inheritance: What code or contract is shared by the concrete rule subclasses?

The concrete rules inherit the rule-name initialization and the `name` property from `AssessmentRule`. They also follow its abstract `evaluate(parcel)` contract. Each subclass implements the evaluation behavior for its own screening conditions.

### 6. Polymorphism: Why can ParcelAssessment call evaluate(parcel) without knowing which concrete rule object it received?

Polymorphism allows different classes to share the same interface, while each class executes its own distinct behavior. In this case, every concrete rule provides the same `evaluate(parcel)` interface. `ParcelAssessment` calls that method on each object, and Python dynamically executes the implementation belonging to that specific rule's class. Thus, the coordinator does not need a conditional branch for each rule type.

### 7. Composition: Why is ParcelAssessment better modeled as having a Parcel and rules rather than inheriting from them?

An assessment coordinates a parcel and its rules, neither of which makes the assessment a parcel nor a rule itself. Storing references to these objects expresses that has-a relationship and keeps their responsibilities separate. The assessment manages evaluation, while the parcel stores spatial state and each rule owns one condition.

### 8. Extension: What did you add for the new rule, and what existing code did you not need to change?

I added a `Road` class with an identifier and `LineString` geometry, along with a `RoadAccessRule` subclass with a road reference and maximum distance limit. I also constructed a road and added the new rule object to the runner's rules list. I did not change `ParcelAssessment.evaluate()`, because the new rule follows the existing interface. Finally, I updated the UML diagram and added unit tests for the new extension.

### 9. UML-to-code consistency: Give one example where the final diagram helped you detect or correct a code-structure problem.

The UML shows that `ParcelAssessment` must provide `evaluate(): list<RuleResult>`. During implementation, the demo first reported that `evaluate()` returned a non-iterable value, and a later run reported that the assessment object had no `evaluate` method. These errors showed a mismatch with the interface specified in the diagram. I corrected the class so that it defines `evaluate()` and returns the collected rule results. The subsequent demo successfully displayed all three results and the overall decision.