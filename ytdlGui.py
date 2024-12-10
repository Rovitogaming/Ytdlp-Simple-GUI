import tkinter
import tkinter.messagebox
import customtkinter
import subprocess
import threading

customtkinter.set_appearance_mode("dark")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Youtube Downloader")
        self.geometry(f"{400}x{300}")
        self.resizable(False, False)

        self.videoLinkLabel = customtkinter.CTkLabel(self, text="Youtube Video URL:")
        self.videoLinkLabel.pack(side=tkinter.TOP, pady=10)

        self.videoLinkBox = customtkinter.CTkEntry(self, width=350)
        self.videoLinkBox.pack(side=tkinter.TOP)
        
        self.videoLinkLabel = customtkinter.CTkLabel(self, text="Download Format:")
        self.videoLinkLabel.pack(side=tkinter.TOP, pady=10)

        self.formatDropdown = customtkinter.CTkOptionMenu(self, values=["Video", "mp3", "wav", "flac"])
        self.formatDropdown.set("mp3")
        self.formatDropdown.pack(side=tkinter.TOP)
        
        self.statusLabel = customtkinter.CTkLabel(self, text="No Downloads In Progress")
        self.statusLabel.pack(side=tkinter.BOTTOM, pady=5)

        self.button = customtkinter.CTkButton(self, command=self.start_download, text="Download")
        self.button.pack(side=tkinter.BOTTOM)
        

    def start_download(self):
        videoLink = self.videoLinkBox.get()
        videoFormat = self.formatDropdown.get()
        print(videoLink)
        print(videoFormat)
        self.button.configure(state="disabled")
        self.statusLabel.configure(text=f"Downloading: {videoLink}", text_color="white")
        
        def downloadFailed():
            self.button.configure(state="active")
            self.statusLabel.configure(text=f"Download Failed!", text_color="red")

        def downloadThread(self, videoLink, downloadFailed, format):
            try:
                if format != "Video":
                    print("Format is of type: audio")
                    print(f"Audio format: {format}")
                    subprocess.check_call(["yt-dlp.exe", "-x", "--audio-format", format, "-o", r"%USERPROFILE%\Downloads\%(title)s-%(id)s.%(ext)s", "--no-mtime", videoLink])
                else:
                    print("Format is of type: video")
                    subprocess.check_call(["yt-dlp.exe", "-o", r"%USERPROFILE%\Downloads\%(title)s-%(id)s.%(ext)s", "--no-mtime", "-f", "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / bv*+ba/b", videoLink])
                self.button.configure(state="active")
                self.statusLabel.configure(text=f"Download Completed!", text_color="green")
            except subprocess.CalledProcessError as e:
                tkinter.messagebox.showerror("Error", e)
                downloadFailed()

        if videoLink == "":
            tkinter.messagebox.showerror("Error", "Please input a youtube video link!")
            downloadFailed()
            return
        
        if not "https://www.youtube.com/watch?v=" in videoLink:
            tkinter.messagebox.showerror("Error", "Video link is not valid!\n\nExample Valid Link:\nhttps://www.youtube.com/watch?v=dQw4w9WgXcQ")
            downloadFailed()
            return
        
        threading.Thread(target=downloadThread, args=[self, videoLink, downloadFailed, videoFormat], daemon=True).start()
        

if __name__ == "__main__":
    app = App()
    app.mainloop()