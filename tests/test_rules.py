import pytest
from shapely.geometry import box
from shapely.geometry import LineString
from spatial import Road
from rules import RoadAccessRule

from spatial import Parcel, HazardZone
from rules import (
    AssessmentRule,
    RuleResult,
    MinimumAreaRule,
    AllowedZoneRule,
    NoHazardOverlapRule,
)


def test_assessment_rule_cannot_be_instantiated():
    with pytest.raises(TypeError):
        AssessmentRule("Example rule")


@pytest.mark.parametrize(
    "area_sqm, expected",
    [
        (6000, True),
        (5000, True),
        (4000, False),
    ],
)
def test_minimum_area_rule(area_sqm, expected):
    parcel = Parcel(
        "P-001",
        box(0, 0, 100, 100),
        "Residential",
        area_sqm,
    )
    rule = MinimumAreaRule(5000)

    result = rule.evaluate(parcel)

    assert isinstance(result, RuleResult)
    assert result.rule_name == rule.name
    assert result.passed is expected
    assert result.message


@pytest.mark.parametrize(
    "zone, expected",
    [
        ("Residential", True),
        ("Commercial", True),
        ("Industrial", False),
    ],
)
def test_allowed_zone_rule(zone, expected):
    parcel = Parcel("P-001", box(0, 0, 10, 10), zone, 100)
    rule = AllowedZoneRule({"Residential", "Commercial"})

    result = rule.evaluate(parcel)

    assert isinstance(result, RuleResult)
    assert result.rule_name == rule.name
    assert result.passed is expected
    assert result.message


@pytest.mark.parametrize(
    "hazard_bounds, expected",
    [
        ((5, 5, 15, 15), False),
        ((20, 20, 30, 30), True),
    ],
)
def test_no_hazard_overlap_rule(hazard_bounds, expected):
    parcel = Parcel(
        "P-001",
        box(0, 0, 10, 10),
        "Residential",
        100,
    )
    hazard = HazardZone(
        "HZ-01",
        box(*hazard_bounds),
        "Flood",
        "High",
    )
    rule = NoHazardOverlapRule(hazard)

    result = rule.evaluate(parcel)

    assert isinstance(result, RuleResult)
    assert result.rule_name == rule.name
    assert result.passed is expected
    assert result.message

@pytest.mark.parametrize(
    "max_distance, expected",
    [
        (15, True),
        (10, True),
        (5, False),
    ],
)
def test_road_access_rule(max_distance, expected):
    parcel = Parcel(
        "P-001",
        box(0, 0, 10, 10),
        "Residential",
        100,
    )
    road = Road(
        "R-001",
        LineString([(20, 0), (20, 10)]),
    )
    rule = RoadAccessRule(road, max_distance)

    result = rule.evaluate(parcel)

    assert isinstance(result, RuleResult)
    assert result.rule_name == rule.name
    assert result.passed is expected
    assert result.message