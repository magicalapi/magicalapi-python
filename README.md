<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->

[![PyPI - Version][pypi-version-shields]][pypi-url]
[![PyPI - Python Version][pypi-python-versions-shields]][pypi-url]
[![Downloads](https://static.pepy.tech/badge/magicalapi)][pypi-url]
<!-- (https://pepy.tech/project/magicalapi) -->

<!--[![Contributors][contributors-shield]][contributors-url]-->
<!-- [![Forks][forks-shield]][forks-url]-->

[![Tests][tests-shield]][github-repo-url]
[![Issues][issues-shield]][issues-url]
[![Stargazers][stars-shield]][stars-url]
[![MIT License][license-shield]][license-url]




<!-- PROJECT LOGO -->

<br />
<div align="center">
  <a href="https://magicalapi.com">
    <img src="https://raw.githubusercontent.com/magicalapi/magicalapi-python/master/docs/logo.png?raw=true" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">MagicalAPI Python Client</h3>

  <p align="center">
    An Async and Type Annotated Python Client to Easy Access <a href="https://magicalapi.com">MagicalAPI.com</a> Service.
    <br />
    <!-- <a href="https://github.com/magicalapi/magicalapi-python"><strong>Explore the docs »</strong></a> -->
    <!-- <br /> -->
    <!-- <br /> -->
    <!-- <a href="https://github.com/magicalapi/magicalapi-python">View Demo</a> -->
    <!-- · -->
    <a href="https://github.com/magicalapi/magicalapi-python/issues">Report Bug</a>
    ·
    <a href="https://github.com/magicalapi/magicalapi-python/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->

## Table of Contents
- [What is MagicalAPI?](#what-is-magicalapi)
- [Features](#features)
- [About the Project](#about-the-project)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)


<!-- ABOUT THE MAGICALAPI -->

## What is [MagicalAPI][website-url]?
[MagicalAPI](https://magicalapi.com) is your AI edge in **careers** and **data insights**, Your ultimate tool for **Resume Parsing**, **LinkedIn data** and more.
It offers services like:
- **Resume Parsing**: Extract structured data from resumes.
- **LinkedIn Data Extraction**: Scrape and analyze LinkedIn profiles.
- **Career Insights**: Gain AI-driven recommendations for career development.

## Features
- **Resume Parsing**: Parse resumes to extract key information like skills, experience, and education.
- **LinkedIn Profile Scraping**: Extract data from LinkedIn profiles for analysis.
- **Career Insights**: Leverage AI to get actionable career recommendations.
- **Type-Annotated and Async**: Built for modern Python with type hints and asynchronous support.


<br>

<!-- ABOUT THE PROJECT -->

## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

This is a Python client that provides easy access to the [MagicalAPI.com][website-url] services, fully type annotated, and asynchronous.

<!-- `magicalapi`, `magicalapi-python`, `MagicalAPI`, `MagicalAPI Python Client` -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!--
### Built With

[![Pydantic][Pydantic.badge]](https://pydantic.dev/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
-->

<!-- GETTING STARTED -->

## Getting Started

This is an example of how you can install the client and use it in your own scripts and projects.

### Installation

Install package using `pip`

```bash
pip install magicalapi
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

here are some samples of how to use the client for each service. 
At first, you have to create an object of `AsyncClient` like this:

```python
from magicalapi.client import AsyncClient

API_KEY = "mag_123456"
client = AsyncClient(api_key=API_KEY)
```

You can pass the `API_KEY` on the code, or put it on a `.env` file and the client will read from there.

### Config `.env` File

Example of using `.env` file, all settings start with the prefix `MAG_` and are case insensitive, so `MAG_EXAMPLE`, `Mag_example`, and `mag_EXAMPLE` are equal.   

```bash
# .env

MAG_API_KEY="mag_1234567"
```

So now you can leave `api_key` parameter empty.

```python
from magicalapi.client import AsyncClient

client = AsyncClinet()
```

<br>

### Using Webhooks (Optional)

For asynchronous response delivery, you can provide a `webhook_url` when initializing the client. The API will send the response to your webhook endpoint instead of using the polling mechanism.

```python
from magicalapi.client import AsyncClient

# Your webhook must be whitelisted in MagicalAPI panel
webhook_url = "https://your-domain.com/webhook"
client = AsyncClient(webhook_url=webhook_url)
```

**Important:** Webhook domains must be registered in the [MagicalAPI panel](https://panel.magicalapi.com/). For setup guide, see the [webhook documentation](https://docs.magicalapi.com/docs/webhook) and [example](https://github.com/magicalapi/magicalapi-python/blob/master/examples/webhook_example.py).

<br>

Here is an example of how to parse a resume using [Resume Parser](https://magicalapi.com/resume/) service:

```python
import asyncio

from magicalapi.client import AsyncClient
from magicalapi.errors import APIServerError, APIServerTimedout
from magicalapi.types.base import ErrorResponse

resume_url = (
    "https://resume-resource.com/wp-content/uploads/00123-sales-professional-resume.pdf"
)
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
```

All of the methods in the client have **type hints** and help to simply use.

_For full examples, please see the [Examples Directory](https://github.com/magicalapi/magicalapi-python/blob/master/examples/)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

Contributions are what makes the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

Here is the [Contributing Guidelines](https://github.com/magicalapi/magicalapi-python/blob/master/CONTRIBUTING.rst).
Don't forget to give the project a star! Thanks again!

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the MIT License. See [`LICENSE`](https://github.com/magicalapi/magicalapi-python/blob/master/LICENSE) for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- SHIELDS -->
[contributors-shield]: https://img.shields.io/github/contributors/magicalapi/magicalapi-python.svg?style=for-the-badge
[forks-shield]: https://img.shields.io/github/forks/magicalapi/magicalapi-python.svg?style=for-the-badge
[stars-shield]: https://img.shields.io/github/stars/magicalapi/magicalapi-python?style=flat&color=green
[issues-shield]: https://img.shields.io/github/issues/magicalapi/magicalapi-python.svg
[license-shield]: https://img.shields.io/github/license/magicalapi/magicalapi-python.svg
<!-- other links -->
[contributors-url]: https://github.com/magicalapi/magicalapi-python/graphs/contributors
[forks-url]: https://github.com/magicalapi/magicalapi-python/network/members
[stars-url]: https://github.com/magicalapi/magicalapi-python/stargazers
[issues-url]: https://github.com/magicalapi/magicalapi-python/issues
[license-url]: https://github.com/magicalapi/magicalapi-python/blob/master/LICENSE
[pypi-url]: https://pypi.org/project/magicalapi
[github-repo-url]: https://github.com/magicalapi/magicalapi-python
<!-- [linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555 -->

<!-- [linkedin-url]: https://linkedin.com/company/MagicalAPI -->

<!-- [product-screenshot]: images/screenshot.png -->

[Pydantic.badge]: https://img.shields.io/badge/pydantic-black?style=for-the-badge&logo=pydantic&logoColor=red
[Httpx.badge]: https://img.shields.io/badge/Httpx-gray?style=for-the-badge
[tests-shield]: https://github.com/magicalapi/magicalapi-python/actions/workflows/tests.yml/badge.svg
[pypi-version-shields]: https://img.shields.io/pypi/v/magicalapi
[pypi-python-versions-shields]: https://img.shields.io/pypi/pyversions/magicalapi
[website-url]: https://magicalapi.com


