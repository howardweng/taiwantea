"""Media server integration service"""

import httpx
from typing import Dict, Optional
from src.config import settings
from src.logger import logger


class MediaServerError(Exception):
    """Custom exception for media server errors"""
    pass


async def upload_to_media_server(
    file_content: bytes,
    filename: str,
    max_retries: int = 3,
    timeout: int = 30
) -> Dict[str, str]:
    """
    Upload a file to the media server

    Args:
        file_content: File content as bytes
        filename: Original filename
        max_retries: Maximum number of retry attempts (default: 3)
        timeout: Request timeout in seconds (default: 30)

    Returns:
        Dict with imageUrl, thumbnailUrl, smImageUrl, and filename

    Raises:
        MediaServerError: If upload fails after retries
    """
    url = f"{settings.MEDIA_SERVER_URL}{settings.MEDIA_SERVER_UPLOAD_ENDPOINT}"

    # Prepare multipart form data
    files = {
        'file': (filename, file_content)
    }

    last_error = None

    # Retry logic
    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"Uploading to media server (attempt {attempt}/{max_retries}): {filename}")

            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(url, files=files)
                response.raise_for_status()

                # Parse response
                data = response.json()

                # Validate response
                if not validate_media_server_response(data):
                    raise MediaServerError(f"Invalid response from media server: {data}")

                # Extract URLs
                result = {
                    "imageUrl": data.get("imgUrl"),
                    "thumbnailUrl": data.get("thumbnailUrl"),
                    "smImageUrl": data.get("smImgUrl"),
                    "filename": data.get("fileName")
                }

                logger.info(f"Successfully uploaded to media server: {result['filename']}")
                return result

        except httpx.TimeoutException as e:
            last_error = e
            logger.warning(f"Timeout uploading to media server (attempt {attempt}/{max_retries}): {str(e)}")

        except httpx.HTTPError as e:
            last_error = e
            logger.warning(f"HTTP error uploading to media server (attempt {attempt}/{max_retries}): {str(e)}")

        except Exception as e:
            last_error = e
            logger.error(f"Unexpected error uploading to media server (attempt {attempt}/{max_retries}): {str(e)}")

        # Don't retry on last attempt
        if attempt < max_retries:
            logger.info(f"Retrying upload... ({attempt + 1}/{max_retries})")

    # All retries failed
    error_msg = f"Failed to upload to media server after {max_retries} attempts: {str(last_error)}"
    logger.error(error_msg)
    raise MediaServerError(error_msg)


def validate_media_server_response(response: Dict) -> bool:
    """
    Validate that the media server response has all required fields

    Args:
        response: Response dict from media server

    Returns:
        True if valid, False otherwise
    """
    required_fields = ["imgUrl", "thumbnailUrl", "smImgUrl", "fileName"]

    for field in required_fields:
        if field not in response or not response[field]:
            logger.error(f"Media server response missing required field: {field}")
            return False

    # Validate URLs are actually URLs
    for url_field in ["imgUrl", "thumbnailUrl", "smImgUrl"]:
        url = response[url_field]
        if not url.startswith("http://") and not url.startswith("https://"):
            logger.error(f"Media server response has invalid URL for {url_field}: {url}")
            return False

    return True
