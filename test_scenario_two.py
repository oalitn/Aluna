import requests
import json
import jsonpath
import pytest

from test_data import (
    EXISTING_PATIENT_IDs,
    VALID_PATIENT_IDs,
    INVALID_PATIENT_IDs,
    BASE_URL,
)

path = "/identity"

# Tests the POST /identity API call
# Checks whether the api responds with Bad Request (400) if the identifier passed is invalid
@pytest.mark.parametrize("id", INVALID_PATIENT_IDs)
def test_create_identifier_invalid_input(id):
    uri = BASE_URL + path
    body = {"identifier": id}

    post_response = requests.post(
        url=uri, data=json.dumps(body), headers={"Content-Type": "application/json"}
    )
    post_response_json = post_response.json()

    assert post_response.status_code == 400
    assert jsonpath.jsonpath(post_response_json, "$.error")
    assert jsonpath.jsonpath(post_response_json, "$.error")[0] == "Invalid input"


# Tests the GET /identity API call
# Checks whether the api responds with Bad Request (400) if the identifier passed is invalid
@pytest.mark.parametrize("id", INVALID_PATIENT_IDs)
def get_user_invalid_input(id):
    uri = BASE_URL + path
    data = {"identifier": id}

    get_response = requests.get(url=uri, params=data)
    get_response_json = get_response.json()

    assert get_response.status_code == 400

    assert jsonpath.jsonpath(get_response_json, "$.error")
    assert jsonpath.jsonpath(get_response_json, "$.error")[0] == "Invalid input"


# Tests POST and GET /identifer api call with a valid input
# Verifies the responses when user are passed in the apis
@pytest.mark.parametrize("id", VALID_PATIENT_IDs)
def test_create_identifier_get_user_valid_input(id):
    uri = BASE_URL + path
    data = {"identifier": id}

    post_response = requests.post(
        url=uri, data=json.dumps(data), headers={"Content-Type": "application/json"}
    )
    post_response_json = post_response.json()

    get_response = requests.get(url=uri, params=data)
    get_response_json = get_response.json()

    assert post_response.status_code == 200
    assert post_response_json == "{}"

    assert get_response.status_code == 200
    assert jsonpath.jsonpath(get_response_json, "$.name")
    assert jsonpath.jsonpath(get_response_json, "$.dob")
    assert jsonpath.jsonpath(get_response_json, "$.gender")


@pytest.mark.parametrize("id", EXISTING_PATIENT_IDs)
def test_create_identifier_record_exists(id):
    uri = BASE_URL + path
    data = {"identifier": id}

    post_response = requests.post(
        url=uri, data=json.dumps(data), headers={"Content-Type": "application/json"}
    )
    post_response_json = post_response.json()

    get_response = requests.get(url=uri, params=data)
    get_response_json = get_response.json()

    assert post_response.status_code == 409
    assert jsonpath.jsonpath(post_response_json, "$.error")
    assert (
        jsonpath.jsonpath(post_response_json, "$.error")[0]
        == "The record already exists"
    )

    assert get_response.status_code == 200
    assert jsonpath.jsonpath(get_response_json, "$.name")
    assert jsonpath.jsonpath(get_response_json, "$.dob")
    assert jsonpath.jsonpath(get_response_json, "$.gender")