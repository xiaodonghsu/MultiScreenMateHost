import json
import os

class AvatarSwitch():
    def __init__(self, config_file: str = None):
        if config_file is None:
            current_dir = os.path.split(os.path.abspath(__file__))[0]
            with open(os.path.join(current_dir, "monitor_config_path.txt"), 'r') as f:
                config_file = f.read().strip()
        if not os.path.exists(config_file):
            print("当前路径:", os.getcwd(), "不存在的文件:", config_file)
            raise FileNotFoundError(f"Config file not found: {config_file}")
        self.config_file = config_file
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Config file not found: {config_file}")
        self.commands = ["play/pause", "stop", "text"]
        self.__config_command_name__ = "avatar_command"
        self.__config_command_response_name__ = "avatar_command_response"

    def load_config(self):
        with open(self.config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
        return config

    def dump_config(self, config):
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)

    def is_command_response_success(self, config):
        return config[self.__config_command_response_name__]["result"] == "success"

    def switch_status(self, command: str = None, text: str = None):
        '''
        切换数字人的状态: play/pause, stop, text
        str -> None 根据当前的状态进行切换
        str -> ["play/pause", "stop", "text"] 切换到指定的状态
        :param command: play/pause, stop, text        
        '''
        if command is None:
            command = "play/pause"

        if command not in self.commands:
            return f"Invalid command. Available commands are: {', '.join(self.commands)}"

        config = self.load_config()
        if command == "play/pause":
            config[self.__config_command_name__]["command"] = command
            config[self.__config_command_response_name__] = {"result": "issue"}
        elif command == "stop":
            config[self.__config_command_name__]["command"] = command
            config[self.__config_command_response_name__] = {"result": "issue"}
        elif command == "text":
            if text is None:
                return "text command needs text parameter."
            else:
                config[self.__config_command_name__]["command"] = command
                config[self.__config_command_name__]["text"] = text
                config[self.__config_command_response_name__] = {"result": "issue"}
        self.dump_config(config)

        # config = self.load_config()

        # if config[self.__config_command_name__]["command"] == command:
        #     if self.is_command_response_success():
        #         return f"Already in {command} command."

        # config[self.__config_command_name__]["command"] = command
        # config[self.__config_command_response_name__] = {"result": "issue"}
        # self.dump_config(config)

        # return f"Send avatar command: {command}"
            
        # else:
        #     config = self.load_config()

        #     if config[self.__config_command_name__]["command"] not in self.commands:
        #         print("invalid command:", config[self.__config_command_name__]["command"])
        #         config[self.__config_command_name__]["command"] = "play"
        #         config[self.__config_command_response_name__] = {"result": "issue"}
    
        #     if config[self.__config_command_name__]["command"] == "play":
        #         config[self.__config_command_name__]["command"] = "pause"
        #         config[self.__config_command_response_name__] = {"result": "issue"}
        #     elif config[self.__config_command_name__]["command"] == "pause":
        #         config[self.__config_command_name__]["command"] = "play"
        #         config[self.__config_command_response_name__] = {"result": "issue"}

        #     # with open(self.config_file, "w", encoding="utf-8") as f:
        #     #     json.dump(config, f, ensure_ascii=False, indent=4)
            
        #     self.dump_config(config)
        return f"Switched work command to: {config[self.__config_command_name__]}"

def switchAvatarStatus():
    avs = AvatarSwitch()
    return avs.switch_status()

def switchAvatarStatusToStop():
    avs = AvatarSwitch()
    return avs.switch_status("stop")

def sendAvatarText(text):
    avs = AvatarSwitch()
    return avs.switch_status(command="text", text=text)