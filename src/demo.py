from shapely.geometry import box
from spatial import Parcel, HazardZone
from rules import MinimumAreaRule, AllowedZoneRule, NoHazardOverlapRule


# Create a parcel and a separate hazard zone.
parcel = Parcel(
    parcel_id="P001",
    geometry=box(0, 0, 20, 30),
    zone="Residential",
    area_sqm=600,
)

hazard = HazardZone(
    hazard_id="H001",
    geometry=box(40, 40, 50, 50),
    hazard_type="Flood",
    severity="High",
)

# Evaluate each rule independently.
rules = [
    MinimumAreaRule(500),
    AllowedZoneRule({"Residential", "Commercial"}),
    NoHazardOverlapRule(hazard),
]

for rule in rules:
    result = rule.evaluate(parcel)
    print(f"{result.rule_name}: {result.passed} — {result.message}")

# Check encapsulation.
try:
    parcel.area_sqm = -100
except AttributeError:
    print("Encapsulation check: direct area assignment is blocked")

# Check constructor validation.
try:
    Parcel("P002", box(0, 0, 10, 10), "Residential", -100)
except ValueError as error:
    print(f"Validation check: {error}")