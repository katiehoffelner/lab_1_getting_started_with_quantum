### !!!!! HEY! !!!!
### This file is for grading your answers and so contains the correct answers!
### Don't use this to cheat please! If you get stuck, ask one of the organisers for help :)
import numpy as np


def check_binary(num: int, num_bits : int | None, bitstring : str):
    if num_bits is None or "___" in bitstring:
        return print("Fill in the blanks first!")
    if set(bitstring) - {"0", "1"}:
        return print("Your bitstring should only contain 0s and 1s.")
    if len(bitstring) != num_bits: # some sort of mismatch
        # is the num_bits wrong?
        if len(bitstring) == len(bin(num)[2:]):
            return print("Your num_bits isn't quite right.")
        # the bitstring must be wrong
        return print("Your bitstring isn't quite right, it should be " + str(num_bits) + " bits long.")

    try:
        parsed = int(bitstring, 2)
    except: 
        return print("Your bitstring isn't quite right. It should only contain 0s and 1s.")
    if parsed != num:
        return print("Your bitstring isn't quite right. In decimal, yours evaluates to " + str(parsed) + ", but it should evaluate to " + str(num) + ".")

    return print(f"✅ Correct! {num} = {bitstring} ({num_bits} bits long).")


def check_basis_states(ket_00: np.ndarray | None,  ket_01:np.ndarray | None, ket_10:np.ndarray | None, ket_11:np.ndarray | None):
    if ket_00 is None or ket_01 is None or ket_10 is None or ket_11 is None:
        return print("Fill in the blanks first!")
    
    if not np.allclose(ket_00, np.array([1, 0, 0, 0])):
        return print("❌ Your |00⟩ state isn't quite right.")
    if not np.allclose(ket_01, np.array([[0], [1], [0], [0]])):
        return print("❌ Your |01⟩ state isn't quite right.")
    if not np.allclose(ket_10, np.array([[0], [0], [1], [0]])):
        return print("❌ Your |10⟩ state isn't quite right.")
    if not np.allclose(ket_11, np.array([[0], [0], [0], [1]])):
        return print("❌ Your |11⟩ state isn't quite right.")
    return print("✅ Correct! Your basis states are all correct.")