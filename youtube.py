import tkinter as tk
from tkinter import ttk, messagebox
from pytube import YouTube, exceptions
from moviepy.editor import VideoFileClip
import os
import threading
import queue
import logging

class YouTubeTrimmerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Trimmer")
        self.root.geometry("600x250")
        self.root.resizable(False, False)
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TEntry", font=("Arial", 12))
        self.create_widgets()
        self.queue = queue.Queue()
        logging.basicConfig(filename='trim_video.log', level=logging.DEBUG)

    def create_widgets(self):
        self.url_label = ttk.Label(self.root, text="YouTube URL:")
        self.url_label.grid(column=0, row=0, padx=10, pady=10, sticky="W")
        self.url_entry = ttk.Entry(self.root, width=50)
        self.url_entry.grid(column=1, row=0, padx=10, pady=10, sticky="W")
        self.download_button = ttk.Button(self.root, text="Download and Trim", command=self.start_download_and_trim)
        self.download_button.grid(column=0, row=1, columnspan=2, pady=10)
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=500, mode="determinate")
        self.progress.grid(column=0, row=2, columnspan=2, padx=10, pady=20)
        self.status_label = ttk.Label(self.root, text="Status: Ready")
        self.status_label.grid(column=0, row=3, columnspan=2, padx=10, pady=10)
        self.output_dir = os.path.join(os.path.expanduser("~"), "Desktop", "YouTube_Reels")
        os.makedirs(self.output_dir, exist_ok=True)

    def update_status(self, message):
        self.status_label.config(text=f"Status: {message}")
        self.root.update_idletasks()

    def start_download_and_trim(self):
        thread = threading.Thread(target=self.download_and_trim)
        thread.start()
        self.root.after(100, self.update_progress)

    def download_and_trim(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL.")
            return

        try:
            self.update_status("Downloading video...")
            yt = YouTube(url)
            stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
            if not stream:
                messagebox.showerror("Error", "No suitable stream found.")
                self.update_status("Ready")
                return

            video_path = stream.download(output_path=self.output_dir)
            self.update_status("Download complete. Trimming video...")
            self.trim_video(video_path)
            self.update_status("Video trimming complete")
            messagebox.showinfo("Success", f"Video downloaded and trimmed to {self.output_dir}")
        except exceptions.VideoUnavailable:
            messagebox.showerror("Error", "Video unavailable.")
            self.update_status("Ready")
        except exceptions.VideoPrivate:
            messagebox.showerror("Error", "Video is private.")
            self.update_status("Ready")
        except exceptions.RegexMatchError:
            messagebox.showerror("Error", "Invalid YouTube URL.")
            self.update_status("Ready")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            self.update_status("Ready")
            logging.error(f"An unexpected error occurred: {e}")

    def trim_video(self, video_path):
        try:
            clip = VideoFileClip(video_path)
            duration = int(clip.duration)
            num_segments = duration // 60 + 1
            total_clips = num_segments

            for i in range(num_segments):
                start = i * 60
                if start >= duration:
                    break 
                end = min(start + 60, duration)
                output_path = os.path.join(self.output_dir, f"part-{i + 1}_{os.path.basename(video_path)}")
                self.queue.put(("update_progress", (i + 1, total_clips)))
                self.queue.put(f"Writing clip from {start} to {end}...")
                try:
                    clip.subclip(start, end).write_videofile(output_path, codec="libx264")
                except Exception as e:
                    messagebox.showerror("Error", f"Error writing clip from {start} to {end}: {e}")
                    logging.error(f"Error writing clip from {start} to {end}: {e}")
                    break
            clip.close()
            self.queue.put(("done", (total_clips,)))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during video trimming: {e}")
            self.update_status("Ready")
            print(f"Error during video trimming: {e}")
            logging.error(f"An error occurred during video trimming: {e}")

    def update_progress(self):
        while not self.queue.empty():
            message = self.queue.get()
            if message[0] == "update_progress":
                segment, total = message[1]
                self.progress["value"] = segment
                self.progress["maximum"] = total
            elif message[0] == "done":
                self.update_status("Video trimming complete")
            else:
                self.update_status(message)
        self.root.after(100, self.update_progress)

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeTrimmerApp(root)
    root.mainloop()
