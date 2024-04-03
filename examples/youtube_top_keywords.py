import asyncio

from magicalapi.client import AsyncClient
from magicalapi.errors import APIServerError, APIServerTimedout
from magicalapi.types.base import ErrorResponse

search_sentence = "movie trailers"
country = "1"
language = "1000"
output_file_name = f"youtube_top_keywords_{search_sentence}.json"


async def main():
    try:
        # the api_key will load from the .env file
        async with AsyncClient() as client:
            # get languages and countries list
            # languages = await client.youtube_top_keywords.get_languages()
            # countries = await client.youtube_top_keywords.get_countries()
            # print("Languauges :")
            # print(languages)
            # print("Countries : ")
            # print(countries)

            # get youtube keywords
            response = await client.youtube_top_keywords.get_keywords(
                search_sentence=search_sentence,
                country=country,
                language=language,
            )
            if isinstance(response, ErrorResponse):
                # got error from api
                print("Error :", response.message)
            else:
                # got response successfully
                print("credists :", response.usage.credits)
                print("keywords count :", len(response.data.keywords))

                # save response in json file
                with open(output_file_name, "w") as file:
                    file.write(response.model_dump_json(indent=3))

                print(f"response saved to {output_file_name}")
    except (APIServerError, APIServerTimedout) as e:
        # handling server errors
        print(e)
    except Exception as e:
        print("An error occurred:", str(e))


asyncio.run(main())
