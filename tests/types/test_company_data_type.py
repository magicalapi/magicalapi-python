from datetime import date
from random import randint
from typing import Any

import pytest
from faker import Faker
from pydantic import ValidationError

from magicalapi.types.company_data import Company, CompanyDataResponse


@pytest.fixture()
def company_data():
    # create a sample company data dictionary
    Faker.seed()
    fake = Faker(locale="en_US")
    _username = fake.user_name()
    _today = date.today()
    company = {
        "url": f"https://linkedin.com/in/{_username}/",
        "company_name": _username,
        "crawled_at": fake.date_time_this_year().strftime("%d/%m/%Y %H:%M:%S"),
        "name": fake.company(),
        "tagline": None,  # test null
        "cover_image_url": fake.uri(),
        "logo_url": fake.uri(),
        "employees": f"{randint(10,1000)} employees",
        "followers": f"{randint(1,500)} followers",
        "about": fake.text(),
        # features
        "website": fake.uri(),
        "industry": fake.text(max_nb_chars=40),
        "size": f"{randint(10,1000)}+ employees",
        "headquarters": fake.text(max_nb_chars=20),
        "organizationType": fake.text(max_nb_chars=20),
        "foundedOn": str(randint(_today.year - 50, _today.year + 50)),
        "specialties": ", ".join([fake.text(max_nb_chars=10) for _ in range(5)]),
        #
        "locations": [
            [fake.location_on_land()[2], fake.location_on_land()[4]]
            for _ in range(randint(1, 5))
        ],
        "products": [
            {
                "name": fake.text(),
                "link": fake.uri(),
                "url": fake.uri(),
                "about": fake.text(max_nb_chars=20),
                "used_for": [fake.text()],
                "customers": [fake.uri()],
            }
        ],
    }

    yield company
    del company


@pytest.mark.dependency()
def test_company_data_type(company_data: dict[str, Any]):
    # check company data validated successfull
    try:
        Company.model_validate(company_data)
    except ValidationError as exc:
        assert False, "validating company data failed : " + str(exc)


@pytest.mark.dependency()
def test_company_data_type_failing(company_data: dict[str, Any]):
    # validating company data must fail
    company_data["url"] = "none"
    del company_data["tagline"]
    company_data["products"][0]["name"] = 12
    try:
        Company.model_validate(company_data)
    except:
        pass
    else:
        # if raised no error, the test failed
        assert False, "validating company_data types must failed but it did not !"


@pytest.mark.dependency(
    depends=["test_company_data_type", "test_company_data_type_failing"]
)
def test_company_data_response_type(company_data: dict[str, Any]):
    try:
        response_schema = {
            "data": company_data,
            "usage": {"credits": randint(1, 200)},
        }
        CompanyDataResponse.model_validate(response_schema)

    except ValidationError as exc:
        assert False, "validating company_data response failed : " + str(exc)
