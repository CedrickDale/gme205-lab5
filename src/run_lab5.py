import json
from dataclasses import asdict
from pathlib import Path

from shapely.geometry import box, LineString
from assessment import ParcelAssessment
from spatial import Parcel, HazardZone, Road
from rules import (
    MinimumAreaRule,
    AllowedZoneRule,
    NoHazardOverlapRule,
    RoadAccessRule,
)


def main():
    parcel_a = Parcel(
        "P-001",
        box(0, 0, 80, 90),
        "Residential",
        7200,
    )

    parcel_b = Parcel(
        "P-002",
        box(120, 0, 190, 80),
        "Commercial",
        5600,
    )

    road = Road(
        "R-001",
        LineString([(0, -20), (200, -20)]),
    )

    hazard = HazardZone(
        "HZ-01",
        box(60, 50, 110, 100),
        "Flood",
        "High",
    )

    rules = [
        MinimumAreaRule(5000),
        AllowedZoneRule({"Residential", "Commercial"}),
        NoHazardOverlapRule(hazard),
        RoadAccessRule(road, 30),
    ]

    report = {
        "scenario": "parcel-development-assessment",
        "parcels": [],
    }

    for parcel in [parcel_a, parcel_b]:
        assessment = ParcelAssessment(parcel, rules)
        results = assessment.evaluate()
        overall_passed = all(result.passed for result in results)

        report["parcels"].append({
            "parcel_id": parcel.parcel_id,
            "passed": overall_passed,
            "results": [asdict(result) for result in results],
        })

        print(f"\nParcel: {parcel.parcel_id}")

        for result in results:
            print(
                f"{result.rule_name}: {result.passed} — "
                f"{result.message}"
            )

        print(f"Overall passed: {overall_passed}")

    project_folder = Path(__file__).resolve().parent.parent
    output_folder = project_folder / "output"
    output_folder.mkdir(parents=True, exist_ok=True)
    output_file = output_folder / "lab5_report.json"

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, ensure_ascii=False)

    print(f"\nReport saved to: {output_file}")


if __name__ == "__main__":
    main()