import pytest
from shapely.geometry import box

from spatial import Parcel, HazardZone


@pytest.mark.parametrize(
    "parcel_id, zone, area_sqm",
    [
        ("", "Residential", 100),
        ("P-001", "", 100),
        ("P-001", "Residential", 0),
        ("P-001", "Residential", -100),
    ],
)
def test_parcel_rejects_invalid_inputs(parcel_id, zone, area_sqm):
    with pytest.raises(ValueError):
        Parcel(parcel_id, box(0, 0, 10, 10), zone, area_sqm)


def test_parcel_exposes_valid_state():
    geometry = box(0, 0, 10, 10)
    parcel = Parcel("P-001", geometry, "Residential", 100)

    assert parcel.parcel_id == "P-001"
    assert parcel.geometry is geometry
    assert parcel.zone == "Residential"
    assert parcel.area_sqm == 100.0


def test_parcel_area_property_is_read_only():
    parcel = Parcel("P-001", box(0, 0, 10, 10), "Residential", 100)

    with pytest.raises(AttributeError):
        parcel.area_sqm = -100


def test_parcel_intersects_overlapping_hazard():
    parcel = Parcel("P-001", box(0, 0, 10, 10), "Residential", 100)
    hazard = HazardZone(
        "HZ-01",
        box(5, 5, 15, 15),
        "Flood",
        "High",
    )

    assert parcel.intersects(hazard) is True


def test_parcel_does_not_intersect_distant_hazard():
    parcel = Parcel("P-001", box(0, 0, 10, 10), "Residential", 100)
    hazard = HazardZone(
        "HZ-01",
        box(20, 20, 30, 30),
        "Flood",
        "High",
    )

    assert parcel.intersects(hazard) is False