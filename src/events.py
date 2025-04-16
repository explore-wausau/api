from flask import request
from utils import supabase, create_error_msg, get_auth, hash_string


def list_events():
    query = supabase.table("events").select().execute()

    if len(query.data) >= 1:
        return query.data
    else:
        return create_error_msg("No events were found.")


def search_events():
    id = request.args.get("id")
    title = request.args.get("title")
    org_id = request.args.get("org_id")

    if id is None and title is None and org_id is None:
        return create_error_msg("Please provide at least one parameter.")

    query = supabase.table("events").select()
    if id:
        query = query.eq("id", id)
    if title:
        query = query.eq("title", title)
    if org_id:
        query = query.eq("org_id", org_id)
    query = query.execute()

    if len(query.data) >= 1:
        return query.data
    else:
        return create_error_msg("No events were found.")


def create_event():
    id = request.args.get("id")
    title = request.args.get("title")
    subtitle = request.args.get("subtitle")  # optional
    description = request.args.get("description")  # optional
    image = request.args.get("image")  # optional
    address_street = request.args.get("address_street")
    address_city = request.args.get("address_city")
    address_state = request.args.get("address_state")
    address_zip = request.args.get("address_zip")
    coords_lat = request.args.get("coords_lat")
    coords_lon = request.args.get("coords_lon")
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")  # optional

    key = request.headers.get("key")

    if key is None:
        return create_error_msg("Please provide an API key with authentication level 1 or higher.")

    if (
        id is None
        or title is None
        or address_street is None
        or address_city is None
        or address_state is None
        or address_zip is None
        or coords_lat is None
        or coords_lon is None
        or start_time is None
    ):
        return create_error_msg("Please provide all required parameters.")
    
    auth = get_auth(key)

    if auth and auth.auth_level >= 1:
        query = (
            supabase.table("events")
            .insert({
                "id": auth.id + "." + id,
                "org_id": auth.id,
                "title": title,
                "subtitle": subtitle,
                "description": description,
                "image": image,
                "address_street": address_street,
                "address_city": address_city,
                "address_state": address_state,
                "address_zip": address_zip,
                "coords_lat": coords_lat,
                "coords_lon": coords_lon,
                "start_time": start_time,
                "end_time": end_time
            })
            .execute()
        )

        return query.data[0]
    else:
        return create_error_msg("Authentication is not valid. Please provide an API key with authentication level 1 or higher.")


# TODO: Modify event
