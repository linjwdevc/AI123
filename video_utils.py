"""
视频合并工具 - 使用FFmpeg合并多个视频
"""

import os
import subprocess
import tempfile
from pathlib import Path


def merge_videos(video_paths: list, output_path: str) -> str:
    """
    使用FFmpeg合并多个视频

    Args:
        video_paths: 视频文件路径列表（按顺序）
        output_path: 输出文件路径

    Returns:
        合并后的视频路径，失败返回None
    """
    if not video_paths:
        print("没有视频需要合并")
        return None

    if len(video_paths) == 1:
        print("只有一个视频，直接复制")
        import shutil

        shutil.copy2(video_paths[0], output_path)
        return output_path

    valid_videos = [v for v in video_paths if os.path.exists(v)]
    if len(valid_videos) != len(video_paths):
        missing = set(video_paths) - set(valid_videos)
        print(f"警告: 以下视频文件不存在: {missing}")

    if not valid_videos:
        print("没有有效的视频文件")
        return None

    if len(valid_videos) == 1:
        import shutil

        shutil.copy2(valid_videos[0], output_path)
        return output_path

    print(f"开始合并 {len(valid_videos)} 个视频...")

    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        for video_path in valid_videos:
            f.write(f"file '{video_path}'\n")
        list_file = f.name

    try:
        cmd = [
            "ffmpeg",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            list_file,
            "-c",
            "copy",
            "-y",
            output_path,
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"FFmpeg错误: {result.stderr}")
            return None

        print(f"视频合并成功: {output_path}")
        return output_path

    except FileNotFoundError:
        print("错误: 未找到FFmpeg，请确保已安装并添加到PATH")
        return None
    except Exception as e:
        print(f"合并视频失败: {e}")
        return None
    finally:
        try:
            os.unlink(list_file)
        except:
            pass


def get_video_duration(video_path: str) -> float:
    """获取视频时长（秒）"""
    try:
        cmd = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            video_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return float(result.stdout.strip())
    except:
        pass
    return 0


def check_ffmpeg() -> bool:
    """检查FFmpeg是否可用"""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except:
        return False
