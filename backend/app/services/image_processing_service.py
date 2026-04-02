from dataclasses import dataclass
from io import BytesIO

from PIL import Image, ImageOps
from rembg import remove


@dataclass
class ProcessedImage:
    content: bytes
    mime_type: str
    extension: str


class ImageProcessingService:
    @staticmethod
    def _apply_operations(image: Image.Image, options: dict) -> Image.Image:
        crop_x = options.get("crop_x")
        crop_y = options.get("crop_y")
        crop_width = options.get("crop_width")
        crop_height = options.get("crop_height")

        if all(value is not None for value in [crop_x, crop_y, crop_width, crop_height]):
            left = max(0, int(crop_x))
            top = max(0, int(crop_y))
            right = left + max(1, int(crop_width))
            bottom = top + max(1, int(crop_height))
            image = image.crop((left, top, right, bottom))

        resize_width = options.get("resize_width")
        resize_height = options.get("resize_height")
        if resize_width and resize_height:
            image = ImageOps.contain(
                image,
                (int(resize_width), int(resize_height)),
                method=Image.Resampling.LANCZOS,
            )

        fit_width = options.get("fit_width")
        fit_height = options.get("fit_height")
        if fit_width and fit_height:
            fit_size = (int(fit_width), int(fit_height))
            fitted = ImageOps.contain(image, fit_size, method=Image.Resampling.LANCZOS)
            canvas = Image.new("RGBA", fit_size, (0, 0, 0, 0))
            x = (fit_size[0] - fitted.width) // 2
            y = (fit_size[1] - fitted.height) // 2
            canvas.paste(fitted, (x, y), fitted)
            image = canvas

        return image

    @classmethod
    def remove_background(cls, image_bytes: bytes, options: dict) -> ProcessedImage:
        result = remove(image_bytes)
        image = Image.open(BytesIO(result)).convert("RGBA")
        image = cls._apply_operations(image, options)

        output_format = str(options.get("output_format", "png")).lower()
        if output_format not in {"png", "jpeg", "webp"}:
            output_format = "png"

        buffer = BytesIO()
        if output_format == "jpeg":
            rgb_image = Image.new("RGB", image.size, (255, 255, 255))
            rgb_image.paste(image, mask=image.split()[-1])
            rgb_image.save(buffer, format="JPEG", quality=92, optimize=True)
            mime_type = "image/jpeg"
            extension = "jpg"
        elif output_format == "webp":
            image.save(buffer, format="WEBP", quality=90, method=6)
            mime_type = "image/webp"
            extension = "webp"
        else:
            image.save(buffer, format="PNG", optimize=True)
            mime_type = "image/png"
            extension = "png"

        return ProcessedImage(content=buffer.getvalue(), mime_type=mime_type, extension=extension)
