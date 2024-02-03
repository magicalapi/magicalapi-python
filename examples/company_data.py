import asyncio
from magicalapi.client import AsyncClient
from magicalapi.types.base import ErrorResponse

API_KEY = "mag_123456789"
company_name = "google"


async def main():
    async with AsyncClient(api_key=API_KEY) as client:
        response = await client.company_data.get_company_data(company_name=company_name)

        if type(response) == ErrorResponse:
            # got error from api
            print("Error :", response.message)
        else:
            # got response successfully
            print("credists :", response.usage.credits)
            print(response.data)
            # save response in json file
            with open(f"company_data_{company_name}.json", "w") as file:
                file.write(response.model_dump_json(indent=3))


asyncio.run(main())
