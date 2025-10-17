#!/usr/bin/env python3
"""
Video Clipper Script
Extract specific time intervals from video files
"""

import os
import sys
import argparse
from moviepy.editor import VideoFileClip
from datetime import timedelta


def parse_time(time_str):
    """
    Parse time string in various formats to seconds

    Supported formats:
    - MM:SS (e.g., "05:30")
    - HH:MM:SS (e.g., "01:05:30")
    - Seconds as string (e.g., "330")
    - Seconds as number (e.g., 330)

    Args:
        time_str: Time string to parse

    Returns:
        float: Time in seconds
    """
    if isinstance(time_str, (int, float)):
        return float(time_str)

    time_str = str(time_str).strip()

    # Check if it's just a number (seconds)
    try:
        return float(time_str)
    except ValueError:
        pass

    # Parse HH:MM:SS or MM:SS format
    if ":" in time_str:
        parts = time_str.split(":")
        if len(parts) == 2:  # MM:SS
            minutes, seconds = map(int, parts)
            return minutes * 60 + seconds
        elif len(parts) == 3:  # HH:MM:SS
            hours, minutes, seconds = map(int, parts)
            return hours * 3600 + minutes * 60 + seconds
        else:
            raise ValueError(f"Invalid time format: {time_str}")

    raise ValueError(f"Could not parse time: {time_str}")


def format_time(seconds):
    """
    Format seconds to HH:MM:SS string

    Args:
        seconds: Time in seconds

    Returns:
        str: Formatted time string
    """
    td = timedelta(seconds=seconds)
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def clip_video(input_path, start_time, end_time, output_path=None):
    """
    Extract a clip from a video file

    Args:
        input_path: Path to input video file
        start_time: Start time (string or seconds)
        end_time: End time (string or seconds)
        output_path: Path for output file (optional)

    Returns:
        str: Path to the created clip
    """
    # Parse times
    start_seconds = parse_time(start_time)
    end_seconds = parse_time(end_time)

    # Validate times
    if start_seconds >= end_seconds:
        raise ValueError("Start time must be before end time")

    # Generate output path if not provided
    if output_path is None:
        base_name = os.path.splitext(input_path)[0]
        start_str = format_time(start_seconds).replace(":", "-")
        end_str = format_time(end_seconds).replace(":", "-")
        output_path = f"{base_name}_clip_{start_str}_to_{end_str}.mp4"

    print(f"Loading video: {input_path}")

    # Load video
    video = VideoFileClip(input_path)

    # Validate times against video duration
    if start_seconds >= video.duration:
        raise ValueError(
            f"Start time ({format_time(start_seconds)}) is beyond video duration ({format_time(video.duration)})"
        )

    if end_seconds > video.duration:
        print(
            f"Warning: End time ({format_time(end_seconds)}) is beyond video duration ({format_time(video.duration)})"
        )
        print(f"Clipping to end of video instead")
        end_seconds = video.duration

    duration = end_seconds - start_seconds

    print(f"Extracting clip:")
    print(f"  Start: {format_time(start_seconds)}")
    print(f"  End: {format_time(end_seconds)}")
    print(f"  Duration: {format_time(duration)}")

    # Extract clip
    clip = video.subclip(start_seconds, end_seconds)

    print(f"Writing clip to: {output_path}")

    # Write the clip
    clip.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        temp_audiofile="temp-audio.m4a",
        remove_temp=True,
        fps=video.fps,
        verbose=False,
        logger=None,
    )

    # Clean up
    clip.close()
    video.close()

    print(f"Clip created successfully: {output_path}")
    return output_path


def clip_multiple_intervals(input_path, intervals, output_dir=None):
    """
    Extract multiple clips from a video file

    Args:
        input_path: Path to input video file
        intervals: List of (start, end) tuples or (start, end, name) tuples
        output_dir: Directory for output files (optional)

    Returns:
        list: Paths to created clips
    """
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_paths = []

    for i, interval in enumerate(intervals):
        if len(interval) == 2:
            start, end = interval
            name = None
        elif len(interval) == 3:
            start, end, name = interval
        else:
            raise ValueError("Interval must be (start, end) or (start, end, name)")

        # Generate output path
        if name:
            if output_dir:
                output_path = os.path.join(output_dir, f"{name}.mp4")
            else:
                base_dir = os.path.dirname(input_path)
                output_path = os.path.join(base_dir, f"{name}.mp4")
        else:
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            start_str = format_time(parse_time(start)).replace(":", "-")
            end_str = format_time(parse_time(end)).replace(":", "-")
            filename = f"{base_name}_clip_{i+1}_{start_str}_to_{end_str}.mp4"

            if output_dir:
                output_path = os.path.join(output_dir, filename)
            else:
                base_dir = os.path.dirname(input_path)
                output_path = os.path.join(base_dir, filename)

        print(f"\n--- Clip {i+1}/{len(intervals)} ---")
        clip_path = clip_video(input_path, start, end, output_path)
        output_paths.append(clip_path)

    return output_paths


def main():
    parser = argparse.ArgumentParser(description="Extract clips from video files")
    parser.add_argument("input", help="Input video file path")
    parser.add_argument("start", help="Start time (MM:SS, HH:MM:SS, or seconds)")
    parser.add_argument("end", help="End time (MM:SS, HH:MM:SS, or seconds)")
    parser.add_argument("-o", "--output", help="Output file path (optional)")
    parser.add_argument("--info", action="store_true", help="Show video information")

    args = parser.parse_args()

    # Check if input file exists
    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)

    # Show video info if requested
    if args.info:
        video = VideoFileClip(args.input)
        print(f"Video Information:")
        print(f"  Duration: {format_time(video.duration)}")
        print(f"  FPS: {video.fps}")
        print(f"  Size: {video.size}")
        video.close()
        if not args.start or not args.end:
            return

    try:
        clip_video(args.input, args.start, args.end, args.output)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


# Example usage functions
def soccer_highlights_example():
    """Example: Extract goal clips from a soccer match"""

    video_path = "/Users/orhanbalci/Downloads/afka_afyon_hd.mp4"

    # Define goal moments with some context (30 seconds before and after)
    goal_intervals = [
        ("07:50", "08:50", "goal_1_afka"),  # Goal at 08:20
        ("32:52", "33:52", "goal_2_afyon"),  # Goal at 33:22
        ("38:38", "39:38", "goal_3_afka"),  # Goal at 39:08
        ("51:34", "52:34", "goal_4_afka"),  # Goal at 52:04
    ]

    output_dir = "/Users/orhanbalci/Downloads/soccer_clips"

    try:
        clips = clip_multiple_intervals(video_path, goal_intervals, output_dir)
        print(f"\nCreated {len(clips)} goal clips:")
        for clip in clips:
            print(f"  - {clip}")
    except Exception as e:
        print(f"Error creating clips: {e}")


def test_clips_example():
    """Example: Create short test clips for development"""

    video_path = "/Users/orhanbalci/Downloads/afka_afyon_hd.mp4"

    # Create short test clips
    test_intervals = [
        ("00:00", "00:30", "test_start"),  # First 30 seconds
        ("08:00", "08:40", "test_goal_sequence"),  # Goal sequence
        ("45:00", "45:30", "test_halftime"),  # Halftime
    ]

    output_dir = "/Users/orhanbalci/Downloads/test_clips"

    try:
        clips = clip_multiple_intervals(video_path, test_intervals, output_dir)
        print(f"\nCreated {len(clips)} test clips:")
        for clip in clips:
            print(f"  - {clip}")
    except Exception as e:
        print(f"Error creating test clips: {e}")


if __name__ == "__main__":
    # Uncomment one of these to run examples:
    # soccer_highlights_example()
    # test_clips_example()

    # Or run as command line tool
    main()
