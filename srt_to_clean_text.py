import pyperclip

# Input text
input_text = """
"""


def convert_subtitles_to_text(subtitles):
    # Split the input text into lines
    lines = subtitles.split("\n")

    # Initialize an empty list to hold the processed lines
    dialogue_lines = []

    # Loop through each line in the input text
    for line in lines:
        # If the line is empty, a subtitle number, or contains a timestamp, skip it
        if not line or line.isdigit() or "-->" in line:
            continue
        else:
            # Remove the speaker name and append the line to the dialogue_lines list
            dialogue_line = line.split(": ", 1)[-1]
            dialogue_lines.append(dialogue_line)

    # Join the processed lines into a single block of text
    output_text = " ".join(dialogue_lines)
    return output_text


# Convert the subtitles to text
output_text = convert_subtitles_to_text(input_text)

# Print the converted text
print(output_text)
pyperclip.copy(output_text)
