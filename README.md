# video-trimmer

# YouTube Video Trimmer

YouTube Video Trimmer is a simple desktop application that allows users to download and trim YouTube videos into 1-minute segments. The application is built using Python and leverages the `pytube` library for downloading videos and `moviepy` for trimming them. The GUI is built using `tkinter`.

## Features

- Download YouTube videos by providing a URL.
- Automatically trim the downloaded video into 1-minute segments.
- Save the trimmed video segments to a specified directory on your desktop.

## Prerequisites

- Python 3.x
- `tkinter` (usually comes with Python installations)
- `pytube` library
- `moviepy` library

## Installation

1. Clone this repository or download the source code.
2. Install the required Python libraries using pip:

   ```sh
   pip install pytube moviepy






## Usage
Run the application:

sh
Copy code
python your_script_name.py
Enter the YouTube video URL in the provided input field.

Click the "Download and Trim" button.

The application will download the video and trim it into 1-minute segments, saving the segments to a folder named YouTube_Reels on your desktop.

## Code Overview
The application is structured as follows:

YouTubeTrimmerApp: The main application class.
__init__: Initializes the application, sets up the GUI components, and configures logging.
create_widgets: Creates and arranges the GUI components.
update_status: Updates the status label in the GUI.
start_download_and_trim: Starts the download and trim process in a separate thread.
download_and_trim: Downloads the YouTube video and trims it into segments.
trim_video: Trims the downloaded video into 1-minute segments.
update_progress: Updates the progress bar based on the current segment being processed.

## Logging
The application logs errors and other important events to a file named trim_video.log in the same directory as the script.

## Error Handling
The application handles various errors, such as:

Invalid YouTube URL
Video unavailable
Private video
Errors during video trimming
Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements
pytube for downloading YouTube videos.
moviepy for video editing.
tkinter for the GUI.