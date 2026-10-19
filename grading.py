# !!!!! HEY! !!!!
# This file is for grading your answers and so contains the correct answers!
# Don't use this to cheat please! If you get stuck, ask one of the organisers for help :)
from typing import Any

import numpy as np

_progress: dict[str, bool] = {}  # question key -> answered correctly, for check_progress()


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
    "six": (np.eye(8)[6], "|110⟩ (6 in binary)"),
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

    _progress[f"state_{target}"] = state.equiv(Statevector(target_vec))
    if _progress[f"state_{target}"]:
        return print(f"✅ Correct! You made {target_label}")

    print(f"❌ Not quite. You made:   {_format_state(state.data)}")
    print(f"   The target is:     {target_label}")
    if np.allclose(state.probabilities(), np.abs(target_vec) ** 2):
        print("   Hint: your measurement probabilities are right, but the phase isn't. Which gate changes the phase?")


# ---------------------------------------------------------------------------
# End-of-module questions. Results are recorded so check_progress() can sum up.
# ---------------------------------------------------------------------------
QUESTION_KEYS = [f"tf{i}" for i in range(1, 10)] + [
    "bit_vs_qubit", "measurement", "state_six", "patterns", "superposed_adder", "toffoli"]


def _record(key: str, correct: bool, message: str):
    _progress[key] = correct
    print(("✅ Correct! " if correct else "❌ Not quite. ") + message)


TRUE_FALSE_ANSWERS = {
    1: (True, "A classical bit is always exactly 0 or 1."),
    2: (False, "Entangled qubits are linked: measuring one tells you about the other."),
    3: (False, "Quantum gates are unitary, so they can always be undone."),
    4: (False, "In Qiskit, q0 is the rightmost (least significant) qubit."),
    5: (False, "If the state is a superposition, repeated runs give random outcomes."),
    6: (True, "H turns |0⟩ into an equal superposition of |0⟩ and |1⟩."),
    7: (True, "Measurement collapses a superposition to one basis state."),
    8: (False, "N bits have 2^N possible states, not 2N. For example, 3 bits give 8 states."),
    9: (True, "The probability of measuring |i⟩ is |c_i|²."),
}


def check_true_false(question: int, answer: bool | None):
    if answer is None:
        return print("Fill in the blank first! Set answer to True or False.")
    if not isinstance(answer, bool):
        return print("Your answer should be True or False (no quotes).")
    correct, explanation = TRUE_FALSE_ANSWERS[question]
    _record(f"tf{question}", answer == correct, explanation if answer == correct else "Try again!")


def check_fair_coin(qc):
    from qiskit.quantum_info import Statevector

    if qc.num_qubits != 1:
        return print(f"❌ Your circuit should have 1 qubit, but it has {qc.num_qubits}.")
    probs = Statevector(qc.remove_final_measurements(inplace=False)).probabilities()
    _record(
        "bit_vs_qubit",
        np.allclose(probs, [0.5, 0.5]),
        f"Your qubit measures 0 with probability {probs[0]:.2f} and 1 with probability {probs[1]:.2f}."
        + (" A classical bit can't do that: it's always definitely 0 or definitely 1." if np.allclose(probs, [0.5, 0.5])
           else " The target is 0.50 each."),
    )


def check_remeasure(prediction: float | None):
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator

    if prediction is None:
        return print("Fill in the blank first!")
    qc = QuantumCircuit(1, 2)
    qc.h(0)
    qc.measure(0, 0)
    qc.measure(0, 1)
    counts = AerSimulator().run(qc, shots=1000).result().get_counts()
    agree = 100 * (counts.get("00", 0) + counts.get("11", 0)) / 1000
    print(f"Simulated 1000 shots: {counts}")
    print(f"The two measurements agreed {agree:.0f}% of the time.")
    _record(
        "measurement",
        abs(prediction - 100) < 1e-9,
        "The first measurement collapses the superposition, so the second one always finds the same result.",
    )


def check_qiskit_patterns(steps: list[str] | None):
    if steps is None or len(steps) != 4 or not all(isinstance(step, str) for step in steps):
        return print("Fill in the blank first! Your answer should be a list of 4 steps.")
    expected = ["map", "optim", "execut", "post"]  # word stems, so "optimize" and "optimise" both count
    correct = all(stem in step.lower() for stem, step in zip(expected, steps))
    _record("patterns", correct, "Map → Optimize → Execute → Post-process." if correct
            else "Check the spelling and the order of your steps.")


def check_superposed_adder(qc, num_outcomes: int | None):
    from qiskit.quantum_info import Statevector

    if num_outcomes is None:
        return print("Fill in the blank first!")
    if qc.num_qubits != 4:
        return print(f"❌ Your circuit should have 4 qubits, but it has {qc.num_qubits}.")
    probs = Statevector(qc.remove_final_measurements(inplace=False)).probabilities_dict()
    if probs.keys() != {"0000", "0101", "0110", "1011"} or not np.allclose(list(probs.values()), 0.25):
        return print("❌ Your circuit doesn't put both A and B into an equal superposition yet. Which gate does that?")
    _record(
        "superposed_adder",
        num_outcomes == 4,
        "Each bar is one row of the truth table (read as C S B A): 0+0, 1+0, 0+1 and 1+1. "
        "The adder computed all four sums at once, but each measurement only shows you one of them at random."
        if num_outcomes == 4 else "Count the bars in your histogram (ignore any tiny ones caused by noise).",
    )


def check_toffoli_cnots(num_cnots: int | None):
    if num_cnots is None:
        return print("Fill in the blank first!")
    _record("toffoli", num_cnots == 6, "The Toffoli gate decomposes into 6 CNOTs plus some single-qubit gates."
            if num_cnots == 6 else "Count the CNOT gates (the ⊕ symbols) in the decomposed circuit.")


def check_progress():
    done = sum(_progress.get(key, False) for key in QUESTION_KEYS)
    print(f"You've answered {done} of {len(QUESTION_KEYS)} questions correctly.")
    if done == len(QUESTION_KEYS):
        print("🎉 All done! Great work.")
