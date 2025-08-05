from datetime import date
from random import choice, randint
from typing import Any

import pytest
from faker import Faker
from pydantic import ValidationError

from magicalapi.types.profile_data import (
    Profile,
    ProfileDataResponse,
)


@pytest.fixture()
def profile_data():
    # create a sample profile data dictionary
    fake = Faker(locale="en_US")
    _username = fake.user_name()
    _start_date = fake.date_object()
    _end_date = fake.date_between_dates(_start_date, date.today())
    profile = {
        "url": f"https://linkedin.com/in/{_username}/",
        "profile": _username,
        "crawled_at": fake.date_time_this_year().strftime("%d/%m/%Y %H:%M:%S"),
        "name": fake.name(),
        "description": "",  # empty text
        "location": "{}, {}".format(*fake.location_on_land()[2:4]),
        "followers": f"{randint(1,500)} followers",
        "connections": f"{randint(1,500)} connections",
        "experience": [
            {
                "image_url": fake.uri(),
                "title": fake.job(),
                "company_name": fake.company(),
                "company_link": fake.uri(),
                "date": {
                    "start_date": _start_date.strftime("%b %Y"),
                    "end_date": _end_date.strftime("%b %Y"),
                    "duration": {"years": randint(0, 10), "months": randint(1, 12)},
                },
                "location": "{}, {}".format(*fake.location_on_land()[2:4]),
                "description": fake.text(),
            },
            # empty dates
            {
                "image_url": fake.uri(),
                "title": fake.job(),
                "company_name": fake.company(),
                "company_link": fake.uri(),
                "date": {
                    "start_date": _start_date.strftime("%b %Y"),
                    "end_date": "",
                    "duration": {"years": randint(0, 10), "months": randint(1, 12)},
                },
                "location": "",  # test convert empty string to None
                "description": fake.text(),
            },
        ],
        "education": [
            {
                "image_url": fake.uri(),
                "university_name": fake.company(),
                "university_link": fake.uri(),
                "degree": fake.text(max_nb_chars=20),
                "major": fake.text(max_nb_chars=20),
                "date": {
                    "start_date": _start_date.strftime("%Y"),
                    "end_date": _end_date.strftime("%Y"),
                },
            },
            # empty dates
            {
                "image_url": fake.uri(),
                "university_name": fake.company(),
                "university_link": fake.uri(),
                "degree": fake.text(max_nb_chars=20),
                "major": fake.text(max_nb_chars=20),
                "date": {
                    "start_date": _start_date.strftime("%Y"),
                    "end_date": "",
                },
            },
        ],
        "certifications": [
            {
                "image_url": fake.uri(),
                "title": fake.name(),
                "course_link": fake.uri(),
                "issuer": fake.company(),
                "credential": fake.text(max_nb_chars=20),
                "issued_date": _start_date.strftime("%b %Y"),
            },
            # empty data
            {
                "image_url": fake.uri(),
                "title": fake.name(),
                "course_link": fake.uri(),
                "issuer": fake.company(),
                "credential": fake.text(max_nb_chars=20),
                "issued_date": "",
            },
        ],
        "languages": [
            {
                "name": choice(("English", "Spanish", "Kurdish", "Arabic")),
                "description": fake.text(),
            },
            # empty data
            {
                "name": choice(("English", "Spanish", "Kurdish", "Arabic")),
                "description": "",
            },
        ],
        "volunteerings": [
            {
                "role": "Volunteer/Member",
                "organization": fake.company(),
                "volunteering_link": fake.uri(),
                "date": {
                    "start_date": _start_date.strftime("%b %Y"),
                    "end_date": _end_date.strftime("%b %Y"),
                    "duration": {"years": randint(0, 10), "months": randint(1, 12)},
                },
                "cause": fake.text(max_nb_chars=25),
                "description": fake.text(),
            },
            # empty date
            {
                "role": "Volunteer/Member",
                "organization": fake.company(),
                "volunteering_link": fake.uri(),
                "date": "",
                "cause": fake.text(max_nb_chars=25),
                "description": "",
            },
        ],
        "publications": [
            {
                "title": fake.name(),
                "publisher": fake.company(),
                "publication_link": fake.uri(),
                "publication_date": _start_date.strftime("%b %Y"),
                "description": fake.text(),
            },
            # empty date
            {
                "title": fake.name(),
                "publisher": fake.company(),
                "publication_link": fake.uri(),
                "publication_date": "",
                "description": "",
            },
        ],
        "projects": [
            {
                "name": fake.name(),
                "date": {
                    "start_date": _start_date.strftime("%b %Y"),
                    "end_date": _end_date.strftime("%b %Y"),
                },
                "description": fake.text(),
            },
            # empty date
            {
                "name": fake.name(),
                "date": "",
                "description": "",
            },
        ],
        "courses": [
            {"name": fake.text(max_nb_chars=25), "number": str(randint(1, 20))},
            # empty
            {"name": fake.text(max_nb_chars=25), "number": ""},
        ],
        "honors_and_awards": [
            {
                "title": fake.name(),
                "issuer": fake.company(),
                "issued_date": _start_date.strftime("%b %Y"),
                "description": fake.text(),
            },
            # empty date
            {
                "title": fake.name(),
                "issuer": fake.company(),
                "issued_date": "",
                "description": "",
            },
        ],
        #
        "activities": [
            {
                "title": fake.text(max_nb_chars=50),
                "subtitle": fake.text(max_nb_chars=30),
                "image_url": fake.image_url(),
                "link": fake.uri(),
            }
            for _ in range(randint(1, 3))
        ],
        "similar_profiles": [
            {
                "url": f"https://linkedin.com/in/{fake.user_name()}/",
                "name": fake.name(),
                "title": fake.job(),
                "image_url": fake.image_url(),
            }
            for _ in range(randint(1, 5))
        ],
        "patents": [
            {
                "title": fake.text(max_nb_chars=100),
                "patent_id": f"US{randint(1000000, 9999999)}",
                "link": f"https://patents.google.com/patent/US{randint(1000000, 9999999)}",
            }
            for _ in range(randint(0, 2))
        ],
    }

    yield profile
    del profile


@pytest.mark.dependency()
def test_profile_data_type(profile_data: dict[str, Any]):
    # check profile data validated successfull
    try:
        Profile.model_validate(profile_data)
    except ValidationError as exc:
        assert False, "validating profile data failed : " + str(exc)


@pytest.mark.dependency()
def test_profile_data_type_failing(profile_data: dict[str, Any]):
    # validating profile data must fail
    profile_data["experience"][0]["date"]["start_date"] = "none"
    del profile_data["education"][0]["date"]
    del profile_data["projects"][0]["date"]["end_date"]
    profile_data["publications"][0]["publication_date"] = 12
    profile_data["honors_and_awards"][0]["issued_date"] = None
    try:
        Profile.model_validate(profile_data)
    except:
        pass
    else:
        # if raised no error, the test failed
        assert False, "validating profile_data types must failed but it did not !"


@pytest.mark.dependency(
    depends=["test_profile_data_type", "test_profile_data_type_failing"]
)
def test_profile_data_response_type(profile_data: dict[str, Any]):
    try:
        response_schema = {
            "data": profile_data,
            "usage": {"credits": randint(1, 200)},
        }
        ProfileDataResponse.model_validate(response_schema)

    except ValidationError as exc:
        assert False, "validating profile_data response failed : " + str(exc)
