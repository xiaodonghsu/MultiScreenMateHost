import json
import os

class WorkModeSwitch():
    def __init__(self, config_file: str = r"..\slide_avatar_cooperate\monitor_service\config.json"):
        if not os.path.exists(config_file):
            print("当前路径:", os.getcwd(), "不存在的文件:", config_file)
            raise FileNotFoundError(f"Config file not found: {config_file}")
        self.config_file = config_file
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Config file not found: {config_file}")
        self.work_modes = ["collaboration", "auto", "manual"]
        self.__config_work_mode_name__ = "work_mode"

    def load_config(self):
        with open(self.config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
        return config

    def dump_config(self, config):
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

    def switch_mode(self, work_mode: str):
        '''
        切换工作模式: collaboration/auto/manual        
        :param mode: collaboration/auto/manual        
        '''
        if work_mode not in self.work_modes:
            return f"Invalid mode. Available modes are: {', '.join(self.work_modes)}"

        config = self.load_config()

        if config[self.__config_work_mode_name__] == work_mode:
            return f"Already in {work_mode} mode."

        config[self.__config_work_mode_name__] = work_mode
        
        self.dump_config(config)

        return f"Switched work mode to: {work_mode}"

def switchWorkModeToManual():
    wms = WorkModeSwitch()
    return wms.switch_mode("manual")

def switchWorkModeToAuto():
    wms = WorkModeSwitch()
    return wms.switch_mode("auto")

def switchWorkModeToCollaboration():
    wms = WorkModeSwitch()
    return wms.switch_mode("collaboration")
