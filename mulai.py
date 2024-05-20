from pytube import YouTube

from colorama import Fore, Style

def banner():
    print(Fore.GREEN + """

░█──░█ ▀▀█▀▀ ── █──█ █▀▀▄ █▀▀▄ █──█ █──█ 
░█▄▄▄█ ─░█── ▀▀ █──█ █──█ █──█ █──█ █▀▀█ 
──░█── ─░█── ── ─▀▀▀ ▀──▀ ▀▀▀─ ─▀▀▀ ▀──▀
""")

banner()

def on_progress(stream, chunk, remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - remaining
    percentage_of_completion = (bytes_downloaded / total_size) * 100
    print(f"Downloaded {percentage_of_completion:.2f}%", end='\r', flush=True)

def unduh_file(url, jenis_file, kualitas='highest'):
    yt_obj = YouTube(url, on_progress_callback=on_progress)
    if jenis_file in ("a", "A", "audio", "Audio"):
        print("Audio sedang diunduh...")
        audio_file = yt_obj.streams.filter(only_audio=True).first()
        audio_file.download()
    elif jenis_file in ("v", "V", "video", "Video"):
        print("Video sedang diunduh...")
        if kualitas == 'highest':
            video_file = yt_obj.streams.filter(only_video=False).get_highest_resolution()
        else:
            video_file = yt_obj.streams.filter(only_video=False, resolution=kualitas).first()
        if video_file:
            video_file.download()
        else:
            print("Tidak ada stream video dengan kualitas yang diminta.")
    else:
        print("Harap masukkan 'audio' atau 'video'.")

def main():
    url = input("Masukkan URL YouTube: ").strip()
    while not url:
        url = input("URL tidak boleh kosong. Masukkan URL YouTube: ").strip()

    format_default = "audio"
    jenis_file = input("Apa yang Anda inginkan, audio atau video? Masukkan 'a' atau 'v': ").strip().lower()
    while jenis_file not in ('a', 'audio', 'v', 'video'):
        jenis_file = input("Input tidak valid. Apa yang Anda inginkan, audio atau video? Masukkan 'a' atau 'v': ").strip().lower()

    if jenis_file == 'v':
        kualitas = input("Pilih kualitas video (mis. 720p, 480p, 360p, dsb.), atau masukkan 'highest' untuk kualitas tertinggi: ").strip().lower()
        unduh_file(url, jenis_file, kualitas)
    else:
        unduh_file(url, jenis_file)

if __name__ == "__main__":
    main()
