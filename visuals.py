# Pictures and interactive widgets for the notebook.
# You don't need to read this file to do the exercises, but feel free to have a look!
from io import BytesIO

import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import display
from qiskit import QuantumCircuit
from qiskit.quantum_info import Pauli, Statevector
from qiskit.visualization import (
    plot_bloch_multivector,
    plot_bloch_vector,
    plot_histogram,
)


def _qubit_figure(state: Statevector):
    """A single qubit's Bloch sphere next to its measurement probabilities."""
    fig = plt.figure(figsize=(8, 3.5))
    bloch = [state.expectation_value(Pauli(p)).real for p in "XYZ"]
    plot_bloch_vector(bloch, ax=fig.add_subplot(1, 2, 1, projection="3d"))

    bars = fig.add_subplot(1, 2, 2)
    probs = state.probabilities()
    bars.bar(["0", "1"], probs, color=["#6929c4", "#1192e8"])
    for x, p in enumerate(probs):
        bars.text(x, p + 0.02, f"{p:.2f}", ha="center")
    bars.set_ylim(0, 1.1)
    bars.set_ylabel("Probability")
    bars.set_title("Chance of measuring...")
    return fig


def _png(fig) -> bytes:
    # Widgets swap the bytes of one Image instead of clearing and redrawing output, which flickers in VS Code
    buffer = BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight")
    plt.close(fig)
    return buffer.getvalue()


def show(qc: QuantumCircuit):
    """Draw a circuit, then what it does to the qubits (Bloch spheres and measurement probabilities)."""
    qc = qc.remove_final_measurements(inplace=False)
    display(qc.draw("mpl"))
    state = Statevector(qc)
    if qc.num_qubits == 1:
        _qubit_figure(state)
        plt.show()
    else:
        display(plot_bloch_multivector(state))
        display(plot_histogram(state.probabilities_dict(decimals=3), title="Chance of measuring..."))


def qubit_explorer():
    """Two sliders: one sets the odds of measuring 0 or 1, the other sets the phase."""
    odds = widgets.IntSlider(value=0, min=0, max=180, step=5, description="Tilt (°)")
    phase = widgets.IntSlider(value=0, min=0, max=360, step=5, description="Phase (°)")
    image = widgets.Image(format="png")

    def update(_=None):
        qc = QuantumCircuit(1)
        qc.ry(np.radians(odds.value), 0)
        qc.p(np.radians(phase.value), 0)
        image.value = _png(_qubit_figure(Statevector(qc)))

    odds.observe(update, names="value")
    phase.observe(update, names="value")
    update()
    display(widgets.VBox([odds, phase, image]))


def gate_playground():
    """Click gate buttons to build up a circuit and watch what each gate does to the qubit."""
    qc = QuantumCircuit(1)
    circuit_image = widgets.Image(format="png")
    qubit_image = widgets.Image(format="png")

    def redraw():
        circuit_image.value = _png(qc.draw("mpl"))
        qubit_image.value = _png(_qubit_figure(Statevector(qc)))

    def add_gate(gate):
        def on_click(_):
            getattr(qc, gate)(0)
            redraw()
        return on_click

    def reset(_):
        qc.clear()
        redraw()

    buttons = []
    for gate in ["x", "h", "z", "t"]:
        button = widgets.Button(description=gate.upper(), layout=widgets.Layout(width="60px"))
        button.on_click(add_gate(gate))
        buttons.append(button)
    reset_button = widgets.Button(description="Reset", button_style="warning")
    reset_button.on_click(reset)

    redraw()
    display(widgets.VBox([widgets.HBox(buttons + [reset_button]), circuit_image, qubit_image]))
