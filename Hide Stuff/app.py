import tkinter as tk
import os
import sys
import cv2 as cv
from image import *

class App(tk.Frame):
    def __init__( self, master=None ):
        super().__init__( master )
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets( self ):
        self.hi_there = tk.Button( self, text="HOI THERE", fg="red",
                                   command=self.text )
        self.hi_there.pack( side="top" )
    
    def text( self ):
        print( "Diely" )

def switch( option, carrier, save_loc ):

    # Hide a manual entry
    def manual_text():
        message = input( "Type in what you would like to hide: " )
        encode_message( message, carrier, save_loc )

    # Hide a text file
    def text_file():
        text_path = input( "Type in the text file path: " )
        if not os.path.isfile( text_path ):
            sys.exit( "ERROR: Text File Not Found!" )
        encode_message( read_book( text_path ), carrier, save_loc )

    # Hide another image
    def image_file():
        image_path = input( "Type in the image file path: " )
        if not os.path.isfile( image_path ):
            sys.exit( "ERROR: Image File Not Found!" )
        encode_image( image_path, carrier, save_loc )

    # Hide an audio clip
    def audio_file():
        audio_path = input( "Type in the audio file path: " )

    # Hide a video clip
    def video_file():
        video_path = input( "Type in the video file path: " )

    # Default case
    def default():
        sys.exit( "Somehow you got this to run.\n" )

    # Retrieve desired case
    dict = {
        0 : manual_text,
        1 : text_file,
        2 : image_file,
        3 : audio_file,
        4 : video_file
    }

    # Returns the function matching the case id
    dict.get( option, default )()

#root = tk.Tk(screenName=":LSLKF:LJASLHFSD")
#myapp = App(root)
#myapp.mainloop()
clear_screen = lambda : os.system( "cls" if os.name == "nt" else "clear" )
file_path = input( "\nGive Carrier File: " )

supported = ( ".png" )

if not file_path.endswith( supported ):
    sys.exit( "Image format not supported!\nAvailable: PNG\n" )
elif not os.path.isfile( file_path ):
    sys.exit( "ERROR: File Not Found!" )

modified_location = input( "Output File Name: " ) + ".png"

allowed = set( "01234" )

stopped = False
while not stopped:
    print( "\nPick a sender: \n" )
    print( "0. Manual Text Entry\n" +
           "1. Text File\n" +
           "2. Image\n" +
           "3. Audio\n" +
           "4. Video\n" )

    answer = input( "Enter Number: " )
    if answer and allowed.issuperset( answer ):
        # Load image
        image = cv.imread( file_path )
        # Custom switch takes over from here
        switch( int( answer ), image, modified_location )
        stopped = True

    else:
        clear_screen()
        print( "INVALID OPTION. GO DIE.\n" )
