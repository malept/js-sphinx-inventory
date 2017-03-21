=========================================================
Sphinx Inventory Generator for MDN's JavaScript Reference
=========================================================

Uses the `Sphinx Inventory Writer`_ to generate a Sphinx inventory file for the
`Mozilla Developer Network`_'s `JavaScript Reference`_.

.. _Sphinx Inventory Writer: https://github.com/malept/sphinx-inventory
.. _Mozilla Developer Network: https://developer.mozilla.org/
.. _JavaScript Reference: https://developer.mozilla.org/docs/Web/JavaScript/Reference

Requirements
------------

* CPython 2.7/3.3+ or PyPy

* The ``sphinx_inventory`` module (`Installation instructions`_)

.. _Installation instructions: https://github.com/malept/sphinx-inventory#installation

Usage
-----

Make sure you're connected to the Internet, then run:

.. code-block:: shell-session

   user@host:mdn-js-sphinx-inventory$ ./generate-inventory.py FILENAME

Where ``FILENAME`` is the path to the output file, like ``js-objects.inv``.

Once it's generated, you can use it in Sphinx-generated documentation via the
`intersphinx extension`_. Here is an example snippet of a Sphinx project's
``conf.py``:

.. code-block:: python

   # Inventory file location
   mdn_inv = '/path/to/mdn-js-objects.inv'
   # base URL
   mdn_url = 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/'

   intersphinx_mapping = {
       'mdn': (mdn_url, mdn_inv),
   }

In that project, JS objects/functions/etc., can be prefixed with ``mdn`` to be
recognized by the mapping. Example:

.. code-block:: rst

   .. js:function:: foo.bar([options])

      :param options: Kind of like ``**kwargs`` in Python.
      :type options: :mdn:class:`Object`

.. _intersphinx extension: http://sphinx-doc.org/ext/intersphinx.html
