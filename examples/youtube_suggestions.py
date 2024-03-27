import asyncio

from magicalapi.client import AsyncClient
from magicalapi.errors import APIServerError, APIServerTimedout
from magicalapi.types.base import ErrorResponse

prompt_sentence = "how get more views in youtube ?"
count = 10
suggestion_goal = "hashtag"
output_file_name = "youtube_suggestions.json"


async def main():
    try:
        # the api_key will load from the .env file
        async with AsyncClient() as client:
            response = await client.youtube_suggestions.get_youtube_suggestions(
                prompt_sentence=prompt_sentence,
                count=count,
                suggestion_goal=suggestion_goal,
            )

            if isinstance(response, ErrorResponse):
                # got error from api
                print("Error :", response.message)
            else:
                # got response successfully
                print("credists :", response.usage.credits)
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
