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
                "description": fake,
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


def test_profile_data_type(dependency_profile_data):
    with pytest.raises(ValidationError) as excinfo:
        Profile.model_validate(dependency_profile_data)


def test_profile_data_response_type(dependency_profile_data):
    with pytest.raises(ValidationError) as excinfo:
        ProfileDataResponse(
            data=Profile.model_validate(dependency_profile_data),
            usage=Usage(credits=randint(1, 200)),
        )
