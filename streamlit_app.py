import streamlit as st
import os
import yt_dlp
import shutil
import time


def cleanup_old_folders(base_path="downloads", max_age_seconds=3600):
    """Delete folders older than max_age_seconds (default 1 hour)."""
    now = time.time()
    if os.path.exists(base_path):
        for folder in os.listdir(base_path):
            folder_path = os.path.join(base_path, folder)
            if os.path.isdir(folder_path):
                folder_age = now - os.path.getmtime(folder_path)
                if folder_age > max_age_seconds:
                    shutil.rmtree(folder_path, ignore_errors=True)


def get_short_links(channel_url, max_links=100):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'playlist_end': max_links,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Referer': 'https://www.youtube.com/',
        },
    }

    if '/@' in channel_url:
        channel_username = channel_url.split('/@')[1].split('/')[0]
        channel_url = f'https://www.youtube.com/@{channel_username}/shorts'
    else:
        channel_url = channel_url.split('/about')[0]
        channel_url = channel_url.split('/community')[0]
        channel_url = channel_url.split('/playlist')[0]
        channel_url = channel_url.split('/playlists')[0]
        channel_url = channel_url.split('/streams')[0]
        channel_url = channel_url.split('/featured')[0]
        channel_url = channel_url.split('/videos')[0]
        channel_url += '/shorts'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(channel_url, download=False)
        if 'entries' in result:
            video_ids = [entry['id'] for entry in result['entries']]
            return [f'https://www.youtube.com/shorts/{vid}' for vid in video_ids][:max_links]
        else:
            st.warning("No videos found.")
            return []


def download_videos(links, output_path):
    total = len(links)
    progress_bar = st.progress(0)
    status_text = st.empty()

    for idx, link in enumerate(links, 1):
        ydl_opts = {
            'quiet': True,
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                'Referer': 'https://www.youtube.com/',
            },
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
            status_text.success(f"✅ Downloaded {idx}/{total}: {link}")
        except Exception as e:
            status_text.error(f"❌ Failed {idx}/{total}: {link} - {e}")

        progress_bar.progress(idx / total)

    status_text.info("🎉 Download process completed!")


# ---- Streamlit UI ----

st.title("📥 Shorts Bulk Downloader")
st.markdown("Download multiple YouTube Shorts from a channel at once.")

channel_url = st.text_input("🔗 Enter YouTube channel URL:")
folder_name = st.text_input("📁 Folder name to save videos (inside ./downloads):", value="default_folder")
num_videos = st.number_input("🎯 How many shorts to download?", min_value=1, max_value=100, value=10, step=1)

if st.button("Start Download"):
    if not channel_url.strip():
        st.warning("Please enter a valid channel URL.")
    else:
        cleanup_old_folders()  # Clean old folders first

        download_dir = os.path.join("downloads", folder_name)
        os.makedirs(download_dir, exist_ok=True)

        st.write("🔍 Extracting short links...")
        short_links = get_short_links(channel_url, max_links=num_videos)

        if short_links:
            st.success(f"Found {len(short_links)} videos. Starting download...")
            download_videos(short_links, download_dir)

            # Create ZIP file
            zip_path = shutil.make_archive(download_dir, 'zip', download_dir)
            st.success("All downloads completed!")

            # Show total ZIP file size
            zip_size_mb = os.path.getsize(zip_path) / (1024 * 1024)
            st.info(f"📦 Total ZIP size: {zip_size_mb:.2f} MB")

            with open(zip_path, "rb") as f:
                st.download_button(
                    label="📦 Download All Videos as ZIP",
                    data=f,
                    file_name=f"{folder_name}.zip",
                    mime="application/zip"
                )
        else:
            st.error("No shorts found or failed to extract links.")
