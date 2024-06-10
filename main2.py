from pytube import YouTube, Playlist
from colorama import Fore
import os

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    print(f"[ $ ] =======>>>> Proses unduh: {percentage:.2f}% selesai", end="\r")

def download_youtube_video():
    print(Fore.GREEN + """
██╗░░░██╗████████╗░░░░░░██╗░░░██╗███╗░░██╗██████╗░██╗░░░██╗██╗░░██╗
╚██╗░██╔╝╚══██╔══╝░░░░░░██║░░░██║████╗░██║██╔══██╗██║░░░██║██║░░██║
░╚████╔╝░░░░██║░░░█████╗██║░░░██║██╔██╗██║██║░░██║██║░░░██║███████║
░░╚██╔╝░░░░░██║░░░╚════╝██║░░░██║██║╚████║██║░░██║██║░░░██║██╔══██║
░░░██║░░░░░░██║░░░░░░░░░╚██████╔╝██║░╚███║██████╔╝╚██████╔╝██║░░██║
░░░╚═╝░░░░░░╚═╝░░░░░░░░░░╚═════╝░╚═╝░░╚══╝╚═════╝░░╚═════╝░╚═╝░░╚═╝
""")
    while True:
        playlist_url = input("[ $ ] =======>>>> Masukkan URL playlist: ")
        try:
            playlist = Playlist(playlist_url)
            print("Daftar Video dalam Playlist:")
            for i, video_url in enumerate(playlist.video_urls):
                yt = YouTube(video_url)
                print(f"{i+1}. {yt.title}")
            selected_videos_indices = []
            while True:
                video_choice = input("[ $ ] =======>>>> Masukkan nomor video (kosongkan untuk selesai): ").strip()
                if not video_choice:
                    break
                try:
                    choice = int(video_choice) - 1
                    if 0 <= choice < len(playlist.video_urls):
                        selected_videos_indices.append(choice)
                    else:
                        print(f"[ ! ] =======>>>> Nomor video {video_choice} tidak ada.")
                except ValueError:
                    print(f"[ ! ] =======>>>> Input '{video_choice}' tidak ada.")

            while True:
                format_choice = input("[ ! ] =======>>>> Pilih format unduhan (video/audio)\n ketik [v] => untuk video\n ketik [a] untuk audio\n ketik [k]  untuk mengubah URL playlist: ").strip().lower()
                if format_choice == 'k':
                    break
                if format_choice in ['v', 'a']:
                    for index in selected_videos_indices:
                        video_url = playlist.video_urls[index]
                        try:
                            yt = YouTube(video_url, on_progress_callback=on_progress)
                            playlist_folder = f'./{playlist.title}'
                            if not os.path.exists(playlist_folder):
                                os.makedirs(playlist_folder)
                            if format_choice == 'v':
                                while True:
                                    streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
                                    print("[ $ ] =======>>>> Pilihan resolusi yang tersedia:")
                                    for i, stream in enumerate(streams):
                                        print(f"{i + 1}. {stream.resolution} - {stream.mime_type}")
                                    
                                    try:
                                        choice = input("[ $ ] =======>>>> Pilih resolusi (masukkan nomor pilihan)\n atau ketik 'k' untuk memilih format lagi: ").strip().lower()
                                        if choice == 'k':
                                            break
                                        choice = int(choice) - 1
                                        if 0 <= choice < len(streams):
                                            stream = streams[choice]
                                            output_path = playlist_folder
                                            if not os.path.exists(output_path):
                                                os.makedirs(output_path)
                                            stream.download(output_path)
                                            print(f"\n[ $ ] =======>>>> Video '{yt.title}' dengan resolusi {stream.resolution} telah berhasil diunduh ke '{output_path}'")
                                            break
                                        else:
                                            print("[ ! ] =======>>>> Pilihan tidak ada bro. Silakan coba lagi.")
                                    except ValueError:
                                        print("[ ! ] =======>>>> Input tidak ada. Silakan masukkan nomor yang sesuai.")
                                break
                            elif format_choice == 'a':
                                stream = yt.streams.filter(only_audio=True).first()
                                output_path = playlist_folder
                                if not os.path.exists(output_path):
                                    os.makedirs(output_path)
                                out_file = stream.download(output_path)
                                base, ext = os.path.splitext(out_file)
                                new_file = base + '.mp3'
                                os.rename(out_file, new_file)
                                print(f"\n[ $ ] =======>>>> Audio '{yt.title}' telah berhasil diunduh dan disimpan sebagai MP3 di '{new_file}'")
                            else:
                                print("[ ! ] =======>>>> Format pilihan tidak ada. coba ketik 'v' atau 'a'.")
                        except Exception as e:
                            print(f"[ ! ] =======>>>> Gagal mengunduh video dari URL: {video_url}")
                            print(f"[ ! ] =======>>>> Kesalahan: {e}")
                    break
                else:
                    print("[ ! ] =======>>>> Format pilihan tidak ada. Pilih 'v' atau 'a'.")
        except Exception as e:
            print(f"[ ! ] =======>>>> Terjadi kesalahan: {e}")
download_youtube_video()
