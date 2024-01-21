from datetime import date
from random import choice, randint
import pytest
from faker import Faker
from pydantic import ValidationError
from magicalapi.types.base import Usage

from magicalapi.types.profile_data import Profile, ProfileDataResponse


@pytest.fixture()
def dependency_profile_data():
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
        "description": fake.text(),
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
            }
        ],
        "certifications": [
            {
                "image_url": fake.uri(),
                "title": fake.name(),
                "course_link": fake.uri(),
                "issuer": fake.company(),
                "credential": fake.text(max_nb_chars=20),
                "issued_date": _start_date.strftime("%b %Y"),
            }
        ],
        "languages": [
            {
                "name": choice(("English", "Spanish", "Kurdish", "Arabic")),
                "description": fake.text(),
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
            }
        ],
        "publications": [
            {
                "title": fake.name(),
                "publisher": fake.company(),
                "publication_link": fake.uri(),
                "publication_date": _start_date.strftime("%b %Y"),
                "description": fake.text(),
            }
        ],
        "projects": [
            {
                "name": fake.name(),
                "date": {
                    "start_date": _start_date.strftime("%b %Y"),
                    "end_date": _end_date.strftime("%b %Y"),
                },
                "description": fake.text(),
            }
        ],
        "courses": [
            {"name": fake.text(max_nb_chars=25), "number": str(randint(1, 20))},
        ],
        "honors_and_awards": [
            {
                "title": fake.name(),
                "issuer": fake.company(),
                "issued_date": _start_date.strftime("%b %Y"),
                "description": fake.text(),
            }
        ],
    }

    yield profile
    del profile


@pytest.mark.dependency()
def test_profile_data_type(dependency_profile_data):
    # check profile data validated successfull
    try:
        Profile.model_validate(dependency_profile_data)
    except ValidationError as exc:
        assert False, "validating profile data failed : " + str(exc)


@pytest.mark.dependency()
def test_profile_data_type_failing(dependency_profile_data):
    # validating profile data must fail
    dependency_profile_data["experience"][0]["date"]["start_date"] = "none"
    dependency_profile_data["education"][0]["date"]["start"] = "none"
    dependency_profile_data["projects"][0]["date"]["end_date"] = "none"
    dependency_profile_data["publications"][0]["publication_date"] = "none"
    dependency_profile_data["honors_and_awards"][0]["issued_date"] = "none"
    try:
        Profile.model_validate(dependency_profile_data)
    except:
        pass
    else:
        # if raised no error, the test failed
        assert False, "validating profile_data types must failed but it did not !"


@pytest.mark.dependency(
    depends=["test_profile_data_type", "test_profile_data_type_failing"]
)
def test_profile_data_response_type(dependency_profile_data):
    try:
        ProfileDataResponse(
            data=Profile.model_validate(dependency_profile_data),
            usage=Usage(credits=randint(1, 200)),
        )

    except ValidationError as exc:
        assert False, "validating profile_data response failed : " + str(exc)
