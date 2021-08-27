Window Magnifier
---

A command line utility for magnifying a single application. This works by:
1. Capturing the section of your screen, which the application to magnify is positioned, as an image
2. Scaling the image based on the selected magnification level
3. And finally displaying the scaled image in another application

This application doesn't just take a single screenshot and upscale it. It will perform the above actions
continuously, up to a maximum of 100 times per second, until the program is closed.

**Important**: The application to be magnified must be visible. This will not work if the application you want to
magnify is hidden behind another window or if it is minimized.

It would likely be best to have the application to be magnified and the application to display the magnified
image result on separate monitors.

### Running
To use the utility run the following two command:
> pip install -r requirements.txt
 
Followed by:
> python magnifier.py

Once running a window will popup that will allow you to select the window to magnify and the magnification level.