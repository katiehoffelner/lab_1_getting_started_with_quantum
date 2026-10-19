# Pictures for the notebook.
# You don't need to read this file to do the exercises, but feel free to have a look!
import matplotlib.pyplot as plt
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
