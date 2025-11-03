import os
from pathlib import Path


def iter_video_files(root: Path) -> list[Path]:
    video_extensions = {
        ".mp4",
        ".mov",
        ".mkv",
        ".avi",
        ".wmv",
        ".flv",
        ".webm",
        ".m4v",
        ".mpg",
        ".mpeg",
    }
    return [
        p
        for p in root.iterdir()
        if p.is_file() and p.suffix.lower() in video_extensions and not p.name.endswith(".binary.txt")
    ]


def convert_file_to_binary_text(input_path: Path, output_path: Path, chunk_size: int = 1024 * 1024) -> None:
    # Precompute lookup table for fast byte->bitstring conversion
    lookup = [format(i, "08b") for i in range(256)]

    with input_path.open("rb") as f_in, output_path.open("w", encoding="utf-8") as f_out:
        while True:
            chunk = f_in.read(chunk_size)
            if not chunk:
                break
            # Convert each byte in chunk to its 8-bit binary representation
            bits_str = "".join(lookup[b] for b in chunk)
            f_out.write(bits_str)


def main() -> None:
    root = Path(os.getcwd())
    video_files = iter_video_files(root)

    if not video_files:
        print("No video files found to convert.")
        return

    for video_path in video_files:
        output_path = video_path.with_name(f"{video_path.name}.binary.txt")
        print(f"Converting {video_path.name} -> {output_path.name} ...")
        convert_file_to_binary_text(video_path, output_path)
        print(f"Done: {output_path.name}")


if __name__ == "__main__":
    main()


