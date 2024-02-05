import asyncio
from magicalapi.client import AsyncClient
from magicalapi.types.base import ErrorResponse

API_KEY = "mag_123456789"
resume_url = "https://example.com/resume.pdf"
job_description = "a description about job"
output_file_name = "resume_score.json"


async def main():
    async with AsyncClient(api_key=API_KEY) as client:
        response = await client.resume_score.get_resume_score(
            url=resume_url, job_description=job_description
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
