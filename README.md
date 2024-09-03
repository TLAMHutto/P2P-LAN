# LAN Streaming & Screenshot Capture with OCR

This project provides a simple Python-based application for streaming video from one computer to another over a Local Area Network (LAN). In addition to streaming, it includes a draggable screenshot tool that allows users to capture images from the client's screen, with the ability to convert these images to text using Optical Character Recognition (OCR).

## Features

-   **LAN Streaming:** Stream video content from one computer to another over the same LAN.
-   **Draggable Screenshot Tool:** Easily capture any portion of the client's screen by dragging a selection box.
-   **OCR Integration:** Convert captured images to text directly within the application using OCR technology.

## Requirements

Before running the app, ensure you have the following installed:

-   Python 3.x
-   [OpenCV](https://opencv.org/) (for video streaming and image capture)
-   [PyQt5](https://pypi.org/project/PyQt5/) (for GUI and draggable screenshot tool)
-   [Tesseract-OCR](https://github.com/tesseract-ocr/tesseract) (for Optical Character Recognition)
-   [Socket](https://docs.python.org/3/library/socket.html) (for handling the LAN streaming)
-   [Pillow](https://python-pillow.org/) (for image handling)

## Installation

1.  **Clone the repository:**
    
    bash
    
    Copy code
    
    `git clone https://github.com/TLAMHutto/P2P-LAN`
    
    
2.  **Install Tesseract:**
    
    -   **Windows:** Download and install from [here](https://github.com/tesseract-ocr/tesseract/wiki).
    -   **Linux:** Install via package manager, e.g., `sudo apt-get install tesseract-ocr`.
    -   **macOS:** Install via Homebrew, `brew install tesseract`.

## Usage

### Server (Streaming Computer)

1.  Run the client script on the computer you want to stream from:
    
    ./Client/clientGUI.py

    bash
    
    Copy code
    
    `python clientGUI.py`

    ***For the moment the ip address and port are hard coded, for personal use you will need to modify the client code to fit your network.

    ```
    class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Client")

        # Hard-coded server IP address
        self.server_ip = '192.168.0.19'
        self.server_port = 9999
    ```
    
2.  The server will start streaming video to any connected client within the same LAN.
    

### Client (Receiving Computer)

1.  Run the server script on the computer you want to receive the stream:
    
    ./Server/main.py

    bash
    
    Copy code
    
    `python main.py`
    
2.  A GUI will appear with options to start streaming, take a screenshot, and convert captured images to text.
    

### Screenshot & OCR

1.  Click on the "Edit" -> "Snip" button in the client application.
2.  Drag your mouse over the area of the screen you want to capture.
3.  The captured image will be displayed, with an option to convert it to text using OCR.
4.  Text will be saved in Server/imgTxt - Screenshot is saved in Server/screenshots

## Acknowledgements

-   [OpenCV](https://opencv.org/)
-   [PyQt5](https://pypi.org/project/PyQt5/)
-   [Tesseract-OCR](https://github.com/tesseract-ocr/tesseract)
-   [Pillow](https://python-pillow.org/)

## WIP priority objectives
1. Enhancing the server-side streaming window to reduce lag and improve responsiveness.
2. Unifying all components into a single, cohesive GUI to enhance the overall user experience.
3. Upgrading the streaming functionality to deliver a smooth video stream at approximately 30fps, replacing the current 5-second interval screenshots.

## Secondary objectives
1. **Optimize Network Usage:**
   - Implement adaptive bitrate streaming to adjust the quality of the stream based on network conditions, which could help reduce lag and improve responsiveness.
   - Explore the use of more efficient video codecs like H.264 or H.265 to reduce bandwidth usage while maintaining video quality.

2. **Implement Error Handling and Reconnection Logic:**
   - Add robust error handling to manage network interruptions or client-server disconnections. Automatic reconnection logic can help ensure a smooth user experience during streaming.

3. **Add Audio Streaming (Optional):**
   - If applicable, consider adding audio streaming to complement the video stream. This would provide a more complete streaming experience.

4. **Cross-Platform Compatibility:**
   - Test and ensure the application works across different operating systems (Windows, macOS, Linux). This might involve handling OS-specific quirks, especially for the GUI and networking components.

5. **Security Enhancements:**
   - Implement basic security features, such as authentication, encryption (e.g., SSL/TLS), and access controls, to ensure that the stream and screenshots are secure from unauthorized access.

6. **Testing and Performance Profiling:**
   - Regularly profile the performance of your application to identify bottlenecks. Use tools like `cProfile` for Python to analyze where improvements can be made in terms of CPU and memory usage.

7. **Documentation and Tutorials:**
   - As you integrate all features into a single GUI, update the documentation accordingly. Consider adding a user guide or video tutorial to help new users understand how to set up and use the application.