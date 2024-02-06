import asyncio
from magicalapi.client import AsyncClient
from magicalapi.types.base import ErrorResponse


prompt_sentence = "how get more views in youtube ?"
count = 10
suggestion_goal = "hashtag"
output_file_name = "youtube_suggestions.json"


async def main():
    # api_key will load from .env
    async with AsyncClient() as client:
        response = await client.youtube_suggestions.get_youtube_suggestions(
            prompt_sentence=prompt_sentence,
            count=count,
            suggestion_goal=suggestion_goal,
        )

        if type(response) == ErrorResponse:
            # got error from api
            print("Error :", response.message)
        else:
            # got response successfully
            print("credists :", response.usage.credits)
            # save response in json file
            with open(output_file_name, "w") as file:
                file.write(response.model_dump_json(indent=3))

            print(f"response saveed on {output_file_name}")


asyncio.run(main())
