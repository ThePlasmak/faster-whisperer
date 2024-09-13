from faster_whisper import WhisperModel, BatchedInferencePipeline
import time
import os

start_time = time.perf_counter()

# For the SRT, use Subtitle Edit to fix common issues automatically (Ctrl+Shift+F)

# Add desired files to process in ".txt"
with open(".txt", "r", encoding="utf-8") as f:
    input_path_ext = f.read().strip()  # Ensure the file path is read correctly

language = "en"
model_size = "distil-large-v3"  # Select from this list: 'tiny.en', 'tiny', 'base.en', 'base', 'small.en', 'small', 'medium.en', 'medium', 'large-v1', 'large-v2', 'large-v3', 'large'

# Run on GPU with FP16
model = WhisperModel(model_size, device="cuda", compute_type="float16")
# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8
# model = WhisperModel(model_size, device="cpu", compute_type="int8")

# Batched (is faster than default)
batched_model = BatchedInferencePipeline(model=model)

def transcribe(input_path_ext):
    input_path, ext = os.path.splitext(input_path_ext)

    # Default
    # segments, info = model.transcribe(
    #     f"{input_path_ext}", beam_size=5, language=language
    # )
    
    # Batched
    segments, info = batched_model.transcribe(f"{input_path_ext}", batch_size=16)

    # Print language detection result
    # print(
    #     "Detected language '%s' with probability %f"
    #     % (info.language, info.language_probability)
    # )

    with open(f"{input_path}_no_timestamp.txt", "w", encoding="utf-8") as fnt:
        with open(f"{input_path}.srt", "w", encoding="utf-8") as fsrt:
            with open(f"{input_path}.txt", "w", encoding="utf-8") as f:
                seq_number = 1  # Initialize seq_number here
                for segment in segments:
                    # Write TXT (no timestamp)
                    fnt.write(f"{segment.text}")

                    # Write TXT
                    segment_start = time.strftime(
                        "%H:%M:%S", time.gmtime(segment.start)
                    )
                    segment_end = time.strftime("%H:%M:%S", time.gmtime(segment.end))

                    line = f"[{segment_start} -> {segment_end}] {segment.text}"

                    f.write(line + "\n")

                    # Write SRT
                    segment_start = "{:02d}:{:02d}:{:02d},{:03d}".format(
                        int(segment.start // 3600),
                        int((segment.start % 3600) // 60),
                        int(segment.start % 60),
                        int((segment.start * 1000) % 1000),
                    )
                    segment_end = "{:02d}:{:02d}:{:02d},{:03d}".format(
                        int(segment.end // 3600),
                        int((segment.end % 3600) // 60),
                        int(segment.end % 60),
                        int((segment.end * 1000) % 1000),
                    )

                    fsrt.write(f"{seq_number}\n")
                    fsrt.write(f"{segment_start} --> {segment_end}\n")
                    fsrt.write(f"{segment.text.strip()}\n\n")

                    print(
                        f"{segment_start} --> {segment_end}\n{segment.text.strip()}\n"
                    )

                    seq_number += 1
    # Strip no_timestamp TXT
    with open(f"{input_path}_no_timestamp.txt", "r+", encoding="utf-8") as fnt:
        file_contents = fnt.read()
        stripped_text = file_contents.strip()
        fnt.seek(0)
        fnt.write(stripped_text)
        fnt.truncate()


audio_extensions = [".mp3", ".wav", ".ogg", ".flac", ".m4a", ".aac", ".wma"]

if os.path.isdir(input_path_ext):
    # List all files in the directory
    all_files = os.listdir(input_path_ext)
    # Filter out files with audio extensions
    audio_files = [
        os.path.join(input_path_ext, file)
        for file in all_files
        if os.path.splitext(file)[1].lower() in audio_extensions
    ]
else:
    audio_files = [input_path_ext]  # Treat the single file path correctly

for ipe in audio_files:
    transcribe(ipe)

time_taken_seconds = time.perf_counter() - start_time

hours = int(time_taken_seconds // 3600)
minutes = int((time_taken_seconds % 3600) // 60)
seconds = time_taken_seconds % 60

print(
    "Time taken: {} hours, {} minutes, {:.3f} seconds".format(hours, minutes, seconds)
)
