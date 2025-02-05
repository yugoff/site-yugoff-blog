# src/services/camera.py
import yaml
import asyncio
from aiortc.contrib.media import MediaPlayer
import logging
from pathlib import Path
from typing import List, Dict

logger = logging.getLogger(__name__)

class CameraManager:
    def __init__(self):
        # Используем путь относительно текущего файла
        self.config_path = Path(__file__).parent.parent / "cameras.yaml"
        self.cameras: List[Dict] = []
        self.active_cameras: List[Dict] = []
        self._load_config()
        
    def _load_config(self) -> None:
        """Загрузка конфигурации камер из файла"""
        try:
            logger.info(f"Loading camera config from {self.config_path}")
            with open(self.config_path, 'r') as file:
                config = yaml.safe_load(file)
                self.cameras = config.get('cameras', [])
                logger.info(f"Loaded {len(self.cameras)} cameras from config")
        except Exception as e:
            logger.error(f"Error loading camera config: {e}")
            self.cameras = []

    async def check_camera(self, camera: Dict) -> bool:
        """Проверка доступности камеры"""
        try:
            logger.info(f"Checking camera: {camera['name']} at {camera['url']}")
            player = MediaPlayer(camera['url'])
            await asyncio.sleep(1)
            if player.video:
                logger.info(f"Camera {camera['name']} is available")
                return True
            logger.warning(f"Camera {camera['name']} has no video stream")
            return False
        except Exception as e:
            logger.warning(f"Camera {camera['name']} ({camera['url']}) is not available: {e}")
            return False

    async def get_active_cameras(self) -> List[Dict]:
        """Получение списка активных камер"""
        logger.info("Getting active cameras...")
        active_cameras = []
        tasks = []

        for camera in self.cameras:
            task = asyncio.create_task(self.check_camera(camera))
            tasks.append((camera, task))

        for camera, task in tasks:
            try:
                is_active = await task
                if is_active:
                    active_cameras.append(camera)
            except Exception as e:
                logger.error(f"Error checking camera {camera['name']}: {e}")

        logger.info(f"Found {len(active_cameras)} active cameras")
        self.active_cameras = active_cameras
        return active_cameras

    async def add_camera(self, camera_info: Dict) -> bool:
        """Добавление новой камеры в конфигурацию"""
        try:
            logger.info(f"Adding new camera: {camera_info}")
            if await self.check_camera(camera_info):
                self.cameras.append(camera_info)
                config = {'cameras': self.cameras}
                with open(self.config_path, 'w') as file:
                    yaml.safe_dump(config, file)
                logger.info(f"Camera added successfully")
                return True
            return False
        except Exception as e:
            logger.error(f"Error adding camera: {e}")
            return False

    async def remove_camera(self, camera_id: int) -> bool:
        """Удаление камеры из конфигурации"""
        try:
            initial_count = len(self.cameras)
            self.cameras = [cam for cam in self.cameras if cam['id'] != camera_id]
            if len(self.cameras) < initial_count:
                config = {'cameras': self.cameras}
                with open(self.config_path, 'w') as file:
                    yaml.safe_dump(config, file)
                logger.info(f"Camera {camera_id} removed successfully")
                return True
            logger.warning(f"Camera {camera_id} not found")
            return False
        except Exception as e:
            logger.error(f"Error removing camera: {e}")
            return False