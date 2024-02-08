import asyncio
from magicalapi.client import AsyncClient
from magicalapi.types.base import ErrorResponse
import json

API_KEY = "mag_123456789"
company_name = "google"
output_file = f"company_data_{company_name}.json"


async def main():
    try:
        async with AsyncClient(api_key=API_KEY) as client:
            response = await client.company_data.get_company_data(company_name=company_name)

            if isinstance(response, ErrorResponse):
                # got error from api
                print("Error:", response.message)
            else:
                # got response successfully
                print("Credits:", response.usage.credits)
                print(response.data)
                # save response in json file
                with open(output_file, "w") as file:
                    json.dump(response.data, file, indent=3)

    except Exception as e:
        print("An error occurred:", str(e))


asyncio.run(main())
