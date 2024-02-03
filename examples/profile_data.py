import asyncio
from magicalapi.client import AsyncClient
from magicalapi.types.base import ErrorResponse

API_KEY = "mag_123456789"
profile_name = "conanobrien"


async def main():
    async with AsyncClient(api_key=API_KEY) as client:
        response = await client.profile_data.get_profile_data(profile_name=profile_name)

        if type(response) == ErrorResponse:
            # got error from api
            print("Error :", response.message)
        else:
            # got response successfully
            print("credists :", response.usage.credits)
            print(response.data)
            # save response in json file
            with open(f"profile_data_{profile_name}.json", "w") as file:
                file.write(response.model_dump_json(indent=3))


asyncio.run(main())
