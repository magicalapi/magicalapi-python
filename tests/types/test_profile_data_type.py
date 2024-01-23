from datetime import date
from random import choice, randint
import pytest
from faker import Faker
from pydantic import ValidationError
from magicalapi.types.base import Usage

from magicalapi.types.profile_data import (
    Certification,
    Course,
    Education,
    Experience,
    HonorAndAward,
    Language,
    Profile,
    ProfileDataResponse,
    Project,
    Publication,
    Volunteering,
)


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
def test_experience_type(dependency_profile_data):
    # check experienc from profile data validated successfull
    try:
        Experience.model_validate(dependency_profile_data["experience"][0])
    except ValidationError as exc:
        assert False, "validating experience failed : " + str(exc)


@pytest.mark.dependency()
def test_education_type(dependency_profile_data):
    # check education from profile data validated successfull
    try:
        Education.model_validate(dependency_profile_data["education"][0])
    except ValidationError as exc:
        assert False, "validating education failed : " + str(exc)


@pytest.mark.dependency()
def test_certification_type(dependency_profile_data):
    # check certification from profile data validated successfull
    try:
        Certification.model_validate(dependency_profile_data["certifications"][0])
    except ValidationError as exc:
        assert False, "validating certification failed : " + str(exc)


@pytest.mark.dependency()
def test_language_type(dependency_profile_data):
    # check language from profile data validated successfull
    try:
        Language.model_validate(dependency_profile_data["languages"][0])
    except ValidationError as exc:
        assert False, "validating language failed : " + str(exc)


@pytest.mark.dependency()
def test_volunteering_type(dependency_profile_data):
    # check volunteering from profile data validated successfull
    try:
        Volunteering.model_validate(dependency_profile_data["volunteerings"][0])
    except ValidationError as exc:
        assert False, "validating volunteering failed : " + str(exc)


@pytest.mark.dependency()
def test_publication_type(dependency_profile_data):
    # check publication from profile data validated successfull
    try:
        Publication.model_validate(dependency_profile_data["publications"][0])
    except ValidationError as exc:
        assert False, "validating publication failed : " + str(exc)


@pytest.mark.dependency()
def test_project_type(dependency_profile_data):
    # check project from profile data validated successfull
    try:
        Project.model_validate(dependency_profile_data["projects"][0])
    except ValidationError as exc:
        assert False, "validating project failed : " + str(exc)


@pytest.mark.dependency()
def test_course_type(dependency_profile_data):
    # check course from profile data validated successfull
    try:
        Course.model_validate(dependency_profile_data["courses"][0])
    except ValidationError as exc:
        assert False, "validating course failed : " + str(exc)


@pytest.mark.dependency()
def test_honors_and_award_type(dependency_profile_data):
    # check honors_and_award from profile data validated successfull
    try:
        HonorAndAward.model_validate(dependency_profile_data["honors_and_awards"][0])
    except ValidationError as exc:
        assert False, "validating honors_and_award failed : " + str(exc)


@pytest.mark.dependency(
    depends=[
        "test_experience_type",
        "test_education_type",
        "test_certification_type",
        "test_language_type",
        "test_volunteering_type",
        "test_publication_type",
        "test_project_type",
        "test_course_type",
        "test_honors_and_award_type",
    ]
)
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
    del dependency_profile_data["education"][0]["date"]
    del dependency_profile_data["projects"][0]["date"]["end_date"]
    dependency_profile_data["publications"][0]["publication_date"] = 12
    dependency_profile_data["honors_and_awards"][0]["issued_date"] = None
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
