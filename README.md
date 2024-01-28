# MagicalAPI Library

## Examples

here are some examples of how send request and get the response for each service.

### [Youtube Top Keywrods](https://magicalapi.com/services/youtube-keywords)

```python
import asyncio
from magicalapi.client import AsyncClient
from magicalapi.types.base import ErrorResponse

API_KEY = "mag_1234567890"

async def main():
    async with AsyncClient(api_key=API_KEY) as client:
        keywords_response = await client.youtube_top_keywords.get_keywords(
            search_sentence="github copilot",
            country="1",
            language="1000",
        )
        if type(keywords_response) == ErrorResponse:
            # got error from api
            print("Error :", keywords_response.message)
        else:
            # got response successfully
            print("credists :", keywords_response.usage.credits)
            print("keywords count :", len(keywords_response.data.keywords))

            with open("keywords_response.json", "w") as file:
                file.write(keywords_response.model_dump_json(indent=3))


asyncio.run(main())
```