import json
import falcon
import shutil
import psutil

class AppHealthCheck:
    """
    To Check APP Health
    """
    def on_get(self, req, resp):
        """
        Get Request For App Health Check
        """

        cpu_dict = self.cpu_usage()
        cpu_dict["health"] = "OK"
        cpu_dict["message"] = "Working Fine."
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(cpu_dict)

    def cpu_usage(self):
        """
        To Check CPU Usage
        """
        du = shutil.disk_usage("/")
        used = (du.used / du.total) * 100
        cpu_percent_data = psutil.cpu_percent()
        virtual_memory_data = dict(psutil.virtual_memory()._asdict())
        virtual_memory_data['used_disk'] = used
        virtual_memory_data['available_disk'] = (100 - used)
        virtual_memory_data['cpu_percent_data'] = cpu_percent_data

        return virtual_memory_data

