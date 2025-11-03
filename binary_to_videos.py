import os
from pathlib import Path


def iter_binary_text_files(root: Path) -> list[Path]:
    return [p for p in root.iterdir() if p.is_file() and p.name.endswith(".binary.txt")]


def write_bits_to_binary_file(bits_path: Path, output_path: Path, chunk_bits: int = 8 * 1024 * 1024) -> None:
    # chunk_bits must be a multiple of 8 so we only split on byte boundaries
    if chunk_bits % 8 != 0:
        raise ValueError("chunk_bits must be a multiple of 8")

    with bits_path.open("r", encoding="utf-8") as f_in, output_path.open("wb") as f_out:
        carry = ""
        while True:
            text = f_in.read(chunk_bits)
            if not text:
                break
            text = carry + text
            remainder = len(text) % 8
            if remainder:
                carry = text[-remainder:]
                text = text[:-remainder]
            else:
                carry = ""

            # Convert every 8 characters (bits) into a byte
            # Using a memoryview-friendly approach for speed
            out_bytes = bytearray(len(text) // 8)
            idx = 0
            for i in range(0, len(text), 8):
                out_bytes[idx] = int(text[i:i+8], 2)
                idx += 1
            f_out.write(out_bytes)

        # Any leftover bits that don't make a full byte are ignored (as in the original logic)


def main() -> None:
    root = Path(os.getcwd())
    binary_text_files = iter_binary_text_files(root)

    if not binary_text_files:
        print("No .binary.txt files found to reconstruct.")
        return

    for bits_path in binary_text_files:
        # Infer original filename by stripping trailing .binary.txt
        base_name = bits_path.name[:-len(".binary.txt")]  # original filename with extension
        output_path = bits_path.with_name(f"reconstructed_{base_name}")
        print(f"Reconstructing {bits_path.name} -> {output_path.name} ...")
        write_bits_to_binary_file(bits_path, output_path)
        print(f"Done: {output_path.name}")


if __name__ == "__main__":
    main()


