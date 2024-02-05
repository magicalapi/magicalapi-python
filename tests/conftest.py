import random
import pytest
from faker import Faker
from random import choice, randint

Faker.seed()


@pytest.fixture(scope="function")
def youtube_keyword():
    # create a sample profile data dictionary
    fake = Faker(locale="en")
    MONTH_LIST = [
        "JANUARY",
        "FEBRUARY",
        "MARCH",
        "APRIL",
        "MAY",
        "JUNE",
        "JULY",
        "AUGUST",
        "SEPTEMBER",
        "OCTOBER",
        "NOVEMBER",
        "DECEMBER",
    ]
    keyword = {
        "keyword": fake.text(max_nb_chars=15),
        "search_volume": randint(1000, 1000000),
        "competition": choice(("LOW", "MEDIUM", "HIGH")),
        "competition_index": randint(0, 100),
        "low_top_of_page_bid_micros": randint(0, 10**7),
        "high_top_of_page_bid_micros": randint(0, 10**7),
        "average_cpc": f"${random.random()}",
        "monthly_search": [
            {
                "month": month,
                "year": randint(2000, 2023),
                "monthly_searches": randint(1000, 1000000),
            }
            for month in MONTH_LIST
        ],
    }

    yield keyword
    del keyword


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
        },
        "summary": fake.text(),
        "work_experiences": [
            {
                "title": fake.text(max_nb_chars=100),
                "company": fake.company(),
                "location": f"{_location[2]}, {_location[3]}",
                "duration": fake.date_object().strftime("%m/%Y")
                + " - "
                + fake.date_object().strftime("%m/%Y"),
                "summary": fake.text(),
            },
        ],
        "educations": [
            {
                "school": fake.company(),
                "degree": fake.text(max_nb_chars=20),
                "field": fake.text(max_nb_chars=40),
                "start": fake.date_object().strftime("%m/%Y"),
                "end": "present",
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
    }
    yield resume_parser_data

    del resume_parser_data
