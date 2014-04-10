This project is hosted at GitHub_. I gladly accept both issues and pull
requests.

.. _GitHub: https://github.com/malept/mdn-js-sphinx-inventory

Filing Issues
-------------

Issues include bugs, feedback, and feature requests. Before you file a new
issue, please make sure that your issue has not already been filed by someone
else.

When filing a bug, please include the following information:

* Operating system name and version. If on Linux, please also include the
  distribution name.
* Python version, by running ``python -V``.
* Installed Python packages, by running ``pip freeze``.
* A detailed list of steps to reproduce the bug.
* If the bug is a Python exception, the traceback will be very helpful.

Pull Requests
-------------

Please make sure your pull requests pass the continuous integration suite, by
running ``tox`` before creating your submission. (Run ``pip install tox`` if
it's not already installed.) The CI suite is automatically run for every pull
request on GitHub, but at this time it's faster to run it locally. It would
probably also be in your best interests to add yourself to the ``AUTHORS.rst``
file if you have not done so already.
