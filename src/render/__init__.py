"""AI NEWS FACTORY — Modular Production Render Engine.

Provides automated synthesis, subtitle authoring, asset registration,
and FFmpeg timeline compositing for vertical 9:16 technical AI news shorts.
"""

from .audio import AudioEngine
from .subtitles import SubtitleEngine
from .assets import AssetEngine
from .compositor import VideoCompositor
from .validate_render import RenderValidator

def __getattr__(name: str):
    if name == "RenderPipeline":
        from .render_pipeline import RenderPipeline
        return RenderPipeline
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = [
    "AudioEngine",
    "SubtitleEngine",
    "AssetEngine",
    "VideoCompositor",
    "RenderValidator",
    "RenderPipeline",
]

