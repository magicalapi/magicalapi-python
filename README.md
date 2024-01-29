# MagicalAPI Library

## Configuration
the library's configurations are stored in `magicalapi/settings.py`, and they can be overridden by environment variables or a `.env` file if exists in the root directory of the project.  
the environment variables should start with the `MAG_` prefix, and they are case insensitive, so `MAG_EXAMPLE`, `Mag_example`, and `mag_EXAMPLE` are equal.  
an example `.env` file content:
```env
# Comments are ignored

MAG_REQUEST_TIMEOUT = 20
```  

<br>

## Examples

here are some examples of how to send a request and get a response for each service.

<h3>
<a href='https://magicalapi.com/services/youtube-keywords' target="_blank">Youtube Top Keywrods<a>
</h3>

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
