import uuid
from PIL import Image

def resize_image(image_path, size=(300, 300)):
    """Resizes an image to the specified size."""
    img = Image.open(image_path)
    if img.height > size[0] or img.width > size[1]:
        img.thumbnail(size)
        img.save(image_path)

def unique_filename(instance, filename):
    """Generates a unique filename for uploaded images."""
    ext = filename.split('.')[-1]
    unique_name = uuid.uuid4().hex
    return f'{instance._meta.app_label}/{instance._meta.model_name}/{unique_name}.{ext}'