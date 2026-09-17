from lerobot.robots.reachy2.robot_reachy2 import Reachy2Robot
from lerobot.robots.reachy2.configuration_reachy2 import Reachy2RobotConfig
from lerobot.scripts.lerobot_replay import replay, ReplayConfig, DatasetReplayConfig
from lerobot.configs import PreTrainedConfig
from lerobot.rollout import BaseStrategyConfig, RolloutConfig
from lerobot.utils.process import ProcessSignalHandler
from lerobot.rollout.strategies import BaseStrategy
from lerobot.rollout.inference import SyncInferenceConfig
from lerobot.rollout import build_rollout_context
from pathlib import Path
import datetime
from datetime import timedelta
import time


class Reachy2Interface:
    def __init__(self, reachy_ip: str, reachy_port: int):
        self.config = Reachy2RobotConfig(ip_address=reachy_ip, port=reachy_port, use_external_commands=False)
        self.robot = Reachy2Robot(self.config)
        self.robot.connect()
    

    def send_action(self, target_location: dict):
       
        self.robot.send_action(target_location)
        

    def get_observation(self):
        return self.robot.get_observation()
    
    def replay_example(self, repo_id: str, episode: int, repo_path: Path, fps: int = 30):
        dataset_config = DatasetReplayConfig(repo_id = repo_id, episode=episode, root=repo_path, fps=fps)
        replay_config = ReplayConfig(robot = self.config, dataset=dataset_config)
        replay(replay_config)


    def rollout(self, policy_path: str, task: str, duration: int):
        policy_config = PreTrainedConfig.from_pretrained(Path(policy_path))
        policy_config.pretrained_path = policy_path
        config = RolloutConfig(robot=self.config, strategy=BaseStrategyConfig(), inference=SyncInferenceConfig(), policy=policy_config, task=task, duration=duration)
        signal_handler = ProcessSignalHandler(use_threads=True)
        context = build_rollout_context(config, signal_handler.shutdown_event)
        strategy = BaseStrategy(config.strategy)
        error = None
        try:
            strategy.setup(context)
            strategy.run(context)
        except Exception as e:
            error  = e
        finally:
            strategy.teardown(context)
            if error is not None:
                raise error
    

