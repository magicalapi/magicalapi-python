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
  <a href="https://github.com/magical-api/python-library">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">MagicalAPI Python Client</h3>

  <p align="center">
    An Async and Type Annotated Python Client to Easy Access <a href="https://magicalapi.com">MagicalAPI.com</a> Service.
    <br />
    <!-- <a href="https://github.com/magical-api/python-library"><strong>Explore the docs »</strong></a> -->
    <!-- <br /> -->
    <!-- <br /> -->
    <a href="https://github.com/magical-api/python-library">View Demo</a>
    ·
    <a href="https://github.com/magical-api/python-library/issues">Report Bug</a>
    ·
    <a href="https://github.com/magical-api/python-library/issues">Request Feature</a>
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

MagicalAPI is an innovative platform that leverages the power of **artificial intelligence** to offer a range of services designed to enhance online **content creation**, **digital marketing**, and **business operations**. It specializes in tools for **YouTube SEO**, including **keyword and tag generation**, title and description optimization, and offers unique features like **resume parsing** and **profile data analysis** for platforms like **LinkedIn**. Whether you're looking to boost your online presence, gain insights into market trends, or streamline your content strategy, MagicalAPI provides **AI-driven** solutions tailored to meet these needs, making it an invaluable tool for businesses and individuals navigating the digital landscape.

<br>

<!-- ABOUT THE PROJECT -->

## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

this is a Python client that provides easy access to the [MagicalAPI.com][website-url] services, fully type annotated, and asynchonous.

<!-- `magical-api`, `python-library`, `MagicalAPI`, `MagicalAPI Python Client` -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

[![Pydantic][Pydantic.badge]](https://pydantic.dev/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

This is an example of how you install the client and use it in your own scripts and projects.

### Installation

Install package using `pip`

```bash
pip install magicalapi
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

here are some samples of how to use the client for each service. at first you have to create an object of `AsyncClient` like that :

```python
from magicalapi.client import AsyncClient

API_KEY = "mag_123456"
client = AsyncClinet(api_key=API_KEY)
```

you can pass the `API_KEY` on the code, or put it on a `.env` file and client will read from there.

### Config `.env` File

example of using `.env` file, all of settings starts with prefix `MAG_` and they are case insensitive, so `MAG_EXAMPLE`, `Mag_example`, and `mag_EXAMPLE` are equal.   

```bash
# .env

MAG_API_KEY="mag_1234567"
```

so now you can leave `api_key` parameter empty.

```python
from magicalapi.client import AsyncClient

client = AsyncClinet()
```

<br>

here is an example of how to get keywords of [Youtube Top Keywords](https://magicalapi.com/services/youtube-keywords) service :

```python
import asyncio
from magicalapi.client import AsyncClient
from magicalapi.types.base import ErrorResponse

search_sentence = "chatgpt 4 turbo" # your search sentence to get keywords related to
country = "1" # use get_countries method to see countries codes (Default = 1 : WorlWide)
language = "1000" # use get_languages method to see countries codes (Default = 1000 : English)


async def main():
    async with AsyncClient() as client:
        # get youtube keywords
        keywords_response = await client.youtube_top_keywords.get_keywords(
            search_sentence=search_sentence,
            country=country,
            language=language,
        )
        if type(keywords_response) == ErrorResponse:
            # got error from api
            print("Error :", keywords_response.message)
        else:
            # got response successfully
            print("credists :", keywords_response.usage.credits)
            print("keywords count :", len(keywords_response.data.keywords))

            # save response in json file
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

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

Here is the [Contributing Guidelines](./CONTRIBUTING.rst).
Don't forget to give the project a star! Thanks again!

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the MIT License. See [`LICENSE`](./LICENSE) for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->


[contributors-shield]: https://img.shields.io/github/contributors/magical-api/python-library.svg?style=for-the-badge
[contributors-url]: https://github.com/magical-api/python-library/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/magical-api/python-library.svg?style=for-the-badge
[forks-url]: https://github.com/magical-api/python-library/network/members
[stars-shield]: https://img.shields.io/github/stars/magical-api/python-library.svg?style=for-the-badge
[stars-url]: https://github.com/magical-api/python-library/stargazers
[issues-shield]: https://img.shields.io/github/issues/magical-api/python-library.svg?style=for-the-badge
[issues-url]: https://github.com/magical-api/python-library/issues
[license-shield]: https://img.shields.io/github/license/magical-api/python-library.svg?style=for-the-badge
[license-url]: https://github.com/magical-api/python-library/blob/master/LICENSE

<!-- [linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555 -->

<!-- [linkedin-url]: https://linkedin.com/company/MagicalAPI -->

<!-- [product-screenshot]: images/screenshot.png -->

[Pydantic.badge]: https://img.shields.io/badge/pydantic-black?style=for-the-badge&logo=pydantic&logoColor=red
[Httpx.badge]: https://img.shields.io/badge/Httpx-gray?style=for-the-badge
[tests-shield]: https://github.com/magical-api/python-library/actions/workflows/tests.yml/badge.svg
[pypi-version-shields]: https://img.shields.io/pypi/v/magicalapi
[pypi-python-versions-shields]: https://img.shields.io/pypi/pyversions/magicalapi
[website-url]: https://magicalapi.com
