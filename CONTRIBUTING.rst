============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/magicalapi/magicalapi-python/issues

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
and "help wanted" is open to whoever wants to implement a fix for it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

MagicalAPI python client could always use more documentation, whether as part of
the official docs, in docstrings, or even on the web in blog posts, articles,
and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at
https://github.com/magicalapi/magicalapi-python/issues.

If you are proposing a new feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `magicalapi-python` for local
development. Please note this documentation assumes you already have
`poetry` and `Git` installed and ready to go.

| 1. Fork the `magicalapi-python` repo on GitHub.

| 2. Clone your fork locally:

   .. code-block:: bash

        cd <directory_in_which_repo_should_be_created>
        git clone git@github.com:YOUR_NAME/magicalapi-python.git


| 3. Now we need to install the environment. Navigate into the directory

   .. code-block:: bash

       cd magicalapi-python

..    If you are using ``pyenv``, select a version to use locally. (See installed versions with ``pyenv versions``)

..    .. code-block:: bash

..        pyenv local <x.y.z>

   Then, install and activate the environment with:

   .. code-block:: bash

        poetry install
        poetry shell

.. | 4. Install pre-commit to run linters/formatters at commit time:

..    .. code-block:: bash

..         poetry run pre-commit install

| 4. Create a branch for local development:

   .. code-block:: bash

        git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.


| 5. Don't forget to add test cases for your added functionality to the ``tests`` directory.

| 6. Now, validate that all unit tests are passing:

   .. code-block:: bash

        pytest

| 7. Before raising a pull request you should also run tox. This will run the
   tests across different versions of Python:

   .. code-block:: bash

        tox

   This requires you to have multiple versions of python installed.
   This step is also triggered in the CI/CD pipeline, so you could also choose to skip this
   step locally.

| 8. Commit your changes and push your branch to GitHub:

   .. code-block:: bash

        git add .
        git commit -m "Your detailed description of your changes."
        git push origin name-of-your-bugfix-or-feature

| 9. Submit a pull request through the GitHub website.

Pull Request Guidelines
---------------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.

2. If the pull request adds functionality, the docs should be updated. Put your
   new functionality into a function with a docstring.
