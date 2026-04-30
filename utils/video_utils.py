import math
import struct
import uuid
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
VIDEO_DIR = DATA_DIR / "videos"
THUMB_DIR = DATA_DIR / "thumbnails"


def save_uploaded_video(uploaded_file) -> Path:
    VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    ext = Path(uploaded_file.name).suffix or ".mp4"
    dest = VIDEO_DIR / f"{uuid.uuid4()}{ext}"
    dest.write_bytes(uploaded_file.read())
    return dest


def _get_video_rotation(video_path: Path) -> int:
    """動画の回転角度（度）を返す。回転なしの場合は 0。"""
    # まず PyAV のストリームメタデータを確認（Android 系動画で有効）
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

    # tkhd 変換行列をパースして回転を取得（iPhone MOV/MP4 で有効）
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
                    # v0: matrix @ offset 40、v1: matrix @ offset 52
                    matrix_start = 52 if version == 1 else 40
                    if len(tkhd) < matrix_start + 44:
                        continue
                    m = struct.unpack(">9i", tkhd[matrix_start:matrix_start + 36])
                    a, b = m[0], m[1]
                    # トラック幅が 0 なら音声トラックなのでスキップ
                    w = struct.unpack(">I", tkhd[matrix_start + 36:matrix_start + 40])[0] >> 16
                    if w == 0 or (a == 0 and b == 0):
                        continue
                    angle = math.degrees(math.atan2(b, a))
                    return round(angle / 90) * 90
    except Exception:
        pass

    return 0


def extract_thumbnail(video_path: Path) -> Path:
    THUMB_DIR.mkdir(parents=True, exist_ok=True)
    thumb_path = THUMB_DIR / f"{video_path.stem}.jpg"
    try:
        import av
        rotation = _get_video_rotation(video_path)
        container = av.open(str(video_path))
        for frame in container.decode(video=0):
            img = frame.to_image()
            if rotation:
                # PIL の rotate は反時計回りなので符号を反転して時計回りに補正
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
    # フォールバック: Pillow でグレー画像を生成
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (320, 180), color=(50, 50, 50))
    draw = ImageDraw.Draw(img)
    draw.text((120, 80), "▶ Video", fill=(200, 200, 200))
    img.save(thumb_path)
    return thumb_path
