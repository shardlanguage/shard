import os
import traceback

from shardc.cli.cli import cli
from spp.constants import LIB_PATH

if __name__ == "__main__":
    if not os.path.exists(LIB_PATH):
        print(f"{LIB_PATH} does not exist. Attempting creation...")
        if os.geteuid() == 0:
            os.mkdir(LIB_PATH)
            print(f"Created {LIB_PATH}")
        else:
            raise PermissionError(f"Failed to create: root permissions needed.")

    try:
        cli()
    except Exception as e:
        print("PYTHON ERROR")
        print("=============================")
        print("Python errors are not supposed to happen. However, because Shard is at an early development stage,")
        print("they may occur. If you believe this is the compiler's fault, please make an Issue on GitHub.")
        traceback.print_exc()