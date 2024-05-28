import os

from youtube_transcript_api import YouTubeTranscriptApi
import re


def sub2text(link):
    assert link.strip(), "Link cannot be empty."

    # example link: 'https://www.youtube.com/watch?v=N-hA0OjAEMA'
    fragment = re.search(r'v=([^\&]+)', link).group(1)
    # assigning srt variable with the list
    # of dictionaries obtained by the get_transcript() function
    try:
        srt = YouTubeTranscriptApi.get_transcript(fragment, languages=[
            'en'])  # dictionary {text: [str], start: [sec], duration: [sec]}
        assert len(
            srt) > 0, "No transcript found for the specified language code. Please provide a file with English subtitles."
        transcript_text = ""
        for item in srt:
            transcript_text += item['text'] + '\n'
        filename = os.path.join(os.getcwd(), 'transcript.txt')
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(transcript_text)
        return filename
    except Exception as e:
        print(
            "Could not retrieve a transcript for the video {}! This is most likely caused by no english subtitles to the video or no subtitles at all.".format(
                link))
