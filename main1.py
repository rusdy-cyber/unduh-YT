from pytube import YouTube
import os

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    print(f"Proses unduh: {percentage:.2f}% selesai", end="\r")

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

    # Kode untuk mengunduh video YouTube disini

    # Meminta pengguna untuk memasukkan URL video YouTube
    video_url = input("masukkan link: ")

    try:
        # Buat objek YouTube dan tambahkan callback untuk progress
        yt = YouTube(video_url, on_progress_callback=on_progress)

        # Meminta pengguna untuk memilih format unduhan
        format_choice = input("Pilih format unduhan (video/audio): ").strip().lower()

        if format_choice == 'video':
            # Menampilkan semua stream yang tersedia dengan format video
            streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
            print("Pilihan resolusi yang tersedia:")
            for i, stream in enumerate(streams):
                print(f"{i + 1}. {stream.resolution} - {stream.mime_type}")

            # Meminta pengguna untuk memilih resolusi
            choice = int(input("Pilih resolusi (masukkan nomor pilihan): ")) - 1

            # Memastikan pilihan valid
            if 0 <= choice < len(streams):
                stream = streams[choice]

                # Tentukan lokasi di mana Anda ingin menyimpan video
                output_path = './downloaded_videos'  # Anda bisa mengganti dengan jalur direktori yang diinginkan

                # Membuat direktori jika belum ada
                if not os.path.exists(output_path):
                    os.makedirs(output_path)

                # Unduh video
                stream.download(output_path)
                print(f"\nVideo '{yt.title}' dengan resolusi {stream.resolution} telah berhasil diunduh ke '{output_path}'")
            else:
                print("Pilihan tidak valid.")

        elif format_choice == 'audio':
            # Mendapatkan stream audio terbaik
            stream = yt.streams.filter(only_audio=True).first()

            # Tentukan lokasi di mana Anda ingin menyimpan audio
            output_path = './downloaded_audios'  # Anda bisa mengganti dengan jalur direktori yang diinginkan

            # Membuat direktori jika belum ada
            if not os.path.exists(output_path):
                os.makedirs(output_path)

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
        print(f"Terjadi kesalahan: {e}")

# Panggil fungsi untuk memulai proses pengunduhan
download_youtube_video()