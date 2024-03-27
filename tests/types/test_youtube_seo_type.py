from random import choice, randint
from uuid import uuid4

import pytest
from faker import Faker
from pydantic import ValidationError

from magicalapi.types.youtube_seo import YoutubeSeoResponse

Faker.seed()


@pytest.fixture(scope="function")
def youtube_seo_data():  # type: ignore
    # test data for youtube seo
    fake = Faker(locale="en")
    _video_id = str(uuid4())
    youtube_seo = {  # type: ignore
        "score": 41,
        "good": {
            "video_quality": [
                "The video is of the highest quality, ensuring a better viewer experience."
            ],
            "thumbnail": [
                "The thumbnail image is of superb quality, attracting more views."
            ],
        },
        "bad": {
            "title": [
                "Title not repeated in video caption.\n<b>Tip:</b> Repeat the video title in the caption for reinforcement and better search indexing.\n"
            ],
            "description": [
                "Caption length outside 4000-5000 characters.\n<b>Tip:</b> Keep the caption between 4000 to 5000 characters to provide detailed context and keywords.\n",
                "Absence of suggested video links.\n<b>Tip:</b> Include links to other relevant videos to increase viewership and channel retention.\n",
                "Missing timestamps.\n<b>Tip:</b> Add timestamps for key segments to enhance viewer experience and retention.\n",
            ],
            "tags": [
                "Tags length outside 450-500 characters.\n<b>Tip:</b> Ensure your video tags are between 450 to 500 characters to maximize keyword coverage.\n"
            ],
            "hashtags": [
                "No hashtags in caption.\n<b>Tip:</b> Use relevant hashtags to improve discover ability in searches and on social platforms.\n",
                "Incorrect number of hashtags.\n<b>Tip:</b> Utilize 3 to 5 hashtags to balance discover ability without appearing spammy.\n",
            ],
        },
        "details": {
            "kind": "youtube#videoListResponse",
            "etag": "dKkUgpwMfKcMUUXnKYiyXvsCcAA",
            "items": [
                {
                    "kind": "youtube#video",
                    "etag": str(uuid4()),
                    "id": _video_id,
                    "snippet": {
                        "publishedAt": fake.date_time_this_year().strftime("%FT%TZ"),
                        "channelId": str(uuid4()),
                        "title": fake.text(max_nb_chars=100),
                        "description": fake.text(),
                        "thumbnails": {
                            "default": {
                                "url": f"https://i.ytimg.com/vi/{_video_id}/mqdefault.jpg",
                                "width": 120,
                                "height": 90,
                            },
                            "medium": {
                                "url": f"https://i.ytimg.com/vi/{_video_id}/mqdefault.jpg",
                                "width": 320,
                                "height": 180,
                            },
                            "high": {
                                "url": f"https://i.ytimg.com/vi/{_video_id}/hqdefault.jpg",
                                "width": 480,
                                "height": 360,
                            },
                        },
                        "channelTitle": fake.name(),
                        "categoryId": str(randint(1, 40)),
                        "liveBroadcastContent": "none",
                        "defaultLanguage": "en",
                        "localized": {
                            "title": fake.text(max_nb_chars=100),
                            "description": fake.text(),
                        },
                        "defaultAudioLanguage": "en",
                        "tags": [fake.text(max_nb_chars=10) for _ in range(1, 5)],
                    },
                    "contentDetails": {
                        "duration": f"PT{randint(0,59)}M{randint(0,59)}S",
                        "dimension": "2d",
                        "definition": choice(("hd", "sd")),
                        "caption": choice(("true", "false")),
                        "licensedContent": choice((True, False)),
                        "projection": "rectangular",
                    },
                    "status": {
                        "uploadStatus": "processed",
                        "privacyStatus": "public",
                        "license": "youtube",
                        "embeddable": choice((True, False)),
                        "publicStatsViewable": choice((True, False)),
                        "madeForKids": choice((True, False)),
                    },
                    "statistics": {
                        "viewCount": str(randint(1, 1000000)),
                        "likeCount": str(randint(1, 1000000)),
                        "favoriteCount": str(randint(1, 1000000)),
                        # "commentCount": str(randint(1, 1000000)),
                        "commentCount": None,  # test no comment count
                    },
                }
            ],
            "pageInfo": {"totalResults": 1, "resultsPerPage": 1},
        },
    }

    yield youtube_seo

    del youtube_seo


def test_youtube_seo_validate_type(youtube_seo_data):
    # test validating youtube_seo response type
    response = {"data": youtube_seo_data, "usage": {"credits": randint(10, 500)}}

    assert type(YoutubeSeoResponse.model_validate(response)) == YoutubeSeoResponse


def test_youtube_seo_validate_type_failing(youtube_seo_data):
    # test validating youtube_seo response type must fail
    # make data schema invalid
    del youtube_seo_data["score"]
    youtube_seo_data["details"]["items"] = {}

    response = {"data": youtube_seo_data, "usage": {"credits": randint(10, 500)}}

    with pytest.raises(ValidationError):
        YoutubeSeoResponse.model_validate(response)
