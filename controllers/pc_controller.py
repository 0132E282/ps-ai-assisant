import os
import platform

class PCController:
    def __init__(self):
        self.os_type = platform.system()
        print(f"PC Controller Initialized ({self.os_type})")

    def execute(self, command_type, params):
        if command_type == "open_app":
            app_name = params.get("app_name")
            print(f"[PC] Attempting to open: {app_name}")
            if self.os_type == "Darwin": # macOS
                os.system(f"open -a '{app_name}'")
            elif self.os_type == "Windows":
                os.system(f"start {app_name}")
            return True
        return False
