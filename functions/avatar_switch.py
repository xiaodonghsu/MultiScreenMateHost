import json
import os

class AvatarSwitch():
    def __init__(self, config_file: str = r"D:\Files\Documents\Project\yancheng_playground\slide_avatar_v5\monitor_service\config.json"):
        self.config_file = config_file
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Config file not found: {config_file}")
        self.statuses = ["play", "pause", "stop"]
        self.__config_status_name__ = "avatar_status"

    def load_config(self):
        with open(self.config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
        return config

    def dump_config(self, config):
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

    def switch_status(self, status: str = None):
        '''
        切换数字人的状态: play, pause, stop
        str -> None 根据当前的状态进行切换
        str -> ["play", "pause", "stop"] 切换到指定的状态
        :param status: play/pause/stop        
        '''
        if not status is None:
            
            if status not in self.statuses:
                return f"Invalid status. Available statuses are: {', '.join(self.statuses)}"

            config = self.load_config()

            if config[self.__config_status_name__] == status:
                return f"Already in {status} status."

            config[self.__config_status_name__] = status

            self.dump_config(config)

            return f"Switched work status to: {status}"
            
        else:
            config = self.load_config()

            if config[self.__config_status_name__] == "play":
                config[self.__config_status_name__] = "pause"
            elif config[self.__config_status_name__] == "pause":
                config[self.__config_status_name__] = "play"

            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            
            self.dump_config(config)
            return f"Switched work status to: {config[self.__config_status_name__]}"


def switchAvatarStatus():
    avs = AvatarSwitch()
    return avs.switch_status()

def switchAvatarStatusToStop():
    avs = AvatarSwitch()
    return avs.switch_status("stop")
