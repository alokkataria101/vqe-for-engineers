import numpy as np
from scipy.optimize import minimize
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp, Statevector


def build_hamiltonian() -> SparsePauliOp:
    """
    Construct a 4x4 Hermitian matrix (2-qubit Hamiltonian) and convert it
    into a weighted sum of Pauli strings (SparsePauliOp).
    """
    H = np.array(
        [
            [2.0, 0.5, 0.5, 0.0],
            [0.5, 1.0, 0.0, 0.5],
            [0.5, 0.0, 3.0, -0.5],
            [0.0, 0.5, -0.5, 2.0],
        ],
        dtype=complex,
    )

    # Verify Hermitian property: H == H^dagger
    assert np.allclose(H, H.conj().T), "Matrix must be Hermitian!"

    return SparsePauliOp.from_operator(H)


def build_ansatz(num_qubits: int = 2) -> QuantumCircuit:
    """
    Prepare a simple 2-qubit parameterized trial state (ansatz):
    - Ry rotation on each qubit
    - CNOT entangling gate between q0 and q1
    """
    qc = QuantumCircuit(num_qubits)
    qc.ry(0.0, 0)
    qc.ry(0.0, 1)
    qc.cx(0, 1)
    return qc


def main():
    hamiltonian = build_hamiltonian()
    H_matrix = hamiltonian.to_matrix()

    # Exact classical reference (feasible only for small matrices)
    exact_evals, exact_evecs = np.linalg.eigh(H_matrix)
    exact_ground_energy = float(np.min(exact_evals))
    exact_ground_state = exact_evecs[:, int(np.argmin(exact_evals))]

    print(f"Exact Eigenvalues (NumPy): {np.round(exact_evals, 6)}")
    print(f"Target Ground State Eigenvalue: {exact_ground_energy:.6f}\n")

    print("Hamiltonian decomposed into Pauli strings:")
    print(f"{hamiltonian}\n")

    template_ansatz = build_ansatz(num_qubits=2)
    print("Quantum Circuit (Ansatz):")
    print(template_ansatz.draw(output="text"))
    print()

    iteration = 0
    history = []

    def cost_function(params: np.ndarray) -> float:
        nonlocal iteration
        iteration += 1

        qc = QuantumCircuit(2)
        qc.ry(float(params[0]), 0)
        qc.ry(float(params[1]), 1)
        qc.cx(0, 1)

        state = Statevector.from_instruction(qc)
        energy = float(np.real(state.expectation_value(hamiltonian)))

        history.append((iteration, params.copy(), energy))
        if iteration == 1 or iteration % 5 == 0:
            print(
                f"Iteration {iteration:2d} | "
                f"Angles: [{params[0]:7.3f}, {params[1]:7.3f}] | "
                f"Energy: {energy:.6f}"
            )
        return energy

    initial_params = np.array([0.5, 0.5], dtype=float)

    print("Starting VQE Optimization Loop...")
    result = minimize(
        cost_function,
        initial_params,
        method="COBYLA",
        options={"maxiter": 200, "rhobeg": 1.0},
    )

    opt_angles = result.x
    vqe_energy = float(result.fun)

    # Build optimal quantum state (ground-state eigenfunction approximation)
    opt_circuit = QuantumCircuit(2)
    opt_circuit.ry(float(opt_angles[0]), 0)
    opt_circuit.ry(float(opt_angles[1]), 1)
    opt_circuit.cx(0, 1)
    vqe_statevector = Statevector.from_instruction(opt_circuit).data

    abs_error = abs(vqe_energy - exact_ground_energy)

    print("\n--- VQE Optimization Complete ---")
    print(f"Total Iterations: {iteration}")
    print(f"Optimal Angles Found: {opt_angles}")
    print(f"VQE Ground State Eigenvalue:   {vqe_energy:.6f}")
    print(f"Exact Ground State Eigenvalue: {exact_ground_energy:.6f}")
    print(f"Absolute Error:                {abs_error:.6e}")
    print(f"VQE Statevector (Amplitudes):  {np.round(vqe_statevector, 4)}")
    print(f"Exact Ground Eigenvector:      {np.round(exact_ground_state, 4)}")


if __name__ == "__main__":
    main()