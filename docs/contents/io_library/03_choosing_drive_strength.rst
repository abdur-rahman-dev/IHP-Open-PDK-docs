Choosing the Right Drive Strength
=================================

.. _io_choosing_drive_strength_lbl:

The drive strength should be chosen based on the **load capacitance** the pad must drive.
The Liberty timing tables (``cell_rise``, ``cell_fall``) are indexed by output load
capacitance (``index_2``), showing that delay scales with load (e.g. 4 mA: 1.48 ns at
1 pF vs 5.38 ns at 10 pF). The ``max_capacitance`` constraint sets the STA limit for
each variant.

.. csv-table:: Drive Strength Selection
    :header: "Variant", "max_capacitance", "index_2 range", "Rout (SLOW)", "Source"
    :widths: 100, 100, 100, 150, 200

    "4 mA", "1.11 pF", "1 – 10 pF", "≈ 1.4 kΩ (3.3V / 2.3mA)", "Liberty L.3026 + DriveStrengthSim"
    "16 mA", "4.21 pF", "1 – 15 pF", "≈ 355 Ω (3.3V / 9.3mA)", "Liberty L.2640 + DriveStrengthSim"
    "30 mA", "4.53 pF", "2 – 30 pF", "≈ 190 Ω (3.3V / 17.4mA)", "Liberty L.2833 + DriveStrengthSim"

.. warning::
    The 4 mA variant: in the slow process corner, Rout ≈ 3.3V / 2.3mA ≈ 1.4 kΩ.
    With a 10 kΩ resistive load: VOL ≈ 3.3 × 1.4k / (1.4k + 10k) ≈ 0.41V instead of 0V.
    For capacitive loads: t_rise ≈ C × ΔV / I = 5pF × 3.3V / 2.3mA ≈ 7.2 ns
    (vs 1.1 ns at NOM for 1 pF).

.. csv-table:: Typical Load Capacitances (external references)
    :header: "Load Type", "Typical Value", "Source", "Justification"
    :widths: 150, 100, 200, 200

    "PCB trace (FR4)", "~1-2 pF/cm", "Cadence, PCBway", "εr=4.6, thickness=1.6mm, trace width=0.75mm"
    "IC pin (QFP package)", "~1 pF", "ResearchGate", "Parasitic model of package lead"
    "Chip-to-chip total", "2-15 pF", "Cadence, ResearchGate", "Trace + pin + connector; depends on length"
    "Wire bond", "0.05-0.6 pF", "HFE, TI SNOA405A", "Predominantly inductive; ~0.2 pF typical"
    "RF/wafer test probe", "~0.7-1 pF", "edaboard", "Agilent RF probe: 1MΩ // 0.7pF"
    "Oscilloscope probe", "8-15 pF", "edaboard", "Standard passive probe; not for pad characterization"


Sources
-------

PDK files in ``$PDK_ROOT/ihp-sg13g2/libs.ref/sg13g2_io/``:

- ``lib/sg13g2_io_typ_1p2V_3p3V_25C.lib``: ``max_capacitance``, ``index_2`` bounds,
  ``drive_current``
- ``doc/DriveStrengthSim.html``: Sink current by process corner (for Rout calculation)

Mathematical deductions (Rout = IOVDD / Isink):

.. csv-table::
    :header: "Calculation", "Formula", "Values", "Result"
    :widths: 200, 200, 200, 100

    "Rout 4 mA SLOW", "IOVDD / Isink_slow", "3.3V / 2.3mA", "≈ 1.4 kΩ"
    "Rout 16 mA SLOW", "IOVDD / Isink_slow", "3.3V / 9.3mA", "≈ 355 Ω"
    "Rout 30 mA SLOW", "IOVDD / Isink_slow", "3.3V / 17.4mA", "≈ 190 Ω"
    "VOL (4 mA SLOW, Rload=10 kΩ)", "IOVDD × Rout / (Rout + Rload)", "3.3 × 1400 / (1400 + 10000)", "≈ 0.41V"
    "t_rise (4 mA SLOW, C=5 pF)", "C × ΔV / I", "5e-12 × 3.3 / 2.3e-3", "≈ 7.2 ns"

External references for typical load capacitances:

- PCB trace capacitance ~1-2 pF/cm on FR4:
  `Cadence <https://resources.pcb.cadence.com/blog/2019-how-parasitic-capacitance-and-inductance-affect-your-signals>`_,
  `PCBway <https://www.pcbway.com/blog/Engineering_Technical/PCB_Trace_to_Plane_Capacitance_Formula.html>`_
- IC pin capacitance ~1 pF (QFP):
  `ResearchGate <https://www.researchgate.net/figure/Model-of-IC-package-and-PCB-parasitic-C-P-IN-is-assumed-to-have-a-value-of-1-pF-for_fig1_311738623>`_
- Wire bond capacitance 0.05-0.6 pF:
  `HFE <https://www.highfrequencyelectronics.com/index.php?option=com_content&view=article&id=1663>`_,
  `TI SNOA405A <https://www.ti.com/lit/an/snoa405a/snoa405a.pdf>`_
- RF/wafer probe capacitance ~0.7-1 pF:
  `edaboard <https://www.edaboard.com/threads/capacitance-of-rf-probes.248473/>`_
