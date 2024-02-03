import asyncio
from magicalapi.client import AsyncClient
from magicalapi.types.base import ErrorResponse

API_KEY = "mag_1234567890"
search_sentence = "github copilot"
country = "1"
language = "1000"


async def main():
    async with AsyncClient(api_key=API_KEY) as client:
        keywords_response = await client.youtube_top_keywords.get_keywords(
            search_sentence=search_sentence,
            country=country,
            language=language,
        )
        if type(keywords_response) == ErrorResponse:
            # got error from api
            print("Error :", keywords_response.message)
        else:
            # got response successfully
            print("credists :", keywords_response.usage.credits)
            print("keywords count :", len(keywords_response.data.keywords))

            # save response in json file
            with open("keywords_response.json", "w") as file:
                file.write(keywords_response.model_dump_json(indent=3))


asyncio.run(main())
