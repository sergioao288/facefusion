import subprocess
import pytest

import facefusion.globals
from facefusion.utilities import conditional_download
from facefusion.vision import detect_fps


@pytest.fixture(scope = 'module', autouse = True)
def before_all() -> None:
	facefusion.globals.temp_frame_quality = 100
	facefusion.globals.trim_frame_start = None
	facefusion.globals.trim_frame_end = None
	facefusion.globals.temp_frame_format = 'png'
	conditional_download('.assets/examples',
	[
		'https://github.com/facefusion/facefusion-assets/releases/download/examples/source.jpg',
		'https://github.com/facefusion/facefusion-assets/releases/download/examples/target-240p.mp4'
	])
	subprocess.run([ 'ffmpeg', '-i', '.assets/examples/target-240p.mp4', '-vf', 'fps=25', '.assets/examples/target-240p-25fps.mp4' ])
	subprocess.run([ 'ffmpeg', '-i', '.assets/examples/target-240p.mp4', '-vf', 'fps=30', '.assets/examples/target-240p-30fps.mp4' ])
	subprocess.run([ 'ffmpeg', '-i', '.assets/examples/target-240p.mp4', '-vf', 'fps=60', '.assets/examples/target-240p-60fps.mp4' ])


@pytest.fixture(scope = 'function', autouse = True)
def before_each() -> None:
	facefusion.globals.trim_frame_start = None
	facefusion.globals.trim_frame_end = None
	facefusion.globals.temp_frame_quality = 90
	facefusion.globals.temp_frame_format = 'jpg'


def test_detect_fps() -> None:
	assert detect_fps('.assets/examples/target-240p-25fps.mp4') == 25.0
	assert detect_fps('.assets/examples/target-240p-30fps.mp4') == 30.0
	assert detect_fps('.assets/examples/target-240p-60fps.mp4') == 60.0