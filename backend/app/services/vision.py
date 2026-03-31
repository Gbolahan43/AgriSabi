from fastapi import UploadFile

async def encode_image(file: UploadFile) -> bytes:
    """
    Reads a FastAPI UploadFile and returns its raw bytes for AWS Bedrock Converse API.
    In Phase 2, this will also include image resizing to 1024x1024 
    and EXIF GPS stripping for privacy.
    """
    contents = await file.read()
    return contents

def get_image_media_type(filename: str) -> str:
    """
    Determine the appropriate media type mapping for AWS Bedrock.
    Supported: jpeg, png, webp, gif
    """
    ext = filename.split(".")[-1].lower()
    if ext in ["jpg", "jpeg"]:
        return "jpeg"
    elif ext == "png":
        return "png"
    elif ext == "webp":
        return "webp"
    elif ext == "gif":
        return "gif"
    else:
        return "jpeg"  # Fallback
