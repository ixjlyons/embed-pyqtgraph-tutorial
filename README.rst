========================
embed-pyqtgraph-tutorial
========================

This is a walkthrough of embedding pyqtgraph_ content in a PyQt application
you're designing with Qt Designer. Here's an overview of the steps involved:

* Create the layout of the UI in Qt Designer (generates ``template.ui``)
* Compile the XML template to Python source (uses ``build_ui.py`` to generate
  ``template.py``)
* Write a custom QWidget class which takes on the UI and populates the embedded
  pyqtgraph widget (``application.py``)

The example provided displays a `PlotWidget`_ with some data and a QCheckBox to
enable/disable mouse control of the plot. It's a simple example, but once
you've seen the process of adding pyqtgraph widgets to your UI, you can create
arbitrarily complex applications without having to write a ton of boilerplate
layout code.

.. image:: screenshot.png


Prerequisites
=============

I'm going to assume you have some way of creating Qt applications with Python,
and the instructions here should not be much (if at all) different between the
ways to accomplish that (i.e. PyQt4, PyQt5, PySide, PySide2). For reference,
I'm using PyQt5 and Python 3, so the following works for setting up an
environment for running the example::

   $ python -m venv .venv
   $ source .venv/bin/activate
   (.venv) $ pip install pyqt5 pyqtgraph
   (.venv) $ python application.py

If you're using a different setup (e.g. PyQt4, PySide), you'll need to fix some
imports before being able to run the example application.

I'm also going to assume you have have some knowledge of how to use pyqtgraph.
The `pyqtgraph examples`_ cover its capabilities pretty well.


Tutorial
========

Creating the UI Layout
----------------------

::

    ┌────────────┐   ┌─────────────┐   ┌─────────────┐
    │ creativity │ → │ Qt Designer │ → │ template.ui │
    └────────────┘   └─────────────┘   └─────────────┘

Generally, you can use custom widgets in Qt Designer through the `promote`_
mechanism. This means you add an item of the base class of your custom item to
your UI layout, right click on it, then go to "Promote to ...". Since we're
using Python instead of C++, the "Header file" in this case is going to be the
Python namespace at which you would access the class as though you were
importing it. For example, if you had a custom widget class, where an import
statement might look like:

.. code:: python

    from myproject.widgets import CustomDialog

you would put ``myproject.widgets`` in the "Header file" field and
``CustomDialog`` in the "Promoted class name" field. The basic Qt class you
inherit from (e.g. QDialog, QWidget, etc.) is then the "Base class name."

pyqtgraph actually provides some documentation for how to embed plotting
objects into a Qt UI using Qt Designer (see `embed pyqtgraph`_), but it's a bit
lacking. In our case, add a QGraphicsView to the layout where you want the plot
to be, then promote it to a PlotWidget. Most pyqtgraph classes are available
under the pyqtgraph namespace, so just put "pyqtgraph" in the header file
field.

If you inspect the ``template.ui`` file, you can see towards the bottom there
is a ``customwidget`` section specifying everything we just covered:

========== ==============
class      PlotWidget
base class QGraphicsView
namespace  pyqtgraph
========== ==============

Compiling the Layout
--------------------

::

    ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
    │ template.ui │ → │ build_ui.py │ → │ template.py │
    └─────────────┘   └─────────────┘   └─────────────┘

There are a few ways to turn your UI template into Python code. The first (my
preferred) way of doing it is to write a little script to grab all of your
``*.ui`` files and use the `pyuic`_ module to write the corresponding Python
code to the desired destination. An example is given here (``build_ui.py``).
You can modify the ``SRC`` and ``DEST`` variables if you want to arrange your
project structure differently. My recommendation is to put your UI files in
something like ``res/`` and the compiled Python files in your project source to
make importing simple (see the next step).

You could instead use ``pyuic`` directly from the command line. For single UI
templates, this is fine, but you'll want a scripted approach if you end up with
more. For reference, here's how you'd convert the template given here::

   (.venv) $ pyuic5 template.ui -o template.py

The third option would be to use the UI template directly from your
hand-written Python code (i.e. using ``uic.loadUI()``). I tend to avoid this to
make packaging the project easier, but it is probably not all that difficult to
package the UI templates. If you're already dealing with packaging custom icon
files and such, this would be a non-issue.

Now, if you take a look at the ``template.py`` file, you'll see there's a class
called ``Ui_CustomWidget`` that has, primarily, a ``setupUi`` method to create
and lay out all of the content we designed in Qt Designer. This is a pretty
simple example, but with complex layouts with many items, the use of Qt
Designer and automatic generation of this code really shines.

Also notice the import line at the bottom of the file:

.. code-block:: python

    from pyqtgraph import PlotWidget

This all comes straight from that bottom section of the ``template.ui`` file,
where we specified in Qt Designer that we have a custom item of a specific
class and where it can be found.

Wrapping the UI in a Custom QWidget
-----------------------------------

::

    ┌─────────────┐   ┌────────────────┐   ┌─────────┐
    │ template.py │ → │ application.py │ → │ success │
    └─────────────┘   └────────────────┘   └─────────┘

Now for the difficult part. PyQt provides some documentation for `using the
generated code`_, though it is a little sparse if you don't have the high-level
overview of the whole process. Essentially, you write a custom class (usually
QWidget, but really it can be any QWidget-like class such as QMainWindow,
QDialog, etc.), then use the compiled Python code to access and interact with
the layout you specified. The key here is that you *are not modifying the
generated Python code*. That means in our case that we don't want to mess with
``template.py`` by hand. If you make changes to it, you can no longer make
changes to your UI from Qt Designer because re-generating the template will
overwrite your changes!

The nice thing about this workflow overall is that it cleans up your custom
class code a lot, since you're not creating container layouts all over the
place, specifying sizes, size policies, etc.

Our implementation is in ``application.py``. It starts out with importing Qt
stuff so we can set up a QApplication and run it. We also *import the template
module* so we have access to the template class (PyQt refers to it as the *form
class*). We then write a custom QWidget implementation which instantiates the
form class and calls its ``setupUi`` method. I typically assign the form class
to an attribute called ``ui``. Once you call ``setupUi``, you now can access
the items in your UI through the names they were given in Qt Designer.

So in our example, we access the ``plotWidget`` attribute of the form class
object, which is a pyqtgraph PlotWidget object. Now the pyqtgraph API applies,
so we can plot some content and whatever else we need. In this case, we connect
up the checkbox to a method that toggles mouse functionality on the PlotWidget.

*Note: It is possible to make CustomWidget inherit from UI_CustomWidget (so
you'd call ``self.setupUi()``), but I prefer to explicitly set up the form
class object as an attribute of the custom widget -- mostly because it's very
clear when you're accessing UI elements specified by Designer rather than
widgets you might add programmatically.*


Other Notes
===========

Feel free to open an issue if anything here isn't clear.

I originally wrote this in response to seeing questions on the `pyqtgraph
mailing list`_ about using pyqtgraph functionality in an application designed
with Qt Designer. It's not obvious at all that you can use the promote
mechanism with PyQt (as opposed to C++ Qt), so I wrote this to help people out.
Feel free to use these materials in a pull request to improve pyqtgraph
documentation.


.. _pyqtgraph: http://pyqtgraph.org/
.. _PlotWidget: http://pyqtgraph.org/documentation/widgets/plotwidget.html
.. _pyqtgraph examples: https://github.com/pyqtgraph/pyqtgraph/tree/develop/examples
.. _embed pyqtgraph: http://pyqtgraph.org/documentation/how_to_use.html#embedding-widgets-inside-pyqt-applications
.. _promote: http://doc.qt.io/qt-5/designer-using-custom-widgets.html
.. _pyuic: http://pyqt.sourceforge.net/Docs/PyQt5/designer.html#the-uic-module
.. _using the generated code: http://pyqt.sourceforge.net/Docs/PyQt5/designer.html
.. _pyqtgraph mailing list: https://groups.google.com/forum/#!forum/pyqtgraph
