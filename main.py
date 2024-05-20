from pytube import YouTube
from colorama import Fore, Style
from moviepy.editor import AudioFileClip, VideoFileClip
import os

def banner():
    print(Fore.GREEN + """

██╗░░░██╗████████╗░░░░░░██╗░░░██╗███╗░░██╗██████╗░██╗░░░██╗██╗░░██╗
╚██╗░██╔╝╚══██╔══╝░░░░░░██║░░░██║████╗░██║██╔══██╗██║░░░██║██║░░██║
░╚████╔╝░░░░██║░░░█████╗██║░░░██║██╔██╗██║██║░░██║██║░░░██║███████║
░░╚██╔╝░░░░░██║░░░╚════╝██║░░░██║██║╚████║██║░░██║██║░░░██║██╔══██║
░░░██║░░░░░░██║░░░░░░░░░╚██████╔╝██║░╚███║██████╔╝╚██████╔╝██║░░██║
░░░╚═╝░░░░░░╚═╝░░░░░░░░░░╚═════╝░╚═╝░░╚══╝╚═════╝░░╚═════╝░╚═╝░░╚═╝
""")

banner()

def on_progress(stream, chunk, remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - remaining
    percentage_of_completion = (bytes_downloaded / total_size) * 100
    print(f"Downloaded {percentage_of_completion:.2f}%", end='\r', flush=True)

def unduh_file(url, jenis_file, kualitas='tinggi'):
    yt_obj = YouTube(url, on_progress_callback=on_progress)
    if jenis_file in ("a", "A", "audio", "Audio"):
        print("bentar ya Audio sedang diunduh...")
        audio_file = yt_obj.streams.filter(only_audio=True).first()
        file_path = audio_file.download()
        convert_audio_to_mp3(file_path)
    elif jenis_file in ("v", "V", "video", "Video"):
        print("bentar ya Video sedang diunduh...")
        if kualitas == 'tinggi':
            video_file = yt_obj.streams.filter(only_video=False).get_highest_resolution()
        else:
            video_file = yt_obj.streams.filter(only_video=False, resolution=kualitas).first()
        if video_file:
            file_path = video_file.download()
            convert_video_to_mp3(file_path)
        else:
            print("Tidak ada stream video dengan kualitas yang diminta.")
    else:
        print("Harap masukkan 'audio' atau 'video'.")

def convert_audio_to_mp3(file_path):
    mp3_file_path = os.path.splitext(file_path)[0] + ".mp3"
    audio = AudioFileClip(file_path)
    audio.write_audiofile(mp3_file_path)
    audio.close()
    os.remove(file_path)
    print(f"Audio telah dikonversi ke format MP3 dan disimpan di: {mp3_file_path}")

def convert_video_to_mp3(file_path):
    mp3_file_path = os.path.splitext(file_path)[0] + ".mp3"
    video = VideoFileClip(file_path)
    audio = video.audio
    audio.write_audiofile(mp3_file_path)
    video.close()
    audio.close()
    os.remove(file_path)
    print(f"Video telah dikonversi ke format MP3 dan disimpan di: {mp3_file_path}")

def main():
    url = input("Masukkan URL YouTube: ").strip()
    while not url:
        url = input("URL tidak boleh kosong. Masukkan URL YouTube: ").strip()

    jenis_file = input("kamu mau apa, audio atau video? Masukkan 'a' atau 'v': ").strip().lower()
    while jenis_file not in ('a', 'audio', 'v', 'video'):
        jenis_file = input("Input tidak valid. Apa yang Anda inginkan, audio atau video? Masukkan 'a' atau 'v': ").strip().lower()

    if jenis_file == 'v':
        kualitas = input("Pilih kualitas video (mis. 720p, 480p, 360p, dsb.), atau masukkan 'tinggi' untuk kualitas tertinggi: ").strip().lower()
        unduh_file(url, jenis_file, kualitas)
    else:
        unduh_file(url, jenis_file)

if __name__ == "__main__":
    main()
