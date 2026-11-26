# Variational Quantum Eigensolver (VQE) for Engineers

A practical, step-by-step demonstration of the **Variational Quantum Eigensolver (VQE)** written for engineers and software developers familiar with linear algebra and optimization, without requiring a deep background in quantum physics.

## Core Idea in Engineering Terms

Finding the lowest eigenvalue (ground-state energy) and corresponding eigenvector (ground state) of a Hermitian matrix $H$ is a central problem in quantum mechanics, quantum chemistry, and materials simulation:

$$H \vert{}\psi\rangle = E \vert{}\psi\rangle$$

For an $n$-qubit system, the state space has dimension $2^n \times 2^n$. VQE splits the work between a **quantum processor** and a **classical optimizer**:
1. **Define the problem:** Choose a system and represent it as a $2^n \times 2^n$ Hermitian matrix $H$ (here, a $4 \times 4$ matrix for $n = 2$ qubits).
2. **Prepare $n$ qubits:** Start with a 2-qubit register initialized to $\vert{}00\rangle$.
3. **Prepare a parameterized trial state (ansatz):** Apply simple rotations ($R_y(\theta_0), R_y(\theta_1)$) and entanglement (`CX`) controlled by classical parameters $\theta$.
4. **Choose a classical optimizer:** Use a straightforward optimizer such as `COBYLA` to update $\theta$ iteratively.
5. **Iterate and converge:** Evaluate the expectation value $\langle \psi(\theta) \vert{} H \vert{} \psi(\theta) \rangle$, feed it to the optimizer, and converge toward the ground-state eigenvalue and eigenstate.
6. **Scaling intuition:** For a tiny $4 \times 4$ matrix, classical `NumPy` is faster and simpler. As matrix size grows exponentially ($2^n \times 2^n$), VQE is designed to scale more naturally on quantum hardware for complex systems.
7. **Run in Qiskit:** Execute the 2-qubit workflow in `vqe.py`.
8. **Objective achieved:** Compare the VQE result against the exact ground-state eigenvalue and eigenstate—and inspect whether the ansatz is expressive enough to reach the true ground state.

## Repository Structure

```text
.
├── README.md
├── requirements.txt
└── vqe.py
```

## Virtual Environment Setup & Installation

Use Python 3.10 or newer (Python 3.11–3.14 recommended).

### 1. Clone the repository and enter the folder

```bash
git clone <YOUR_GITHUB_REPO_URL>
cd <YOUR_REPO_FOLDER_NAME>
```

### 2. Create and activate a virtual environment

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt / `cmd.exe`):**

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

Once activated, your terminal prompt should show `(.venv)`.

### 3. Upgrade `pip` and install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

To deactivate the virtual environment later, simply run:

```bash
deactivate
```

## Running the Code

With the virtual environment activated, run:

```bash
python3 vqe.py
```

*(On Windows, you can run `python vqe.py` or `python3 vqe.py`.)*

## Actual Run Output

```text
python3 vqe.py
Exact Eigenvalues (NumPy): [0.633975 1.633975 2.366025 3.366025]
Target Ground State Eigenvalue: 0.633975

Hamiltonian decomposed into Pauli strings:
SparsePauliOp(['II', 'IZ', 'XI', 'ZI', 'ZX'],
              coeffs=[ 2. +0.j,  0.5+0.j,  0.5+0.j, -0.5+0.j,  0.5+0.j])

Quantum Circuit (Ansatz):
     ┌───────┐     
q_0: ┤ Ry(0) ├──■──
     ├───────┤┌─┴─┐
q_1: ┤ Ry(0) ├┤ X ├
     └───────┘└───┘

Starting VQE Optimization Loop...
Iteration  1 | Angles: [  0.500,   0.500] | Energy: 2.293428
Iteration  5 | Angles: [  1.873,  -2.475] | Energy: 1.424907
Iteration 10 | Angles: [  3.649,  -3.292] | Energy: 1.205511
Iteration 15 | Angles: [  3.087,  -2.012] | Energy: 0.835358
Iteration 20 | Angles: [  3.153,  -2.434] | Energy: 0.795072
Iteration 25 | Angles: [  3.121,  -2.402] | Energy: 0.793809
Iteration 30 | Angles: [  3.143,  -2.345] | Energy: 0.792936
Iteration 35 | Angles: [  3.139,  -2.358] | Energy: 0.792898
Iteration 40 | Angles: [  3.141,  -2.356] | Energy: 0.792893
Iteration 45 | Angles: [  3.142,  -2.356] | Energy: 0.792893

--- VQE Optimization Complete ---
Total Iterations: 46
Optimal Angles Found: [ 3.14158159 -2.35623744]
VQE Ground State Eigenvalue:   0.792893
Exact Ground State Eigenvalue: 0.633975
Absolute Error:                1.589186e-01
VQE Statevector (Amplitudes):  [ 0.    +0.j -0.9239+0.j -0.    +0.j  0.3827+0.j]
Exact Ground Eigenvector:      [ 0.3251+0.j -0.8881+0.j  0.    +0.j  0.3251+0.j]
```

### Engineering Takeaway from This Run
Notice that VQE smoothly decreased the energy from `2.293428` down to `0.792893`, whereas the exact ground-state eigenvalue is `0.633975` (`1.589186e-01` difference). Why? Because a minimal two-rotation + single-`CX` ansatz has **limited expressibility**—it cannot represent the exact ground eigenvector `[0.3251, -0.8881, 0, 0.3251]`, so the optimizer settles on the best approximation (`[0, -0.9239, 0, 0.3827]`) reachable by this circuit. Adding more parameterized rotation/entanglement layers (or choosing a problem-tailored ansatz) lets VQE get closer to the true ground state.