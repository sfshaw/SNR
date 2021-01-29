from typing import Any, Dict

from snr.snr_core.base import *
from snr.snr_std.camera.config import CameraConfig, ManagerRole
from snr.snr_std.camera.factory import VideoReceiverFactory, VideoSourceFactory

INITIAL_PORT = 8000
CAMERA_MANAGER_TICK_HZ = 1


class CameraManager(ThreadLoop):
    def __init__(self,
                 factory: LoopFactory,
                 parent: NodeProtocol,
                 name: str,
                 role: ManagerRole,
                 camera_map: Dict[str, int]
                 ) -> None:
        super().__init__(factory, parent, name,
                         CAMERA_MANAGER_TICK_HZ)
        self.role = role
        self.camera_map = camera_map
        self.num_cameras = len(camera_map.keys())
        self.cam_num = 0  # Cameras which have been allocated
        self.port = INITIAL_PORT
        self.cameras = []

        # self.pool = Pool(num_cameras)

        # if role is ManagerRole.Receiver:

        #     return CameraManager(parent, name)
        # elif role is ManagerRole.Source:

        #     return CameraManager(parent, name)
        # else:
        #     self.err("Unknown camera manager role {}",
        #         [role])

        # self.start_loop()

    def setup(self):
        fac: Any = no_op
        if self.role is ManagerRole.Source:
            fac = VideoSourceFactory
        elif self.role is ManagerRole.Receiver:
            fac = VideoReceiverFactory

        # Create each camera process from pool
        for camera_name in self.camera_map.keys():
            config = CameraConfig(camera_name,
                                  self.next_port(),
                                  self.camera_map[camera_name])
            f = fac(config)
            cam = f.get(self, self.parent)
            self.cameras.append(cam)
            self.dbg("Created camera {}", [cam])

    def loop_handler(self):
        pass

    def terminate(self):
        self.dbg("camera_manager", "Joining managed camera processes")
        # for proc_endpoint in self.cameras:
        #     proc_endpoint.set_terminate_flag()
        for proc_endpoint in self.cameras:
            proc_endpoint.join()

    def next_port(self):
        val = self.port
        self.port += 2
        self.cam_num += 1
        self.dbg("Allocating port {} for camera {}",
                 [val, self.cam_num])
        return val

    def __repr__(self):
        return f"Camera {str(self.role)} Manager"
