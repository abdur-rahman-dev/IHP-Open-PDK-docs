Output Drive Strength
=====================

.. _io_drive_strength_lbl:

The output pads are available in three drive strength variants: **4 mA**, **16 mA** and **30 mA**.
The naming refers to the **short-circuit current** of the output driver, i.e. the current the pad can
source or sink when driving a load to the opposite rail.

From the SPICE netlist (``spice/sg13g2_io.spi``), all three variants share the same
internal architecture:

1. A level shifter (``GateLevelUpInv``) converts the 1.2V core signal to the 3.3V IO domain.
2. A complementary NMOS/PMOS clamp pair drives the pad.
3. ESD protection diodes (``DCNDiode``, ``DCPDiode``) protect against electrostatic discharge.

The difference between the variants is the **number of parallel transistors** in the
clamp subcircuits:

.. csv-table:: Output Driver Clamp Transistors
    :header: "Variant", "NMOS Clamp", "PMOS Clamp", "NMOS Transistors", "PMOS Transistors"
    :stub-columns: 0
    :file: tables/io_driver_fingers.csv
    :widths: 100, 200, 200, 100, 100

.. tip::
    Each NMOS instance is a ``sg13_hv_nmos`` (W=4.4 um, L=0.6 um) and each PMOS instance
    is a ``sg13_hv_pmos`` (W=6.66 um, L=0.6 um). More parallel transistors means more
    current capability and the ability to drive larger capacitive loads.


.. _io_short_circuit_current_lbl:

Short-Circuit Current by Process Corner
----------------------------------------

The following tables show the simulated short-circuit current for each output pad variant
across process corners. Values are from the simulation notebook ``doc/DriveStrengthSim.html``.

.. tip::
    The TriState (``IOPadTriOut``) and Bidirectional (``IOPadInOut``) variants have identical
    drive characteristics to their corresponding ``IOPadOut`` variant.

**Sink current** (NMOS pull-down active, pad driven to VOL):

.. csv-table:: Sink Current
    :header: "Cell", "NOM", "SLOW", "SLOW_COMM", "SLOW_ROOM", "FAST", "FAST_COMM", "FAST_ROOM"
    :stub-columns: 0
    :file: tables/io_sink_current.csv
    :widths: 200, 80, 80, 80, 80, 80, 80, 80

**Source current** (PMOS pull-up active, pad driven to VOH):

.. csv-table:: Source Current
    :header: "Cell", "NOM", "SLOW", "SLOW_COMM", "SLOW_ROOM", "FAST", "FAST_COMM", "FAST_ROOM"
    :stub-columns: 0
    :file: tables/io_source_current.csv
    :widths: 200, 80, 80, 80, 80, 80, 80, 80


.. _io_max_capacitance_lbl:

Maximum Load Capacitance
------------------------

The Liberty timing models specify a ``max_capacitance`` constraint for each pad output pin.
STA tools will flag a violation when the actual load exceeds this value.

.. csv-table:: Liberty ``max_capacitance`` Constraint
    :header: "Cell", "drive_current", "max_capacitance (pF)", "Liberty Corner"
    :stub-columns: 0
    :file: tables/io_max_capacitance.csv
    :widths: 200, 100, 150, 200

However, the Liberty timing lookup tables (``cell_rise``, ``cell_fall``) are characterized
up to much higher loads:

- **4 mA**: up to 10 pF
- **16 mA**: up to 15 pF
- **30 mA**: up to 30 pF

These are the ``index_2`` upper bounds of the delay tables, meaning timing data is available
and the pads can physically drive loads up to these values.

.. note::
    The ``max_capacitance`` values are significantly lower than the ``index_2`` upper bounds
    in the timing lookup tables. This means STA tools will flag violations at capacitances
    where timing data is still available and the pad can physically drive the load.


.. _io_transition_times_lbl:

Output Transition Times
-----------------------

The following tables show the output ``rise_transition`` and ``fall_transition`` times
from the Liberty timing models (typical corner, ``lib/sg13g2_io_typ_1p2V_3p3V_25C.lib``).

The Liberty lookup tables use two indices: input slew (``index_1``) and output load
capacitance (``index_2``). Since the input slew has a negligible effect on the output
transition time (< 0.1% variation), only the load capacitance dependency is shown below.

.. note::
    Each drive strength variant is characterized at **different load capacitance points**
    (``index_2``) in the Liberty file. The load values shown in each table below are
    exactly those defined in the Liberty lookup tables. This is why the three tables
    do not share the same capacitance points.

**sg13g2_IOPadOut4mA** (characterized from 1 to 10 pF):

.. csv-table:: Transition Times (4 mA)
    :header: "Load (pF)", "Rise (ns)", "Fall (ns)"
    :stub-columns: 0
    :file: tables/io_transition_4mA.csv
    :widths: 100, 100, 100

**sg13g2_IOPadOut16mA** (characterized from 1 to 15 pF):

.. csv-table:: Transition Times (16 mA)
    :header: "Load (pF)", "Rise (ns)", "Fall (ns)"
    :stub-columns: 0
    :file: tables/io_transition_16mA.csv
    :widths: 100, 100, 100

**sg13g2_IOPadOut30mA** (characterized from 2 to 30 pF):

.. csv-table:: Transition Times (30 mA)
    :header: "Load (pF)", "Rise (ns)", "Fall (ns)"
    :stub-columns: 0
    :file: tables/io_transition_30mA.csv
    :widths: 100, 100, 100


Sources
-------

PDK files in ``$PDK_ROOT/ihp-sg13g2/libs.ref/sg13g2_io/``:

- ``spice/sg13g2_io.spi``: Internal architecture, clamp subcircuit names,
  parallel transistor counts, transistor dimensions (W, L)
- ``doc/DriveStrengthSim.html``: Sink and source current tables (all process corners)
- ``lib/sg13g2_io_typ_1p2V_3p3V_25C.lib``: ``drive_current``, ``max_capacitance``,
  ``rise_transition``, ``fall_transition``, output voltage definitions (VOH, VOL)
