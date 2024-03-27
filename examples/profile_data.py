import asyncio

from magicalapi.client import AsyncClient
from magicalapi.errors import APIServerError, APIServerTimedout
from magicalapi.types.base import ErrorResponse

profile_name = "conanobrien"
output_file_name = f"profile_data_{profile_name}.json"


async def main():
    try:
        # the api_key will load from the .env file
        async with AsyncClient() as client:
            response = await client.profile_data.get_profile_data(
                profile_name=profile_name
            )

            if isinstance(response, ErrorResponse):
                # got error from api
                print("Error:", response.message)
            else:
                print("Credits:", response.usage.credits)
                print(response.data)
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
