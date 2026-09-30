"""
AcuDiag Master Verification Runner
Executes all 23 automated tests across DSP Math, 10 Adversarial Eval Cases, and 3-Rail Mock Server.
"""

import sys
import subprocess
import time

def run():
    print("=" * 70)
    print(">> ACUDIAG ROUND 3 ENTERPRISE VERIFICATION HARNESS")
    print("=" * 70)
    
    t0 = time.time()
    creationflags = 0x08000000 if sys.platform == "win32" else 0
    res = subprocess.run(
        [sys.executable, "-m", "pytest", "01_Projects/AcuDiag/tests/", "-v", "--tb=short"],
        capture_output=True,
        text=True,
        creationflags=creationflags
    )
    duration = time.time() - t0
    
    print(res.stdout)
    if res.returncode != 0:
        print("\n>> VERIFICATION FAILED <<")
        print(res.stderr)
        sys.exit(1)

    # 2. Run Pass^k Enterprise Benchmark
    res_pk = subprocess.run(
        [sys.executable, "01_Projects/AcuDiag/benchmarks/run_pass_k_benchmark.py"],
        capture_output=True,
        text=True,
        creationflags=creationflags
    )
    print(res_pk.stdout)
    if res_pk.returncode != 0:
        print("\n>> PASS^k BENCHMARK FAILED <<")
        print(res_pk.stderr)
        sys.exit(1)

    # 3. Run CWRU 6205-2RS Dataset Kinematics Verification
    res_cwru = subprocess.run(
        [sys.executable, "01_Projects/AcuDiag/databank/06_Acoustic_Datasets/test_cwru_dataset_kinematics.py"],
        capture_output=True,
        text=True,
        creationflags=creationflags
    )
    print(res_cwru.stdout)
    if res_cwru.returncode != 0:
        print("\n>> CWRU DATASET KINEMATICS VERIFICATION FAILED <<")
        print(res_cwru.stderr)
        sys.exit(1)

    print("\n" + "=" * 70)
    print(f">> ALL VERIFICATION GATES PASSED (100% SUITE & PASS^50 IN {time.time() - t0:.2f}s) <<")
    print(">> ACUDIAG IS 100% READY FOR PINE LABS AGENTICORG ROUND 3 BUILD <<")
    print("=" * 70)

if __name__ == "__main__":
    run()
