import asyncio

from magicalapi.client import AsyncClient
from magicalapi.errors import APIServerError, APIServerTimedout
from magicalapi.types.base import ErrorResponse

company_username = "google"
output_file_name = f"company_data_{company_username}.json"


async def main():
    try:
        # the api_key will load from the .env file
        async with AsyncClient() as client:
            response = await client.company_data.get_company_data(
                company_username=company_username
            )

            if isinstance(response, ErrorResponse):
                # got error from api
                print("Error:", response.message)
            else:
                # got response successfully
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
