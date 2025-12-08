import json
import os

class AvatarSwitch():
    def __init__(self, config_file: str = r"..\slide_avatar_cooperate\monitor_service\config.json"):
        if not os.path.exists(config_file):
            print("当前路径:", os.getcwd(), "不存在的文件:", config_file)
            raise FileNotFoundError(f"Config file not found: {config_file}")
        self.config_file = config_file
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Config file not found: {config_file}")
        self.commands = ["play", "pause", "stop"]
        self.__config_command_name__ = "avatar_command"

    def load_config(self):
        with open(self.config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
        return config

    def dump_config(self, config):
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

    def switch_status(self, command: str = None):
        '''
        切换数字人的状态: play, pause, stop
        str -> None 根据当前的状态进行切换
        str -> ["play", "pause", "stop"] 切换到指定的状态
        :param command: play/pause/stop        
        '''
        if not command is None:
            
            if command not in self.commands:
                return f"Invalid command. Available commands are: {', '.join(self.commands)}"

            config = self.load_config()

            if config[self.__config_command_name__] == command:
                return f"Already in {command} command."

            config[self.__config_command_name__] = command

            self.dump_config(config)

            return f"Switched work command to: {command}"
            
        else:
            config = self.load_config()

            if config[self.__config_command_name__] not in self.commands:
                print("invalid command:", config[self.__config_command_name__])
                config[self.__config_command_name__] = "play"
            
            if config[self.__config_command_name__] == "play":
                config[self.__config_command_name__] = "pause"
            elif config[self.__config_command_name__] == "pause":
                config[self.__config_command_name__] = "play"

            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            
            self.dump_config(config)
            return f"Switched work command to: {config[self.__config_command_name__]}"

def switchAvatarStatus():
    avs = AvatarSwitch()
    return avs.switch_status()

def switchAvatarStatusToStop():
    avs = AvatarSwitch()
    return avs.switch_status("stop")
