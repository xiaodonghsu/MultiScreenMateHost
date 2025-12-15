import json
import os

class SceneSwitch():
    def __init__(self, config_file: str = None):
        self.__CONFIG_FILE = "slide_monitor_running_config.json"
        if config_file is None:
            temp_path = os.getenv('TEMP')
            config_file = os.path.join(temp_path, self.__CONFIG_FILE)
        if not os.path.exists(config_file):
            print("当前路径:", os.getcwd(), "不存在的文件:", config_file)
            raise FileNotFoundError(f"Config file not found: {config_file}")
        self.config_file = config_file
        self.__config_active_scene_name__ = "active_scene"
        self.__config_active_scene_response_name__ = "active_scene_response"

    def load_config(self):
        with open(self.config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
        return config

    def dump_config(self, config):
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)

    def switchScene(self):
        config = self.load_config()
        if self.is_active_scene_response_success(config):
            config[self.__config_active_scene_name__] = "next"
            config[self.__config_active_scene_response_name__] =  {"result": "issue"}
            self.dump_config(config)
            return "Scene Switch: %s -> %s" % (previous_scene, new_scene)
        else:
            return "Previous Scene not switched!"

    def is_active_scene_response_success(self, config):
        return config[self.__config_active_scene_response_name__]["result"] == "success"

def switchScene():
    ss = SceneSwitch()
    return ss.switchScene()