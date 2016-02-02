===========================================
TYPO3 Python Doc Builder: t3pdb_sxw2html.py
===========================================

:author: Martin Bless
:email:  martin@mbless.de
:date:   2012-09-03, 2013-08-02, 2016-02-02

.. default-role:: code
.. highlight:: bash


What does it do?
================

``t3pdb_sxw2html.py`` is an OpenOffice to ReST converter.

It reads an OpenOffice document and creates ReST files, HTML files and
a complete TYPO3 Sphinx documentation project.

How to
======

- To run this locally on your personal machine you have to install
  some software: http://mbless.de/blog/2015/01/26/sphinx-doc-installation-steps.html

- Get the T3PythonDocBuilderPackage from https://github.com/marble/T3PythonDocBuilderPackage

- Goto the `t3pythondocbuilder` folder::

    $ cd ./T3PythonDocBuilderPackage/t3pythondocbuilder

- Specify the path to an OpenOffice manual::

    $ infile=~/example_manual.sxw

- Specify the path to a temp folder for temporary file storage::

    $ tempdir=~/temp

- Run the application::

    $ python  t3pdb_sxw2html.py   $infile $tempdir


What you should get
===================

$tempdir/t3pdb
--------------
A newly created folder containing all temporary and final output. The application will
remove the complete folder 't3pdb' the next time you run it
with the same $tempdir parameter.


$tempdir/t3pdb/*
----------------
==== ======================= =====================================
step file                    description
==== ======================= =====================================
1    manual-<images>         written by OpenOffice or by inline to file dumper
1    manual.html             saved by OpenOffice as HTML
2    manual.dl.inline.txt    ReST, may still contain inline images
2    manual.t3flt.inline.txt ReST, may still contain inline images
3    manual.dl.rst           single ReST file using "definition list" markup
3    manual.t3flt.rst        single ReST file using "t3-field-list-table" directive for tables
4    manual.dl.html          single HTML file renderd by Docutils from manual.dl.rst
4    manual.t3flt.html       single HTML file renderd by Docutils from manual.t3flt.rst
==== ======================= =====================================


$tempdir/t3pdb/Documentation
----------------------------

This is a complete Sphinx Documentation project in TYPO3-style!
Take this folder as a starter for your real documentation project.


$tempdir/t3pdb/Documentation/_make
----------------------------------

Run `make html` to generate your ReST source as HTML in TYPO3 style.


$tempdir/t3pdb/Documentation/_make/_not_versioned
-------------------------------------------------

These are logfiles of the Sphinx builder process.


$tempdir/t3pdb/logs/
--------------------

manual.t3flt.rst.t3rst2html-warnings.txt (**important**)
   Errors and warnings when parsing ReST

manual.dl.rst.t3rst2html-warnings.txt (**important**)
   Errors and warnings when parsing ReST

manual.flt.rst.t3rst2html-warnings.txt (**important**)
   Errors and warnings when parsing ReST


manual.html.tidy-error-log.txt
   Notes from tidy when it's creating xhtml from html.

manual.html.restparser-log.txt
   Notes of the restparser about what has been done.

manual.html.restparser-tree.txt
   A tree like dump of the input html.
   This is useful for debugging the HTML parser and ReST writer.


manual.dl.rst.t3rst2html-stderr-log.txt
   stderr output when doing ``python t3rst2html.py``

manual.dl.rst.t3rst2html-stdout.txt
   stdout output when doing ``python t3rst2html.py``

manual.flt.rst.t3rst2html-stderr-log.txt
   stderr output when doing ``python t3rst2html.py``

manual.t3flt.rst.t3rst2html-stderr-log.txt
   stderr output when doing ``python t3rst2html.py``

manual.flt.rst.t3rst2html-stdout.txt
   stderr output when doing ``python t3rst2html.py``

manual.t3flt.rst.t3rst2html-stdout.txt
   stderr output when doing ``python t3rst2html.py``


$tempdir/t3pdb/_sliced
----------------------
Temporary files of an intermediate step. Can be removed.



2013-08-02, new: Convert *.gif to *.png
---------------------------------------

*2016-02-02 This step is deaactivated!*

Images of the OpenOffice document typically have names like
:file:`manual_html_11cdfe72.gif`. Since GIF files are not garanteed to
work in Latex they are now converted to PNG and saved additionally as
'GIF-file-name.gif'+'.png'. So in this case there will be and
additional file :file:`manual_html_11cdfe72.gif.png`. The references to
the images are changed in the :file:'manual.html' by a simple
"string search and replace" from ``*.gif`` to ``*.gif.png``.

The GIF files are not removed but kept as a measure of precaution. It
should be ok to remove them since they are not being referenced.

.. note::

   The `Python Imaging Library (PIL) <http://www.pythonware.com/products/pil/>`__
   is used for the GIF to PNG conversion. Available via "easy_install"
   and the `Python Package Index <https://pypi.python.org/pypi/PIL>`__.

   This is not a new requirement since its already installed on the
   TYPO3 Docs server.


End of README.

