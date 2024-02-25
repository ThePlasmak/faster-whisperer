import pyperclip

# Input text
input_text = """So right after 11pm, I brought him to sleep, about 12pm, I think I heard some sound, so I realised, eh, what got smell?

10
00:02:10,940 --> 00:02:11,660
Fiona: Then I woke up,

11
00:02:11,660 --> 00:02:13,280
Fiona: oh he actually had a diarrhoea,

12
00:02:13,280 --> 00:02:13,520
Fiona: a very

13
00:02:13,520 --> 00:02:14,520
Fiona: bad diarrhoea,

14
00:02:14,520 --> 00:02:16,860
Fiona: so I wanted to clean him up and

15
00:02:16,860 --> 00:02:17,960
Fiona: I realised that his

16
00:02:17,960 --> 00:02:18,440
Fiona: whole

17
00:02:18,440 --> 00:02:40,500
Fiona: body was very jelly and I actually screamed for my parents. and when I went to scream for my parents, he actually made a very loud sound, he made a girl's voice screaming like, ah, very loud. So I went over to him and he actually slowly gaps in for air and so he passed on when everyone is at home.

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
