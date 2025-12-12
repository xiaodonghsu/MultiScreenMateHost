import json
import os

class SceneSwitch():
    def __init__(self, config_file: str = None):
        if config_file is None:
            current_dir = os.path.split(os.path.abspath(__file__))[0]
            with open(os.path.join(current_dir, "scene_config_path.txt"), 'r') as f:
                config_file = f.read().strip()
        if not os.path.exists(config_file):
            print("当前路径:", os.getcwd(), "不存在的文件:", config_file)
            raise FileNotFoundError(f"Config file not found: {config_file}")
        self.config_file = config_file
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Config file not found: {config_file}")

    def load_config(self):
        with open(self.config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
        return config

    def dump_config(self, config):
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)

def switchScene():
    ss = SceneSwitch()
    config = ss.load_config()
    ipnt = 0
    previous_scene = config["scene_active"]
    new_scene = ""
    for item in config["scene_list"]:
        if config["scene_active"] == item["name"]:
            ipnt += 1
            ipnt = ipnt % len(config["scene_list"])
            new_scene = config["scene_list"][ipnt]["name"]
            config["scene_active"] = new_scene
            ss.dump_config(config)
            break
        ipnt += 1
    return "Scene Switched: %s -> %s" % (previous_scene, new_scene)
