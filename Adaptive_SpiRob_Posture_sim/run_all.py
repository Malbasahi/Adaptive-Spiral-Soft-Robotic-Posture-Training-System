import subprocess
import sys

commands = [
    [sys.executable, "evaluate_system.py"],
    [sys.executable, "parameter_sweep.py"],
    [sys.executable, "plot_results.py"],
]

for cmd in commands:
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)

print("Done. Check results/ and figures/.")
