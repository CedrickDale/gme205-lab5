class Parcel:
    def __init__(self, parcel_id, geometry, zone, area_sqm):
        if not parcel_id:
            raise ValueError("parcel_id is required")
        if not zone:
            raise ValueError("zone is required")
        if float(area_sqm) <= 0:
            raise ValueError("area_sqm must be positive")

        self._parcel_id = str(parcel_id)
        self._geometry = geometry
        self._zone = str(zone)
        self._area_sqm = float(area_sqm)

    @property
    def parcel_id(self):
        return self._parcel_id

    @property
    def zone(self):
        return self._zone

    @property
    def area_sqm(self):
        return self._area_sqm

    @property
    def geometry(self):
        return self._geometry

    def intersects(self, other):
        return self._geometry.intersects(other.geometry)


class HazardZone:
    def __init__(self, hazard_id, geometry, hazard_type, severity):
        if not hazard_id:
            raise ValueError("hazard_id is required")
        if not hazard_type:
            raise ValueError("hazard_type is required")
        if not severity:
            raise ValueError("severity is required")

        self._hazard_id = str(hazard_id)
        self._geometry = geometry
        self._hazard_type = str(hazard_type)
        self._severity = str(severity)

    @property
    def hazard_id(self):
        return self._hazard_id

    @property
    def geometry(self):
        return self._geometry

    @property
    def hazard_type(self):
        return self._hazard_type

    @property
    def severity(self):
        return self._severity