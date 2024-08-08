import sys
import os
import io
import functools

from PIL import Image as PilImage
from PIL import ImageDraw as PilImageDraw
from PIL import ImageFont as PilImageFont

from ... import aiotools


# =====
async def make_text_jpeg(width: int, height: int, quality: int, text: str) -> bytes:
    return (await aiotools.run_async(_inner_make_text_jpeg, width, height, quality, text))


@functools.lru_cache(maxsize=10)
def _inner_make_text_jpeg(width: int, height: int, quality: int, text: str) -> bytes:
    image = PilImage.new("RGB", (width, height), color=(0, 0, 0))
    draw = PilImageDraw.Draw(image)
    draw.multiline_text((20, 20), text, font=_get_font(), fill=(255, 255, 255))
    with io.BytesIO() as bio:
        image.save(bio, format="jpeg", quality=quality)
        return bio.getvalue()


@functools.lru_cache()
def _get_font() -> PilImageFont.FreeTypeFont:
    module_path = sys.modules[__name__].__file__
    assert module_path is not None
    path = os.path.join(os.path.dirname(module_path), "fonts", "Azbuka04.ttf")
    return PilImageFont.truetype(path, size=20)
