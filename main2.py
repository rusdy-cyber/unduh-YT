from pytube import YouTube, Playlist
from colorama import Fore
import os

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    print(Fore.GREEN +f"[ * ] ==>>>> Proses unduh: {percentage:.2f}% bentar", end="\r")

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
        playlist_url = input(Fore.LIGHTBLACK_EX +"linux㉿root)\n|=# Masukkan URL playlist: ")
        try:
            playlist = Playlist(playlist_url)
            print("==>>>> Daftar Video dalam Playlist:")
            for i, video_url in enumerate(playlist.video_urls):
                yt = YouTube(video_url)
                print(f"{i+1}. {yt.title}")
            selected_videos_indices = []
            while True:
                video_choice = input(Fore.LIGHTBLACK_EX +"---------------------------------------------------\n==>>>> Masukkan nomor video (kosongkan untuk selesai)\nlinux㉿root)\n|=# ketikkan: ").strip()
                if not video_choice:
                    break
                try:
                    choice = int(video_choice) - 1
                    if 0 <= choice < len(playlist.video_urls):
                        selected_videos_indices.append(choice)
                    else:
                        print(Fore.RED + f"[ ! ] ==>>>> Nomor video {video_choice} tidak valid.")
                except ValueError:
                    print(Fore.RED + f"[ ! ] ==>>>> Input '{video_choice}' tidak valid.")
            while True:
                format_choice = input(Fore.LIGHTBLACK_EX + "---------------------------------------------------\n==>>>> Pilih format unduhan (video/audio)\nketik [v] => untuk video\nketik [a] => untuk audio\nketik [k] => untuk mengubah URL playlist\n---------------------------------------------------\n(linux㉿root)\n|=# ketikkan: ").strip().lower()
                if format_choice == 'k':
                    break
                if format_choice in ['v', 'a']:
                    if format_choice == 'v':
                        yt_example = YouTube(playlist.video_urls[selected_videos_indices[0]])
                        streams = yt_example.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
                        print("--------------------------------------------------------\n==>>>> Pilihan resolusi yang tersedia:")
                        for i, stream in enumerate(streams):
                            print(f"{i + 1}. {stream.resolution} - {stream.mime_type}")

                        while True:
                            try:
                                resolution_choice = input("==>>>> Pilih resolusi (masukkan nomor pilihan) atau ketik 'k' untuk memilih format lagi\n--------------------------------------------------------\nlinux㉿root)\n|=# ketikkan: ").strip().lower()
                                if resolution_choice == 'k':
                                    break
                                resolution_choice = int(resolution_choice) - 1
                                if 0 <= resolution_choice < len(streams):
                                    selected_stream = streams[resolution_choice]
                                    for index in selected_videos_indices:
                                        video_url = playlist.video_urls[index]
                                        try:
                                            yt = YouTube(video_url, on_progress_callback=on_progress)
                                            playlist_folder = f'./{playlist.title}'
                                            if not os.path.exists(playlist_folder):
                                                os.makedirs(playlist_folder)
                                            output_path = playlist_folder
                                            selected_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()[resolution_choice]
                                            selected_stream.download(output_path)
                                            print(f"\n==>>>> Video '{yt.title}' dengan resolusi {selected_stream.resolution} telah berhasil diunduh ke '{output_path}'")
                                        except Exception as e:
                                            print(Fore.RED + f"[ ! ] ==>>>> Gagal mengunduh video dari URL: {video_url}")
                                            print(Fore.RED + f"[ ! ] ==>>>> Kesalahan: {e}")
                                    break
                                else:
                                    print(Fore.RED + "[ ! ] ==>>>> Pilihan tidak ada bro. Silakan coba lagi.")
                            except ValueError:
                                print(Fore.RED + "[ ! ] ==>>>> Input tidak valid. Silakan masukkan nomor yang sesuai.")
                    elif format_choice == 'a':
                        for index in selected_videos_indices:
                            video_url = playlist.video_urls[index]
                            try:
                                yt = YouTube(video_url, on_progress_callback=on_progress)
                                playlist_folder = f'./{playlist.title}'
                                if not os.path.exists(playlist_folder):
                                    os.makedirs(playlist_folder)
                                output_path = playlist_folder
                                stream = yt.streams.filter(only_audio=True).first()
                                out_file = stream.download(output_path)
                                base, ext = os.path.splitext(out_file)
                                new_file = base + '.mp3'
                                os.rename(out_file, new_file)
                                print(f"\n==>>>> Audio '{yt.title}' telah berhasil diunduh dan disimpan sebagai MP3 di '{new_file}'")
                            except Exception as e:
                                print(Fore.RED + f"[ ! ] ==>>>> Gagal mengunduh video dari URL: {video_url}")
                                print(Fore.RED + f"[ ! ] ==>>>> Kesalahan: {e}")
                    break
                else:
                    print(Fore.RED + "[ ! ] ==>>>> Format pilihan tidak valid. Pilih 'video' atau 'audio'.")
        except Exception as e:
            print(Fore.RED + f"[ ! ] ==>>>> Terjadi kesalahan: {e}")

# Panggil fungsi untuk memulai proses pengunduhan
download_youtube_video()
