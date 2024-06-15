from pytube import YouTube
from colorama import Fore
import os

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    print(Fore.GREEN +f"[ * ] ==>>>> Proses unduh: {percentage:.2f}% bentar", end="\r")

def download_youtube_video():
    
    print("""
    
██╗░░░██╗████████╗  ░███████╗
╚██╗░██╔╝╚══██╔══╝  ██╔██╔══╝
░╚████╔╝░░░░██║░░░  ╚██████╗░
░░╚██╔╝░░░░░██║░░░  ░╚═██╔██╗
░░░██║░░░░░░██║░░░  ███████╔╝
░░░╚═╝░░░░░░╚═╝░░░  ╚══════╝░

██╗░░██╗░█████╗░░█████╗░██╗░░██╗
██║░░██║██╔══██╗██╔══██╗██║░██╔╝
███████║███████║██║░░╚═╝█████═╝░
██╔══██║██╔══██║██║░░██╗██╔═██╗░
██║░░██║██║░░██║╚█████╔╝██║░╚██╗
╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
    """)

    video_url = input(Fore.LIGHTBLACK_EX +"(linux㉿root)\n|=# Masukkan link: ")

    try:
        yt = YouTube(video_url, on_progress_callback=on_progress)
        while True:
            format_choice = input(Fore.LIGHTBLACK_EX +"---------------------------------\n==>>>> Pilih format unduhan (video/audio)\n ketik [v] => untuk video\n ketik [a] => untuk audio\n ketik [k] => untuk mengubah link\n---------------------------------\nlinux㉿root)\n|=# ketikkan: ").strip().lower()
            if format_choice == 'v':
                while True:
                    streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
                    print("---------------------------------\nPilihan resolusi yang tersedia:")
                    for i, stream in enumerate(streams):
                        print(f"{i + 1}. {stream.resolution} - {stream.mime_type}")
                    
                    try:
                        choice = input(Fore.LIGHTBLACK_EX +"==>>>> Pilih resolusi (masukkan nomor tersedia)atau ketik 'k' untuk memilih format lagi\n---------------------------------\nlinux㉿root)\n|=# ketikkan: ").strip().lower()
                        if choice == 'k':
                            break
                        choice = int(choice) - 1
                        if 0 <= choice < len(streams):
                            stream = streams[choice]
                            output_path = './downloaded_videos'
                            if not os.path.exists(output_path):
                                os.makedirs(output_path)
                            stream.download(output_path)
                            print(Fore.GREEN + f"\n==>>>> Video '{yt.title}' dengan resolusi {stream.resolution} telah berhasil diunduh ke '{output_path}'")
                            return
                        else:
                            print(Fore.RED +"[ ! ] ==>>>> Pilihan tidak ada bro. coba ketik nomor yang tersedia.")
                    except ValueError:
                        print(Fore.RED +"[ ! ] ==>>>> Input tidak ada. coba ketik nomor yang sesuai? bukan huruf.")
            elif format_choice == 'a':
                while True:
                    stream = yt.streams.filter(only_audio=True).first()
                    if stream:
                        output_path = './downloaded_audios'
                        if not os.path.exists(output_path):
                            os.makedirs(output_path)
                        out_file = stream.download(output_path)
                        base, ext = os.path.splitext(out_file)
                        new_file = base + '.mp3'
                        os.rename(out_file, new_file)
                        print(Fore.GREEN + f"\n==>>>> Audio '{yt.title}' telah berhasil diunduh dan disimpan sebagai MP3 di '{new_file}'")
                        return
                    else:
                        print(Fore.RED +"[ ! ] ==>>>> Tidak ada stream audio yang tersedia. Coba lagi.")
                    break
            elif format_choice == 'k':
                video_url = input(Fore.LIGHTBLACK_EX +"linux㉿root)\n|=# Masukkan link baru: ")
                yt = YouTube(video_url, on_progress_callback=on_progress)
            else:
                print(Fore.RED +"[ ! ] ==>>>> Format pilihan tidak ada. Pilih 'v' atau 'a' atau ketik 'k' untuk mengubah link.")
    except Exception as e:
        print(Fore.RED + f"[ ! ] ==>>>> Terjadi kesalahan: {e}")

download_youtube_video()
