from dotenv import load_dotenv
from imagekitio import ImageKit
import os
import logging

logger = logging.getLogger(__name__)

load_dotenv()

private_key = os.getenv("IMAGEKIT_PRIVATE_KEY")
if not private_key:
    logger.warning("IMAGEKIT_PRIVATE_KEY not found in environment variables")

imageKit = ImageKit(
    private_key=private_key,
)
