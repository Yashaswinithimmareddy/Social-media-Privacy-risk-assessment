"""
Social Media Privacy Risk Assessment Framework
Local EXIF Photo Metadata Inspector & Sanitizer

Allows users to inspect image metadata (EXIF) locally to understand privacy leakage
risks (such as GPS coordinates, camera models, and timestamps).
Provides an in-memory sanitizer to strip all metadata before sharing photos.
Zero external transmission; all processing is local and defensive.
"""

import io
from typing import Dict, Any, Optional
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def convert_to_degrees(value) -> float:
    """Helper function to convert GPS coordinates stored in EXIF to decimal degrees."""
    try:
        d = float(value[0])
        m = float(value[1])
        s = float(value[2])
        return d + (m / 60.0) + (s / 3600.0)
    except Exception:
        return 0.0

def extract_exif_metadata(image_bytes: bytes) -> Dict[str, Any]:
    """
    Parses EXIF metadata from raw image bytes.
    Extracts camera info, timestamps, and GPS coordinates if present.
    """
    result: Dict[str, Any] = {
        "has_exif": False,
        "format": "Unknown",
        "dimensions": "Unknown",
        "camera_make": None,
        "camera_model": None,
        "datetime_original": None,
        "software": None,
        "gps_latitude": None,
        "gps_longitude": None,
        "gps_altitude": None,
        "raw_tags": {},
        "privacy_warning": None
    }

    try:
        image = Image.open(io.BytesIO(image_bytes))
        result["format"] = image.format or "Unknown"
        result["dimensions"] = f"{image.width} x {image.height} px"

        exif_data = image.getexif()
        if not exif_data:
            result["privacy_warning"] = "Safe: No EXIF metadata detected in this image."
            return result

        result["has_exif"] = True
        raw_tags = {}
        gps_info = {}

        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, str(tag_id))
            # Convert binary or non-serializable data to string
            if isinstance(value, bytes):
                try:
                    value = value.decode("utf-8", errors="ignore")
                except Exception:
                    value = str(value)
            
            raw_tags[tag_name] = str(value)

            if tag_name == "Make":
                result["camera_make"] = str(value).strip()
            elif tag_name == "Model":
                result["camera_model"] = str(value).strip()
            elif tag_name == "DateTime":
                result["datetime_original"] = str(value).strip()
            elif tag_name == "Software":
                result["software"] = str(value).strip()
            elif tag_name == "GPSInfo":
                gps_info = value

        result["raw_tags"] = raw_tags

        # Try parsing GPS IFD
        try:
            from PIL.ExifTags import IFD
            gps_ifd = exif_data.get_ifd(IFD.GPSInfo)
            if gps_ifd:
                lat_ref = gps_ifd.get(1)
                lat = gps_ifd.get(2)
                lon_ref = gps_ifd.get(3)
                lon = gps_ifd.get(4)
                alt = gps_ifd.get(6)

                if lat and lat_ref:
                    deg_lat = convert_to_degrees(lat)
                    if lat_ref == 'S':
                        deg_lat = -deg_lat
                    result["gps_latitude"] = round(deg_lat, 6)

                if lon and lon_ref:
                    deg_lon = convert_to_degrees(lon)
                    if lon_ref == 'W':
                        deg_lon = -deg_lon
                    result["gps_longitude"] = round(deg_lon, 6)

                if alt:
                    result["gps_altitude"] = f"{float(alt):.1f} meters"
        except Exception:
            pass

        # Evaluate privacy warning
        if result["gps_latitude"] is not None and result["gps_longitude"] is not None:
            result["privacy_warning"] = (
                f"HIGH PRIVACY RISK: Image contains exact GPS coordinates "
                f"({result['gps_latitude']}, {result['gps_longitude']}). "
                f"Sharing this photo directly will expose your physical location."
            )
        elif result["camera_model"] or result["datetime_original"]:
            result["privacy_warning"] = (
                f"MODERATE EXPOSURE: Image contains device identifiers ({result['camera_model']}) "
                f"and timestamp ({result['datetime_original']})."
            )
        else:
            result["privacy_warning"] = "Low Exposure: Basic image metadata present, but no GPS detected."

    except Exception as e:
        result["error"] = f"Failed to parse image metadata: {str(e)}"

    return result


def strip_exif_metadata(image_bytes: bytes) -> bytes:
    """
    Sanitizes an image by removing all EXIF and metadata blocks.
    Re-encodes the image pixels cleanly in memory.
    """
    image = Image.open(io.BytesIO(image_bytes))
    
    # Create clean image buffer without EXIF metadata
    clean_image = Image.new(image.mode, image.size)
    clean_image.paste(image)

    output = io.BytesIO()
    # Save without EXIF
    img_format = image.format if image.format in ["JPEG", "PNG", "WEBP"] else "JPEG"
    clean_image.save(output, format=img_format)
    return output.getvalue()
