class Auth:
    id: str
    key_hash: str
    auth_level: int
    portal_username: str
    portal_password_hash: str | None

    def __init__(
        self,
        id: str,
        key_hash: str,
        auth_level: int,
        portal_username: str,
        portal_password_hash: str | None = None,
    ):
        self.id = id
        self.key_hash = key_hash
        self.auth_level = auth_level
        self.portal_username = portal_username
        self.portal_password_hash = portal_password_hash

    @classmethod
    def from_dict(cls, dict: dict):
        return cls(**dict)

    def to_dict(self):
        return {
            "id": self.id,
            "auth_level": self.auth_level,
            "portal_username": self.portal_username,
            "portal_password_hash": self.portal_password_hash,
        }


class Event:
    id: str
    org_id: str
    title: str
    subtitle: str | None
    description: str | None
    image: str | None
    address_street: str
    address_city: str
    address_state: str
    address_zip: str
    coords_lat: float
    coords_lon: float
    start_time: int
    end_time: int | None

    def __init__(
        self,
        id: str,
        org_id: str,
        title: str,
        address_street: str,
        address_city: str,
        address_state: str,
        address_zip: str,
        coords_lat: float,
        coords_lon: float,
        start_time: int,
        subtitle: str | None = "",
        description: str | None = "",
        image: str | None = "",
        end_time: int | None = "",
    ):
        self.id = id
        self.org_id = org_id
        self.title = title
        self.address_street = address_street
        self.address_city = address_city
        self.address_state = address_state
        self.address_zip = address_zip
        self.coords_lat = coords_lat
        self.coords_lon = coords_lon
        self.start_time = start_time
        self.subtitle = subtitle
        self.description = description
        self.image = image
        self.end_time = end_time

    @classmethod
    def from_dict(cls, dict: dict):
        return cls(**dict)

    def to_dict(self):
        return {
            "id": self.id,
            "org_id": self.org_id,
            "title": self.title,
            "address_street": self.address_street,
            "address_city": self.address_city,
            "address_state": self.address_state,
            "address_zip": self.address_zip,
            "coords_lat": self.coords_lat,
            "coords_lon": self.coords_lon,
            "start_time": self.start_time,
            "subtitle": self.subtitle,
            "description": self.description,
            "image": self.image,
            "end_time": self.end_time,
        }
