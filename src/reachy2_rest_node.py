#!/usr/bin/env python3
"""REST node for the Reachy2 bimanual robot."""

from typing import Annotated, Optional

from madsci.common.types.action_types import ActionFailed
from madsci.common.types.node_types import RestNodeConfig
from madsci.node_module.helpers import action
from madsci.node_module.rest_node_module import RestNode
from madsci.common.types.location_types import LocationArgument
from pathlib import Path
from reachy2_interface import Reachy2Interface


        #  "right_wrist_right": {"type": "opencv", "index_or_path": "/dev/video3", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}

class Reachy2NodeConfig(RestNodeConfig):
    """Configuration for the Reachy2 node module."""

    reachy2_ip: str = "localhost"
    reachy2_port: int = "50065"


class Reachy2Node(RestNode):
    """A Rest Node object to control the Reachy2 bimanual robot."""

    robot: Optional[Reachy2Interface] = None
    config: Reachy2NodeConfig = Reachy2NodeConfig()
    config_model = Reachy2NodeConfig

    def startup_handler(self) -> None:
        """Called to (re)initialize the node. """
        
        self.logger.log_info("Reachy2 Node initialized.")
        self.robot = Reachy2Interface(self.config.reachy2_ip, self.config.reachy2_port)

    def shutdown_handler(self) -> None:
        """Called to shutdown the node. Disables both arms and releases CAN resources."""
        try:
            if self.robot is not None:
                self.robot.shutdown()
                del self.robot
                self.robot = None
        except Exception as err:
            self.logger.log_error(f"Error shutting down the Reachy2 Node: {err}")
            raise err

    def state_handler(self) -> None:
        """Periodically called to update the current state of the node."""
        try:
            if self.robot is not None:
                observation = self.robot.get_observation()
                print(observation)
                self.node_state = observation
        except Exception as err:
                    self.logger.log_error(f"Error shutting down the Reachy2 Node: {err}")
                    print(err)
                    raise err
    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    @action
    def move_to_position(self, position: Annotated[LocationArgument, "the target location to move to"]) -> None:
            """replay a pretrained teleop trajectory"""
            self.robot.send_action(position.representation)


    @action
    def set_speeds(self, speeds: Annotated[list[float], "[vx, vy, vtheta]"]):
         """set the mobile base speeeds"""
         pos = self.robot.get_observation()
         pos["mobile_base.vx"] = speeds[0]
         pos["mobile_base.vy"] = speeds[1]
         pos["mobile_base.vtheta"] = speeds[2]
         self.robot.send_action(pos)

    @action
    def stop(self):
         """stop all base motion"""
         pos = self.robot.get_observation()
         pos["mobile_base.vx"] = 0
         pos["mobile_base.vy"] = 0
         pos["mobile_base.vtheta"] = 0
         self.robot.send_action(pos)

         
    

    @action
    def replay(self, repo_id: Annotated[str, "lerobot repo id for the episode"], episode: Annotated[int, "lerobot episode number to replay"], fps: int = 30) -> None:
        """replay a pretrained teleop trajectory"""
        self.robot.replay_example(repo_id, episode, self.config.dataset_root, fps)

    @action
    def rollout(self, policy_path: Annotated[str, "path to the folder containg the policies config.json"], task: Annotated[str, "the task to perform"], duration: Annotated[int, "the duration of the rollout in seconds"]) -> None:
        self.robot.rollout(policy_path, task, duration)
   


if __name__ == "__main__":
    reachy2_node = Reachy2Node()
    reachy2_node.start_node()