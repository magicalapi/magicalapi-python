import asyncio
from magicalapi.client import AsyncClient
from magicalapi.errors import APIServerError, APIServerTimedout
from magicalapi.types.base import ErrorResponse

resume_url = "https://example.com/resume.pdf"
output_file_name = "resume_parser.json"


async def main():
    try:
        # the api_key will load from the .env file
        async with AsyncClient() as client:
            response = await client.resume_parser.get_resume_parser(url=resume_url)

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
