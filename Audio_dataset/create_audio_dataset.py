from pydub import AudioSegment
from pydub.utils import make_chunks
from tqdm import tqdm

import os

BASEDIR = "FullAudio/"
CHUNK_SIZE = 1000  # chunk size in ms
SAMPLE_RATE = 16000


def make_chunks_of_audio(path_to_wav: str):
    audio = AudioSegment.from_file(file=path_to_wav, format='wav')
    audio.set_frame_rate(SAMPLE_RATE)
    audio_chunks = make_chunks(audio, chunk_length=CHUNK_SIZE)
    basefilename = (os.path.split(path_to_wav)[-1]). split('.')[0]

    if not os.path.exists(basefilename.upper()):
        # print(f"Creating {basefilename.upper()} folder")
        os.mkdir(basefilename.upper())

    for i, chunk in enumerate(audio_chunks):
        new_chunkname = f"{basefilename}_{i}.wav"
        # print(f"Exporting {basefilename.upper()}/{new_chunkname}")
        chunk.export(f"{basefilename.upper()}/{new_chunkname}", format='wav')

if __name__ == "__main__":
    all_audio_files = os.listdir(BASEDIR)
    for audio_file in tqdm(all_audio_files, desc='Creating Dataset...', colour='green', smoothing=0.6):
        if (".wav" in audio_file):
            make_chunks_of_audio(f"{BASEDIR}{audio_file}")