<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->

![Tests][tests-shield]
![PyPI - Version][pypi-version-shields]
![PyPI - Python Version][pypi-python-versions-shields]

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->

<br />
<div align="center">
  <a href="https://github.com/magicalapi/magicalapi-python">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">MagicalAPI Python Client</h3>

  <p align="center">
    An Async and Type Annotated Python Client to Easy Access <a href="https://magicalapi.com">MagicalAPI.com</a> Service.
    <br />
    <!-- <a href="https://github.com/magicalapi/magicalapi-python"><strong>Explore the docs »</strong></a> -->
    <!-- <br /> -->
    <!-- <br /> -->
    <a href="https://github.com/magicalapi/magicalapi-python">View Demo</a>
    ·
    <a href="https://github.com/magicalapi/magicalapi-python/issues">Report Bug</a>
    ·
    <a href="https://github.com/magicalapi/magicalapi-python/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#waht-is-magicalapi">What is MagicalAPI</a>
    </li>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <!-- <li><a href="#prerequisites">Prerequisites</a></li> -->
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <!-- <li><a href="#acknowledgments">Acknowledgments</a></li> -->
  </ol>
</details>


<!-- ABOUT THE MAGICALAPI -->

## What is [MagicalAPI][website-url]?

MagicalAPI is your AI edge in **content** and **careers**, Your ultimate tool for **YouTube SEO**, **Resume Parsing**, **LinkedIn data** and more.

<br>

<!-- ABOUT THE PROJECT -->

## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

This is a Python client that provides easy access to the [MagicalAPI.com][website-url] services, fully type annotated, and asynchronous.

<!-- `magicalapi`, `magicalapi-python`, `MagicalAPI`, `MagicalAPI Python Client` -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

[![Pydantic][Pydantic.badge]](https://pydantic.dev/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

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

Here is an example of how to get keywords of [Youtube Top Keywords](https://magicalapi.com/services/youtube-keywords) service:

```python
import asyncio
from magicalapi.client import AsyncClient
from magicalapi.types.base import ErrorResponse

search_sentence = "chatgpt 4 turbo" # your search sentence to get keywords related to
country = "1" # use get_countries method to see countries codes (Default = 1 : WorlWide)
language = "1000" # use get_languages method to see countries codes (Default = 1000 : English)


async def main():
    # the api_key will load from the .env file
    async with AsyncClient() as client:
        # Get YouTube keywords
        keywords_response = await client.youtube_top_keywords.get_keywords(
            search_sentence=search_sentence,
            country=country,
            language=language,
        )
        if type(keywords_response) == ErrorResponse:
            # got error from API
            print("Error :", keywords_response.message)
        else:
            # got response successfully
            print("credits :", keywords_response.usage.credits)
            print("keywords count :", len(keywords_response.data.keywords))

            # save response in JSON file
            with open("keywords_response.json", "w") as file:
                file.write(keywords_response.model_dump_json(indent=3))


        # get languages list
        # languages = await client.youtube_top_keywords.get_languages()
        # get countries list
        # countries = await client.youtube_top_keywords.get_countries()


asyncio.run(main())
```

All of the methods in the client have **type hints** and help to simply use.

_For full examples, please see the [Examples Directory](./examples/)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

Contributions are what makes the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

Here is the [Contributing Guidelines](./CONTRIBUTING.rst).
Don't forget to give the project a star! Thanks again!

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the MIT License. See [`LICENSE`](./LICENSE) for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->


[contributors-shield]: https://img.shields.io/github/contributors/magicalapi/magicalapi-python.svg?style=for-the-badge
[contributors-url]: https://github.com/magicalapi/magicalapi-python/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/magicalapi/magicalapi-python.svg?style=for-the-badge
[forks-url]: https://github.com/magicalapi/magicalapi-python/network/members
[stars-shield]: https://img.shields.io/github/stars/magicalapi/magicalapi-python.svg?style=for-the-badge
[stars-url]: https://github.com/magicalapi/magicalapi-python/stargazers
[issues-shield]: https://img.shields.io/github/issues/magicalapi/magicalapi-python.svg?style=for-the-badge
[issues-url]: https://github.com/magicalapi/magicalapi-python/issues
[license-shield]: https://img.shields.io/github/license/magicalapi/magicalapi-python.svg?style=for-the-badge
[license-url]: https://github.com/magicalapi/magicalapi-python/blob/master/LICENSE

<!-- [linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555 -->

<!-- [linkedin-url]: https://linkedin.com/company/MagicalAPI -->

<!-- [product-screenshot]: images/screenshot.png -->

[Pydantic.badge]: https://img.shields.io/badge/pydantic-black?style=for-the-badge&logo=pydantic&logoColor=red
[Httpx.badge]: https://img.shields.io/badge/Httpx-gray?style=for-the-badge
[tests-shield]: https://github.com/magicalapi/magicalapi-python/actions/workflows/tests.yml/badge.svg
[pypi-version-shields]: https://img.shields.io/pypi/v/magicalapi
[pypi-python-versions-shields]: https://img.shields.io/pypi/pyversions/magicalapi
[website-url]: https://magicalapi.com
