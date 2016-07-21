embed-pyqtgraph-tutorial
========================

This is a walkthrough of how to embed pyqtgraph_ in your PyQt applications
using the following steps:

* Create the layout of the UI in Qt Designer (generates ``template.ui``)
* Compile the resulting XML to Python source (uses ``build_ui.py`` to generate
  ``template.py``)
* Write a custom QWidget class which takes on the UI and populates the embedded
  pyqtgraph widget (``application.py``)

The example provided displays a `PlotWidget`_ with some data and a QCheckBox to
enable/disable mouse control of the plot.

.. image:: screenshot.png


Prerequisites
-------------

I'm going to assume you have some way of creating Qt applications with Python,
and the instructions should not be much (if at all) different between the ways
to accomplish that (i.e. PyQt4, PyQt5, and PySide). For reference, I'm using
PyQt4.

I'm also going to assume you have pyqtgraph installed and have some knowledge
of how to use it. The `pyqtgraph examples`_ cover the capabilities of pyqtgraph
pretty well.


Tutorial
--------

Creating the UI Layout
~~~~~~~~~~~~~~~~~~~~~~

::

    ┌────────────┐   ┌─────────────┐   ┌─────────────┐
    │ creativity │ → │ Qt Designer │ → │ template.ui │
    └────────────┘   └─────────────┘   └─────────────┘

Generally, you use custom widget implementations in Qt Designer through the
`promote`_ mechanism. Since we're using Python instead of C++, the "Header
file" in this case is going to be the Python namespace at which you would
access the class as though you were importing it. For example, if you had
a custom widget class, where an import statement might look like:

.. code:: python

    from myproject.widgets import CustomDialog

you would put ``myproject.widgets`` in the "Header file" field and
``CustomDialog`` in the "Promoted class name" field. The basic Qt class you
inherit from (e.g. QDialog, QWidget, etc.) is then the "Base class name."

pyqtgraph actually provides some documentation for how to embed plotting
objects into a Qt UI using Qt Designer (see `embed pyqtgraph`_). The basic idea
is that you lay out your UI with your plot(s) represented as QGraphicsView. You
then use the above instructions for promoting it to a pyqtgraph class.
pyqtgraph makes this simple by including pretty much everything in the
pyqtgraph namespace, so you just put ``pyqtgraph`` in the "Header file" field.

Compiling the Layout
~~~~~~~~~~~~~~~~~~~~

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
more.

The third option would be to use the UI template directly (i.e. using
``uic.loadUI()``). I tend to avoid this to make packaging the project easier,
but it is probably not all that difficult to package the UI templates. If
you're already dealing with packaging custom icon files and such, this would be
a non-issue.

Wrapping the UI in a Custom QWidget
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
generated Python code*.

The nice thing about this workflow overall is that it cleans up your custom
class code a lot, since you're not creating container layouts all over the
place, specifying sizes, size policies, etc. (take a peek at ``template.py`` --
even a trivial example is ugly). It just involves importing your template class
(PyQt refers to it as the *form class*), instantiating it in your custom
widget, and calling ``setupUi()``. You'll see that this is the first thing
happening in the ``CustomWidget`` implementation found in ``application.py``.

Once you have a class attribute representing your form class, you have access
to all of the widgets in it, named according to the names you specify in Qt
Designer. In the simple example presented here, I am accessing the PlotWidget
to plot some data, then connecting a check box to enable/disable the mouse on
that PlotWidget.

*Note: I prefer to explicitly set up the form class object as an attribute of
the custom widget rather than using multiple inheritance to use the form class
objects directly -- mostly because it's very clear when you're accessing UI
elements specified by Designer rather than widgets you might add
programmatically.*


.. _pyqtgraph: http://pyqtgraph.org/
.. _PlotWidget: http://pyqtgraph.org/documentation/widgets/plotwidget.html?highlight=plotwidget#pyqtgraph.PlotWidget
.. _pyqtgraph examples: https://github.com/pyqtgraph/pyqtgraph/tree/develop/examples
.. _embed pyqtgraph: http://pyqtgraph.org/documentation/how_to_use.html#embedding-widgets-inside-pyqt-applications
.. _promote: https://doc.qt.io/qt-4.8/designer-using-custom-widgets.html
.. _pyuic: http://pyqt.sourceforge.net/Docs/PyQt4/designer.html#module-PyQt4.uic
.. _using the generated code: http://pyqt.sourceforge.net/Docs/PyQt4/designer.html
