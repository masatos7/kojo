import math
import struct
import tempfile
import uuid
from pathlib import Path

TEMP_DIR = Path(tempfile.gettempdir()) / "kojo"

MIME_TYPES = {
    ".mp4": "video/mp4",
    ".mov": "video/quicktime",
    ".avi": "video/x-msvideo",
    ".webm": "video/webm",
    ".mkv": "video/x-matroska",
}


def _sb():
    import streamlit as st
    from supabase import create_client
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_SERVICE_KEY"])


def save_uploaded_video(uploaded_file) -> Path:
    """アップロードファイルをテンポラリに保存して Path を返す。"""
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    ext = Path(uploaded_file.name).suffix or ".mp4"
    dest = TEMP_DIR / f"{uuid.uuid4()}{ext}"
    dest.write_bytes(uploaded_file.read())
    return dest


def upload_to_storage(local_path: Path, bucket: str) -> str:
    """ファイルを Supabase Storage にアップロードして公開 URL を返す。"""
    content_type = MIME_TYPES.get(local_path.suffix.lower(), "application/octet-stream")
    filename = local_path.name
    _sb().storage.from_(bucket).upload(
        filename,
        local_path.read_bytes(),
        {"content-type": content_type, "x-upsert": "true"},
    )
    return _sb().storage.from_(bucket).get_public_url(filename)


def delete_from_storage(url: str, bucket: str):
    """Supabase Storage からファイルを削除する。"""
    if not url or not url.startswith("http"):
        return
    try:
        filename = url.split("/")[-1].split("?")[0]
        _sb().storage.from_(bucket).remove([filename])
    except Exception:
        pass


def _get_video_rotation(video_path: Path) -> int:
    """動画の回転角度（度）を返す。"""
    try:
        import av
        container = av.open(str(video_path))
        stream = container.streams.video[0]
        rotate = stream.metadata.get("rotate") or container.metadata.get("rotate")
        container.close()
        if rotate:
            return int(rotate)
    except Exception:
        pass

    try:
        data = video_path.read_bytes()

        def iter_atoms(buf, start, end):
            pos = start
            while pos < end - 8:
                size = struct.unpack(">I", buf[pos:pos + 4])[0]
                if size < 8 or pos + size > end:
                    break
                yield buf[pos + 4:pos + 8], pos, size
                pos += size

        for name, mpos, msize in iter_atoms(data, 0, len(data)):
            if name != b"moov":
                continue
            for tname, tpos, tsize in iter_atoms(data, mpos + 8, mpos + msize):
                if tname != b"trak":
                    continue
                for kname, kpos, ksize in iter_atoms(data, tpos + 8, tpos + tsize):
                    if kname != b"tkhd":
                        continue
                    tkhd = data[kpos + 8:kpos + ksize]
                    if len(tkhd) < 84:
                        continue
                    version = tkhd[0]
                    matrix_start = 52 if version == 1 else 40
                    if len(tkhd) < matrix_start + 44:
                        continue
                    m = struct.unpack(">9i", tkhd[matrix_start:matrix_start + 36])
                    a, b = m[0], m[1]
                    w = struct.unpack(">I", tkhd[matrix_start + 36:matrix_start + 40])[0] >> 16
                    if w == 0 or (a == 0 and b == 0):
                        continue
                    angle = math.degrees(math.atan2(b, a))
                    return round(angle / 90) * 90
    except Exception:
        pass

    return 0


def extract_thumbnail(video_path: Path) -> Path:
    """動画の最初のフレームをサムネールとして保存し、ローカル Path を返す。"""
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    thumb_path = TEMP_DIR / f"{video_path.stem}.jpg"
    try:
        import av
        rotation = _get_video_rotation(video_path)
        container = av.open(str(video_path))
        for frame in container.decode(video=0):
            img = frame.to_image()
            if rotation:
                img = img.rotate(-rotation, expand=True)
            img.save(str(thumb_path), "JPEG", quality=85)
            break
        container.close()
        return thumb_path
    except Exception:
        pass
    try:
        import cv2
        cap = cv2.VideoCapture(str(video_path))
        ok, frame = cap.read()
        cap.release()
        if ok:
            cv2.imwrite(str(thumb_path), frame)
            return thumb_path
    except Exception:
        pass
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (320, 180), color=(50, 50, 50))
    draw = ImageDraw.Draw(img)
    draw.text((120, 80), "▶ Video", fill=(200, 200, 200))
    img.save(thumb_path)
    return thumb_path
