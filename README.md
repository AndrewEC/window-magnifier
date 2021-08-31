Window Magnifier
---

A command line utility for magnifying a single application. This works by:
1. Capturing the visible content of the target application that we want to magnify as an image
2. Scaling the image to fit within the bounds of the magnifier display window
3. And finally displaying the scaled image in the magnifier display window

This application doesn't just take a single screenshot and upscale it. It will perform the above actions
continuously until the program is closed.

**Important**: The application to be magnified cannot be minimized. Otherwise the application can be hidden behind other
windows or even hidden off-screen.

### Running
This program requires Python 3 to be installed and can be launched using `launch.bat`.