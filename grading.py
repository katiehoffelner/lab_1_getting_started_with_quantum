# !!!!! HEY! !!!!
# This file is for grading your answers and so contains the correct answers!
# Don't use this to cheat please! If you get stuck, ask one of the organisers for help :)
from typing import Any

import numpy as np


def check_binary(num: int, num_bits: int | None, bitstring: str):
    if num_bits is None or "___" in bitstring:
        return print("Fill in the blanks first!")
    if set(bitstring) - {"0", "1"}:
        return print("Your bitstring should only contain 0s and 1s.")
    if len(bitstring) != num_bits:  # some sort of mismatch
        # is the num_bits wrong?
        if len(bitstring) == num.bit_length():
            return print("Your num_bits isn't quite right.")
        # the bitstring must be wrong
        return print("Your bitstring isn't quite right, it should be " + str(num_bits) + " bits long.")

    try:
        parsed = int(bitstring, 2)
    except:
        return print("Your bitstring isn't quite right. It should only contain 0s and 1s.")
    if parsed != num:
        return print("Your bitstring isn't quite right. In decimal, yours evaluates to " + str(parsed) + ", but it should evaluate to " + str(num) + ".")
    if num_bits != num.bit_length():
        return print("Your bitstring is right, but can you do it with fewer bits? Try removing the leading 0s.")

    return print(f"✅ Correct! {num} = {bitstring} ({num_bits} bits long).")


def check_basis_states(ket_00: np.ndarray | None,  ket_01: np.ndarray | None, ket_10: np.ndarray | None, ket_11: np.ndarray | None):
    if ket_00 is None or ket_01 is None or ket_10 is None or ket_11 is None:
        return print("Fill in the blanks first!")

    # Accept both flat [0, 1, 0, 0] and column [[0], [1], [0], [0]] vectors
    ket_00, ket_01, ket_10, ket_11 = (np.ravel(k)
                                      for k in (ket_00, ket_01, ket_10, ket_11))
    if any(k.shape != (4,) for k in (ket_00, ket_01, ket_10, ket_11)):
        return print("❌ Each two-qubit state should be a vector with 4 entries.")

    if not np.allclose(ket_00, np.array([1, 0, 0, 0])):
        return print("❌ Your |00⟩ state isn't quite right.")
    if not np.allclose(ket_01, np.array([0, 1, 0, 0])):
        return print("❌ Your |01⟩ state isn't quite right.")
    if not np.allclose(ket_10, np.array([0, 0, 1, 0])):
        return print("❌ Your |10⟩ state isn't quite right.")
    if not np.allclose(ket_11, np.array([0, 0, 0, 1])):
        return print("❌ Your |11⟩ state isn't quite right.")
    return print("✅ Correct! Your basis states are all correct.")


# Target states for the "build this state" puzzles (vector, how to print it)
TARGET_STATES: dict[str, tuple[Any, str]] = {
    "minus": (np.array([1, -1]) / np.sqrt(2), "|−⟩ = (|0⟩ − |1⟩)/√2"),
    "bell": (np.array([1, 0, 0, 1]) / np.sqrt(2), "(|00⟩ + |11⟩)/√2"),
}


def _format_state(vec: np.ndarray) -> str:
    """Write a statevector as e.g. '0.71|00⟩ + 0.71|11⟩', skipping zero amplitudes."""
    num_qubits = int(np.log2(len(vec)))
    terms = []
    for i, amp in enumerate(vec):
        if abs(amp) < 1e-9:
            continue
        if abs(amp.imag) < 1e-9:
            amp_str = f"{amp.real:.2f}"
        else:
            amp_str = f"({amp.real:.2f}{amp.imag:+.2f}i)"
        terms.append(f"{amp_str}|{i:0{num_qubits}b}⟩")
    return " + ".join(terms).replace("+ -", "− ")


def check_state(qc, target: str):
    from qiskit.quantum_info import Statevector

    if qc is None:
        return print("Fill in the blanks first!")
    target_vec, target_label = TARGET_STATES[target]
    num_qubits = int(np.log2(len(target_vec)))
    if qc.num_qubits != num_qubits:
        return print(f"❌ Your circuit should have {num_qubits} qubit(s), but it has {qc.num_qubits}.")

    try:
        state = Statevector(qc.remove_final_measurements(inplace=False))
    except Exception:
        return print("❌ Couldn't simulate your circuit. Make sure it only contains gates (no measurements).")

    if state.equiv(Statevector(target_vec)):
        return print(f"✅ Correct! You made {target_label}")

    print(f"❌ Not quite. You made:   {_format_state(state.data)}")
    print(f"   The target is:     {target_label}")
    if np.allclose(state.probabilities(), np.abs(target_vec) ** 2):
        print("   Hint: your measurement probabilities are right, but the phase isn't. Which gate changes the phase?")
