from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import asyncio
import av
import aiortc
from aiortc import RTCPeerConnection, RTCSessionDescription, MediaStreamTrack
from aiortc.contrib.media import MediaPlayer
import logging
import cv2
import numpy as np
from src.services.camera import CameraManager

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory='src/templates')

# Храним активные соединения
pcs = set()

camera_manager = CameraManager()

class VideoTransformTrack(MediaStreamTrack):
    kind = "video"

    def __init__(self, track):
        super().__init__()
        self.track = track

    async def recv(self):
        frame = await self.track.recv()
        img = frame.to_ndarray(format="bgr24")
        height, width = img.shape[:2]
        color = (0, 255, 0)
        thickness = 2
        size = 20
        center_x = width // 2
        center_y = height // 2
        
        cv2.line(img, 
                 (center_x - size, center_y),
                 (center_x + size, center_y),
                 color,
                 thickness)
        cv2.line(img, 
                 (center_x, center_y - size),
                 (center_x, center_y + size),
                 color,
                 thickness)
        
        new_frame = av.VideoFrame.from_ndarray(img, format="bgr24")
        new_frame.pts = frame.pts
        new_frame.time_base = frame.time_base
        
        return new_frame

@router.get('/stream', response_class=HTMLResponse)
async def stream(request: Request):
    return templates.TemplateResponse('stream.html', {'request': request})

@router.get('/stream/api/search_stream')
async def search_stream():
    """Получение списка активных камер"""
    try:
        logger.info("Searching for active cameras...")
        active_cameras = await camera_manager.get_active_cameras()
        logger.info(f"Found {len(active_cameras)} active cameras")
        return {'streams': active_cameras}
    except Exception as e:
        logger.error(f"Error getting active cameras: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stream/offer")
async def offer(params: dict):
    logger.info(f"Received offer for stream: {params['stream_url']}")
    
    try:
        offer = RTCSessionDescription(
            sdp=params["sdp"],
            type=params["type"]
        )
        
        pc = RTCPeerConnection()
        pcs.add(pc)

        player = MediaPlayer(params["stream_url"])
        
        @pc.on("connectionstatechange")
        async def on_connectionstatechange():
            logger.info(f"Connection state changed to: {pc.connectionState}")
            if pc.connectionState == "failed":
                await pc.close()
                pcs.discard(pc)

        if player.video:
            video_processor = VideoTransformTrack(player.video)
            pc.addTrack(video_processor)

        await pc.setRemoteDescription(offer)
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)

        logger.info("Successfully created WebRTC answer")
        return {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
    
    except Exception as e:
        logger.error(f"Error processing offer: {str(e)}")
        raise

async def close_connections():
    """Функция для закрытия всех WebRTC соединений"""
    logger.info("Closing all WebRTC connections...")
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()