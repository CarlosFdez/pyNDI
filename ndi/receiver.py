import enum

import numpy as np

from lib import lib, ffi
from finder import NDISource

class FrameType(enum.IntEnum):
    type_none = 0
    type_video = 1
    type_audio = 2
    type_metadata = 3
    type_error = 4

    # emitted when the type has changed
    type_status_change = 100 

class ColorFormat(enum.IntEnum):
    format_BGRX_BGRA = 0 # No alpha channel: BGRX, Alpha channel: BGRA
    format_UYVY_BGRA = 1 # No alpha channel: UYVY, Alpha channel: BGRA
    format_RGBX_RGBA = 2 # No alpha channel: RGBX, Alpha channel: RGBA
    format_UYVY_RGBA = 3 # No alpha channel: UYVY, Alpha channel: RGBA

class RecvBandwith(enum.IntEnum):
    metadata_only = -10, # Receive metadata.
    audio_only    =  10, # Receive metadata, audio.
    lowest        =  0,  # Receive metadata, audio, video at a lower bandwidth and resolution.
    highest       =  100 # Receive metadata, audio, video at full resolution.

def create_receiver(source: NDISource, *, color_format=ColorFormat.format_BGRX_BGRA, bandwidth=RecvBandwith.highest):
    create_config = ffi.new("NDIlib_recv_create_v3_t *")
    create_config.source_to_connect_to = source.raw
    create_config.color_format = color_format
    create_config.bandwidth = bandwidth
    create_config.allow_video_fields = True
    create_config.p_ndi_recv_name = ffi.NULL

    pNDI_recv = lib.NDIlib_recv_create_v3(create_config)
    receiver = NDIReceiver(pNDI_recv, source)
    return receiver

class NDIReceiver():
    def __init__(self, pNDI_recv, source):
        self.pNDI_recv = pNDI_recv
        self.source = source

        # handle connection here
        lib.NDIlib_recv_connect(pNDI_recv, ffi.addressof(source.raw))

    def __del__(self):
        lib.NDIlib_recv_destroy(self.pNDI_recv)

    def read(self):
        # self note: only one of video frame or audio frame gets read. Gotta check with one
        pNDI_recv = self.pNDI_recv

        video_frame = ffi.new("NDIlib_video_frame_v2_t*")

        # Loop until we get data
        while True:
            res_val = lib.NDIlib_recv_capture_v2(pNDI_recv, video_frame, ffi.NULL, ffi.NULL, 1000)
            
            if res_val == FrameType.type_video:
                width = video_frame.xres
                height = video_frame.yres

                # Note: this should always be 4 * xres
                bytes_per_row = video_frame.line_stride_in_bytes
                total_bytes = bytes_per_row * height
                
                byte_data = np.frombuffer(ffi.buffer(video_frame.p_data, total_bytes))
                new_data = np.ndarray((height, width, 4), dtype=np.uint8, buffer=byte_data)
                new_data = new_data.copy() # prevent seg-fault

                lib.NDIlib_recv_free_video_v2(pNDI_recv, video_frame)
                
                return new_data

