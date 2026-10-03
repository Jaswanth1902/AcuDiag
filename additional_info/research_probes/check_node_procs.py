import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
cmd = "Get-CimInstance Win32_Process -Filter \"Name = 'node.exe'\" | ForEach-Object { \"$($_.ProcessId): $($_.CommandLine)\" }"
out = subprocess.check_output(["powershell", "-NoProfile", "-Command", cmd], creationflags=0x08000000).decode()
print("Node processes:")
print(out)
