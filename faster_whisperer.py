from faster_whisper import WhisperModel
import time
import os

# For the SRT, use Subtitle Edit to fix common issues automatically (Ctrl+Shift+F)

start_time = time.time()

input_path_ext = [""] # Paths to audio file

language = "en"
model_size = "large-v2"  # Select from this list: 'tiny.en', 'tiny', 'base.en', 'base', 'small.en', 'small', 'medium.en', 'medium', 'large-v1', 'large-v2', 'large'

# Run on GPU with FP16
model = WhisperModel(model_size, device="cuda", compute_type="float16")
# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8
# model = WhisperModel(model_size, device="cpu", compute_type="int8")

def transcribe(input_path_ext):
    input_path, ext = os.path.splitext(input_path_ext)

    segments, info = model.transcribe(
        f"{input_path_ext}", beam_size=5, language=language
    )

    # Print language detection result
    # print(
    #     "Detected language '%s' with probability %f"
    #     % (info.language, info.language_probability)
    # )

    with open(
        f"{input_path}_no_timestamp.txt", "w", encoding='utf-8'
    ) as fnt:
        with open(
            f"{input_path}.srt", "w", encoding="utf-8"
        ) as fsrt:
            with open(f"{input_path}.txt", "w", encoding='utf-8') as f:
                for segment in segments:
                    # Write TXT (no timestamp)
                    fnt.write(f"{segment.text}")

                    # Write TXT
                    segment_start = time.strftime("%H:%M:%S", time.gmtime(segment.start))
                    segment_end = time.strftime("%H:%M:%S", time.gmtime(segment.end))

                    line = f"[{segment_start} -> {segment_end}] {segment.text}"

                    f.write(line + "\n")

                    # Write SRT
                    seq_number = 1
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

                    print(f"{segment_start} --> {segment_end}\n{segment.text.strip()}\n")

                    seq_number += 1
    # Strip no_timestamp TXT
    with open(
        f"{input_path}_no_timestamp.txt", "r+", encoding='utf-8'
    ) as fnt:
        file_contents = fnt.read()
        stripped_text = file_contents.strip()
        fnt.seek(0)
        fnt.write(stripped_text)
        fnt.truncate()

for ipe in input_path_ext:
    transcribe(ipe)

# Calculate the time taken in seconds
time_taken_seconds = time.time() - start_time

# Format the time taken to three decimal places
time_taken_formatted = "{:.3f}".format(time_taken_seconds)

# Calculate hours, minutes, and seconds
hours = int(time_taken_seconds // 3600)
minutes = int((time_taken_seconds % 3600) // 60)
seconds = int(time_taken_seconds % 60)

# Print the time taken in hours, minutes, and seconds format with three decimal places
print(
    "Time taken: {} hours, {} minutes, {} seconds".format(
        hours, minutes, time_taken_formatted
    )
)