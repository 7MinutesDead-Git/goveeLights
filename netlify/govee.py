import requests
import govee_config

# ------------------------------------------------------------------------------
# Static variables.
header = {"Govee-API-Key": govee_config.apiKey}
govee_dev_url = "https://developer-api.govee.com/"
device_info = "v1/devices"


# ------------------------------------------------------------------------------
class GoveeLight:
    def __init__(self, device_response):
        self.state = None
        self.response = device_response
        self.model       = self.response["model"]
        self.light_name  = self.response["deviceName"]
        self.retrievable = self.response["retrievable"]
        self.commands    = self.response["supportCmds"]
        self.device     = self.response["device"]
        self.status = {
            "device": self.device,
            "model": self.model
        }
        self.cmd = {
            "device": self.device,
            "model": self.model,
            "cmd": {"name": "", "value": ""}
            }

    # -------------------------------------
    def set_toggle(self):
        self.cmd['cmd']['name'] = "turn"

        if self.state['data']['properties'][1]['powerState'] == "on":
            self.cmd["cmd"]["value"] = "off"
        else:
            self.cmd["cmd"]["value"] = "on"

    def set_brightness(self, value):
        self.cmd['cmd']['name'] = "brightness"
        self.cmd['cmd']['value'] = value

    # -------------------------------------
    def send_command(self, cmd_name=""):
        request = requests.put(f"{govee_dev_url}{device_info}/control", headers=header, json=self.cmd).json()
        print(f'Send command {cmd_name}: {request["message"]}')
        print(self.cmd)

    # -------------------------------------
    def get_state(self):
        self.state = requests.get(f"{govee_dev_url}{device_info}/state", headers=header, params=self.status).json()
        print(f'Get {self.light_name} state: {self.state["message"]}')


# ------------------------------------------------------------------------------
# Static functions.
# ---------------------------
def get_all_lights():
    lights = []
    devices_request = requests.get(f"{govee_dev_url}{device_info}", headers=header)
    devices_list = devices_request.json()["data"]["devices"]

    for light in devices_list:
        lights.append(GoveeLight(light))

    get_light_states(lights)
    return lights


# ---------------------------
def get_light_states(lights):
    for light in lights:
        light.get_state()
        print(f"{light.light_name} is {light.state['data']['properties'][1]['powerState']}.")


# ---------------------------
def toggle_lights(lights):
    for light in lights:
        light.set_toggle()
        light.send_command("toggle")
        print(f"    - {light.light_name} is now {light.state['data']['properties'][1]['powerState']}.")


# ---------------------------
def set_brightness(lights, value):
    for light in lights:
        light.set_brightness(value)
        light.send_command("set brightness")
        print(f"    - {light.light_name} brightness set to {value}.")


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    all_lights = get_all_lights()
    set_brightness(all_lights, 40)
