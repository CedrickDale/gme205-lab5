import pytest
from shapely.geometry import box
from shapely.geometry import LineString
from spatial import Road
from rules import RoadAccessRule

from spatial import Parcel, HazardZone
from rules import (
    RuleResult,
    MinimumAreaRule,
    AllowedZoneRule,
    NoHazardOverlapRule,
)
from assessment import ParcelAssessment


@pytest.fixture
def scenario():
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
    ]

    return parcel_a, parcel_b, rules


def test_assessment_accepts_mixed_rule_subclasses(scenario):
    parcel_a, parcel_b, rules = scenario
    assessment = ParcelAssessment(parcel_b, rules)

    results = assessment.evaluate()

    assert len(results) == 3
    assert all(isinstance(result, RuleResult) for result in results)


def test_parcel_a_fails_only_hazard_rule(scenario):
    parcel_a, parcel_b, rules = scenario
    assessment = ParcelAssessment(parcel_a, rules)

    results = assessment.evaluate()

    assert [result.passed for result in results] == [True, True, False]
    assert assessment.passed() is False


def test_parcel_b_passes_all_rules(scenario):
    parcel_a, parcel_b, rules = scenario
    assessment = ParcelAssessment(parcel_b, rules)

    results = assessment.evaluate()

    assert [result.passed for result in results] == [True, True, True]
    assert assessment.passed() is True


def test_assessment_rejects_empty_rule_list(scenario):
    parcel_a, parcel_b, rules = scenario

    with pytest.raises(ValueError):
        ParcelAssessment(parcel_a, [])

@pytest.mark.parametrize(
    "max_distance, expected",
    [
        (30, True),
        (10, False),
    ],
)
def test_assessment_accepts_road_access_rule(
    scenario, max_distance, expected
):
    _, parcel_b, rules = scenario

    road = Road(
        "R-001",
        LineString([(0, -20), (200, -20)]),
    )
    extended_rules = rules + [RoadAccessRule(road, max_distance)]

    assessment = ParcelAssessment(parcel_b, extended_rules)
    results = assessment.evaluate()

    assert len(results) == 4
    assert all(isinstance(result, RuleResult) for result in results)
    assert [result.passed for result in results] == [
        True,
        True,
        True,
        expected,
    ]
    assert assessment.passed() is expected