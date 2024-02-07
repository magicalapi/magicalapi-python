import asyncio
from magicalapi.client import AsyncClient
from magicalapi.types.base import ErrorResponse

API_KEY = "mag_12345678"
profile_name = "conanobrien"


async def main():
    async with AsyncClient(api_key=API_KEY) as client:
        try:
            response = await client.profile_data.get_profile_data(profile_name=profile_name)
            print("Credits:", response.usage.credits)
            print(response.data)
            # Save response in JSON file
            file_path = f"profile_data_{profile_name}.json"
            with open(file_path, "w") as file:
                file.write(response.model_dump_json(indent=3))
            print(f"Profile data saved to {file_path}")
        except Exception as e:
            print("An error occurred:", e)


asyncio.run(main())
