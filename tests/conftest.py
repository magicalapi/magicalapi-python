import datetime
from random import choice, randint

import pytest
from faker import Faker

Faker.seed()


@pytest.fixture(scope="function")
def resume_data():
    # sample data of resume parser service

    fake = Faker(locale="en")
    _location = fake.location_on_land()
    resume_parser_data = {
        "basic": {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "phone_number": fake.phone_number(),
            "location": f"{_location[2]}, {_location[3]}",
            "portfolio_website_url": fake.uri(),
            "linkedin_url": fake.uri(),
            "github_url": fake.uri(),
            "university": fake.company(),
            "graduation_year": fake.date_object().strftime("%m/%Y"),
            "majors": fake.text(max_nb_chars=50),
            "birthday": fake.text(max_nb_chars=50),
        },
        "summary": fake.text(),
        "project_experiences": [{"title": fake.text(), "description": fake.text()}],
        "work_experiences": [
            {
                "title": fake.text(max_nb_chars=100),
                "company": fake.company(),
                "location": f"{_location[2]}, {_location[3]}",
                "duration": {
                    "years": randint(0, 10),
                    "months": randint(0, 12),
                },
                "summary": fake.text(),
            },
        ],
        "educations": [
            {
                "school": fake.company(),
                "degree": fake.text(max_nb_chars=20),
                "field": fake.text(max_nb_chars=40),
                "start": {
                    "year": randint(1990, datetime.date.today().year),
                },
                "end": {
                    "year": choice(
                        (
                            "present",
                            randint(1990, datetime.date.today().year),
                        )
                    ),
                },
            },
        ],
        "certifications": [
            {
                "title": fake.text(max_nb_chars=100),
                "provider": fake.text(),
            }
        ],
        "languages": [
            {"name": "English"},
        ],
        "skills": [
            {"name": "Python"},
        ],
        "interests": [{"name": fake.text()} for _ in range(randint(1, 5))],
    }
    yield resume_parser_data

    del resume_parser_data
