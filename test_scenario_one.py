import requests
import json
import jsonpath
import pytest

from test_data import BASE_URL

path = "/patients/identifier"


@pytest.mark.parametrize(
    "name,dob,gender,expected_id",
    [
        ("Virat Kohli", "1988-12-21", "Male", "VIKO1988M"),
        ("Jane Janet Doe", "2021-01-20", "Female", "JAJADO2021F"),
        ("John", "1997-01-20", "Male", "JO1997M"),
    ],
)
def test_get_patient_identifier_when_all_params_valid(name, dob, gender, expected_id):
    # arrange
    uri = BASE_URL + path + "?name=" + name + "&dob=" + dob + "&gender=" + gender

    # act
    response = requests.get(url=uri)
    response_json = json.loads(response.text)

    # assert
    assert response.status_code == 200
    assert jsonpath.jsonpath(response_json, "$.identifier")
    assert jsonpath.jsonpath(response_json, "$.identifier")[0] == expected_id


@pytest.mark.parametrize(
    "name,dob,gender,expected_error_code",
    [
        ("", "2021-01-20", "Female", 400),
        (" ", "2021-01-20", "Female", 400),
        ("Virat Kohli", "", "Female", 400),
        ("Virat Kohli", "2021-01-20", "", 400),
        ("", "", "", 400),
    ],
)
def test_get_patient_identifier_when_atleast_one_input_invalid(
    name, dob, gender, expected_error_code
):
    # arrange
    uri = BASE_URL + path + "?name=" + name + "&dob=" + dob + "&gender=" + gender

    # act
    response = requests.get(url=uri)

    # assert
    assert response.status_code == expected_error_code


def test_get_patient_identifier_when_no_inputs():

    # arrange
    uri = BASE_URL + path

    # act
    response = requests.get(url=uri)

    # assert
    assert response.status_code == 400