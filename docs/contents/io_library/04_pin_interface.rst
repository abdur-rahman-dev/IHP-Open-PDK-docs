Pin Interface
=============

.. _io_pin_interface_lbl:

.. tip::
    All pads have ``vdd``, ``vss``, ``iovdd``, ``iovss`` power/ground pins in addition
    to the signal pins listed below.

Output Pads (``sg13g2_IOPadOut*mA``)
------------------------------------

.. code-block:: verilog

    module sg13g2_IOPadOut30mA (iovdd, iovss, vdd, vss, pad, c2p);

+------------+-----------+---------------------------------------------------+
| Pin        | Direction | Description                                       |
+============+===========+===================================================+
| ``c2p``    | input     | Core-to-pad signal (1.2V domain)                  |
+------------+-----------+---------------------------------------------------+
| ``pad``    | inout     | Pad connection to bond wire (3.3V domain)         |
+------------+-----------+---------------------------------------------------+

Input Pad (``sg13g2_IOPadIn``)
------------------------------

.. code-block:: verilog

    module sg13g2_IOPadIn (iovdd, iovss, vdd, vss, pad, p2c);

+------------+-----------+---------------------------------------------------+
| Pin        | Direction | Description                                       |
+============+===========+===================================================+
| ``pad``    | inout     | Pad connection from bond wire (3.3V domain)       |
+------------+-----------+---------------------------------------------------+
| ``p2c``    | output    | Pad-to-core signal (1.2V domain)                  |
+------------+-----------+---------------------------------------------------+

Bidirectional Pads (``sg13g2_IOPadInOut*mA``)
---------------------------------------------

.. code-block:: verilog

    module sg13g2_IOPadInOut30mA (iovdd, iovss, vdd, vss, pad, c2p, c2p_en, p2c);

+------------+-----------+---------------------------------------------------+
| Pin        | Direction | Description                                       |
+============+===========+===================================================+
| ``c2p``    | input     | Core-to-pad signal (1.2V domain)                  |
+------------+-----------+---------------------------------------------------+
| ``c2p_en`` | input     | Output enable (active high, 1.2V domain)          |
+------------+-----------+---------------------------------------------------+
| ``p2c``    | output    | Pad-to-core signal (1.2V domain)                  |
+------------+-----------+---------------------------------------------------+
| ``pad``    | inout     | Pad connection to bond wire (3.3V domain)         |
+------------+-----------+---------------------------------------------------+

Analog Pad (``sg13g2_IOPadAnalog``)
------------------------------------

.. code-block:: verilog

    module sg13g2_IOPadAnalog (iovdd, iovss, vdd, vss, pad, padres);

+------------+-----------+--------------------------------------------------------------+
| Pin        | Direction | Description                                                  |
+============+===========+==============================================================+
| ``pad``    | inout     | Pad connection to bond wire (3.3V domain)                    |
+------------+-----------+--------------------------------------------------------------+
| ``padres`` | inout     | Pad connection through secondary protection (resistor+diodes)|
+------------+-----------+--------------------------------------------------------------+

Tri-State Output Pads (``sg13g2_IOPadTriOut*mA``)
-------------------------------------------------

.. code-block:: verilog

    module sg13g2_IOPadTriOut30mA (iovdd, iovss, vdd, vss, pad, c2p, c2p_en);

+------------+-----------+---------------------------------------------------+
| Pin        | Direction | Description                                       |
+============+===========+===================================================+
| ``c2p``    | input     | Core-to-pad signal (1.2V domain)                  |
+------------+-----------+---------------------------------------------------+
| ``c2p_en`` | input     | Output enable (active high, 1.2V domain)          |
+------------+-----------+---------------------------------------------------+
| ``pad``    | inout     | Pad connection to bond wire (3.3V domain)         |
+------------+-----------+---------------------------------------------------+


Sources
-------

- ``verilog/sg13g2_io.v``: Module port signatures, pin names and directions
