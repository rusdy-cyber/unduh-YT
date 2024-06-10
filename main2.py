from pytube import YouTube, Playlist
from colorama import Fore
import os

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    print(f"Proses unduh: {percentage:.2f}% selesai", end="\r")

def download_youtube_video():
    print(Fore.GREEN + """
██╗░░░██╗████████╗░░░░░░██╗░░░██╗███╗░░██╗██████╗░██╗░░░██╗██╗░░██╗
╚██╗░██╔╝╚══██╔══╝░░░░░░██║░░░██║████╗░██║██╔══██╗██║░░░██║██║░░██║
░╚████╔╝░░░░██║░░░█████╗██║░░░██║██╔██╗██║██║░░██║██║░░░██║███████║
░░╚██╔╝░░░░░██║░░░╚════╝██║░░░██║██║╚████║██║░░██║██║░░░██║██╔══██║
░░░██║░░░░░░██║░░░░░░░░░╚██████╔╝██║░╚███║██████╔╝╚██████╔╝██║░░██║
░░░╚═╝░░░░░░╚═╝░░░░░░░░░░╚═════╝░╚═╝░░╚══╝╚═════╝░░╚═════╝░╚═╝░░╚═╝
""")
    # Meminta pengguna untuk memasukkan URL playlist YouTube
    playlist_url = input("Masukkan URL playlist: ")
    try:
        # Buat objek Playlist dari URL
        playlist = Playlist(playlist_url)

        # Menampilkan daftar judul semua playlist
        print("Daftar Playlist:")
        for i, pl in enumerate(playlist.video_urls):
            print(f"{i+1}. {pl}")

        # Meminta pengguna untuk memilih playlist (bisa lebih dari satu)
        selected_playlists_indices = []
        while True:
            playlist_choice = input("Masukkan nomor playlist (kosongkan untuk selesai): ").strip()
            if not playlist_choice:
                break
            try:
                choice = int(playlist_choice) - 1
                if 0 <= choice < len(playlist.video_urls):
                    selected_playlists_indices.append(choice)
                else:
                    print(f"Nomor playlist {playlist_choice} tidak valid.")
            except ValueError:
                print(f"Input '{playlist_choice}' tidak valid.")

        # Meminta pengguna untuk memilih format unduhan
        format_choice = input("Pilih format unduhan (video/audio): ").strip().lower()

        for index in selected_playlists_indices:
            video_url = playlist.video_urls[index]
            try:
                # Buat objek YouTube dan tambahkan callback untuk progress
                yt = YouTube(video_url, on_progress_callback=on_progress)

                # Membuat direktori untuk playlist jika belum ada
                playlist_folder = f'./{playlist.title}'
                if not os.path.exists(playlist_folder):
                    os.makedirs(playlist_folder)

                if format_choice == 'video':
                    # Menampilkan semua stream yang tersedia dengan format video
                    streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
                    # Memilih stream dengan kualitas terbaik
                    stream = streams.first()
                    # Tentukan lokasi di mana Anda ingin menyimpan video
                    output_path = playlist_folder  # Folder playlist
                    # Unduh video
                    out_file = stream.download(output_path)
                    print(f"\nVideo '{yt.title}' dengan resolusi {stream.resolution} telah berhasil diunduh ke '{output_path}'")
                elif format_choice == 'audio':
                    # Menampilkan semua stream yang tersedia dengan format audio
                    stream = yt.streams.filter(only_audio=True).first()
                    # Tentukan lokasi di mana Anda ingin menyimpan audio
                    output_path = playlist_folder  # Folder playlist
                    # Unduh audio
                    out_file = stream.download(output_path)
                    # Mengubah nama file ke format MP3
                    base, ext = os.path.splitext(out_file)
                    new_file = base + '.mp3'
                    os.rename(out_file, new_file)
                    print(f"\nAudio '{yt.title}' telah berhasil diunduh dan disimpan sebagai MP3 di '{new_file}'")
                else:
                    print("Format pilihan tidak valid. Pilih 'video' atau 'audio'.")
            except Exception as e:
                print(f"Gagal mengunduh video dari URL: {video_url}")
                print(f"Kesalahan: {e}")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

# Panggil fungsi untuk memulai proses pengunduhan
download_youtube_video()