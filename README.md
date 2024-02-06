# MagicalAPI Library

## Configuration
the library's configurations are stored in `magicalapi/settings.py`, and they can be overridden by environment variables or a `.env` file if exists in the root directory of the project.  
the environment variables should start with the `MAG_` prefix, and they are case insensitive, so `MAG_EXAMPLE`, `Mag_example`, and `mag_EXAMPLE` are equal.  
an example `.env` file content:
```bash
# Comments are ignored

MAG_API_KEY="mag_12345656787"
MAG_REQUEST_TIMEOUT=20
```  

<br>

## Examples

here are some examples of how to send a request and get a response for each service.

full usage examples are in [examples](./examples) directory.

the complete usage exists on the first example and in others just contains  details about usage of specific service, because the base implementation is same in all services.

<!--youtube top keywords-->

<h3

Youtube Top Keywords 
(
<a href='https://magicalapi.com/services/youtube-keywords' target="_blank">Service<a> , 
<a href='./examples/youtube_top_keywords.py' target="_blank">Example<a>
)

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

<!--profile data-->
<br>

<h3>

Profile Data 
(
<a href='https://magicalapi.com/services/profile-data' target="_blank">Service<a> , 
<a href='./examples/profile_data.py' target="_blank">Example<a>
)
<a>
</h3>

```python
await client.profile_data.get_profile_data(profile_name="profile_name")
```


<!--company data-->
<br>

<h3>
Company Data 
(
<a href='https://magicalapi.com/services/company-data' target="_blank">Service<a> , 
<a href='./examples/company_data.py' target="_blank">Example<a>
)
<a>
</h3>


```python
await client.company_data.get_company_data(company_name="company_name")
```

<!--youtub seo-->
<br>

<h3>
Youtube SEO 
(
<!--a href='https://magicalapi.com/services/youtube-seo' target="_blank">Service<a> , -->
<a href='./examples/youtube_seo.py' target="_blank">Example<a>
)

<a>
</h3>


```python
await client.youtube_seo.get_youtube_seo(url="https://youtube.com/?v=example")
```

<!--resume parser-->
<br>

<h3>

Resume Parser 
(
<a href='https://magicalapi.com/services/resume-parser' target="_blank">Service<a> , 
<a href='./examples/resume_parser.py' target="_blank">Example<a>
)
<a>
</h3>


```python
await client.resume_parser.get_resume_parser(url="https://example.com/resume.pdf")
```

<!--resume score-->
<br>

<h3>
Resume Score 
(
<a href='https://magicalapi.com/services/resume-score' target="_blank">Service<a> , 
<a href='./examples/resume_score.py' target="_blank">Example<a>
)

<a>
</h3>


```python
await client.resume_score.get_resume_score(
    url="https://example.com/resume.pdf",
    job_description="an example job description"
)
```

<!--resume review-->
<br>

<h3>
Resume Review 
(
<!--a href='https://magicalapi.com/services/resume-review' target="_blank">Service<a> , -->
<a href='./examples/resume_review.py' target="_blank">Example<a>
)
</h3>


```python
await client.resume_review.get_resume_review(url="https://example.com/resume.pdf")
```

<!-- youtube suggestions -->
<br>

<h3>
Youtube Suggestions 
(
<a href='https://magicalapi.com/services/youtube-suggestions' target="_blank">Service<a> , 
<a href='./examples/youtube_suggestions.py' target="_blank">Example<a>
)
</h3>


```python
await client.youtube_suggestions.get_youtube_suggestions(
    prompt_sentence="your prompt sentence to get suggestions based on it",
    count=10,
    suggestion_goal="hashtag",
)
```
