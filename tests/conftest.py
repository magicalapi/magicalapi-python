import random
import pytest
from faker import Faker
from random import choice, randint


@pytest.fixture()
def dependency_keyword():
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
