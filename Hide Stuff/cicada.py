# -*- coding: utf-8 -*-

import cv2 as cv
import sys
import os

delimiter = "$t3g0"

def set_bit( num, index, bit ):
    # Shift mask to specified bit
    mask = 1 << index 
    # NAND masked bit to clear it
    num &= ~mask 
    adjusted_bit = ( ( bit << index ) & mask )
    return ( num | adjusted_bit )

def dec2bin( dec, length ):
    # Create a binary string of the decimal
    # [2:] b/c the full string begins w/ "0b"
    x = bin( dec )[2:]
    # While specified bit len isn't met
    # pad with 0s
    while len( x ) < length:
        x = '0' + x
    return x 

def encode_message( secret, image, total_pixels, needed_pixels ):
    '''
    LSB - Least Significant Bit Steganography
    # Each pixel under openCV is a collection of BGR - 8bit values
    # The idea is to hide 3 bits at a time into each set of BGR
    # Of course, the target is the LSB of each channel
    # Bitwise manipulation is needed here, solved by set_bit()
    '''
    # - - -
    height, width, channels = image.shape
    
    # Worst Case Time Complexity: height * width * channels
    # Scroll across each pixel hiding the data
    def fruit_loops( secret, height, width, needed_pixels, image ):
        index = 0

        for y in range( height ):
            for x in range( width ):
                # Brush through the BGR of a pixel
                for i in range( channels ):
                    # Loops are limited by string length
                    if index >= needed_pixels: return image
                    # Replace bits with binary string
                    bit = int( secret[index], 2 )
                    old = image.item( y, x, i )
                    old = set_bit( old, 0, bit )
                    image.itemset( ( y, x, i ), old )
                    # Increase message index
                    index += 1
    
    # MMMMMMMMMTHISMAKESMEUNCOMFYYYYYYYYYAAAAAAAAAAAAAAAAAAA
    image = fruit_loops( secret, height, width, needed_pixels, image )
    
    # Save the encrypted image to a new location
    new_file = "agentD.png"
    # cv.imwrite() is a bool function
    # Use as a flag for saving errors
    saved = cv.imwrite( new_file, image )

    # - - -
    if not saved:
        sys.exit( "Error While Saving Image" )
    else:
        print( "Image Saved Successfully to \"agentD.png\"" )
        return new_file

def decode_message( path ):
    # Open the desired image
    decode = cv.imread( path )
    # Retreive dimensions of the desired image
    height, width, channels = decode.shape
    total_pixels = height * width

    # Hold the raw encrypted data
    hidden_bits = ""

    # 
    def fruit_loops( hidden_bits, height, width, decode ):
        for y in range( height ):
            for x in range( width ):
                # Bush through the BGR of a pixel
                for i in range( channels ):
                    hidden_bits += ( bin( decode.item( y, x, i ) )[2:][-1] )
        # "hidden_bits" is just 1 string of everything
        return hidden_bits
    
    # ISTILLDONTLIKETHISAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    hidden_bits = fruit_loops( hidden_bits, height, width, decode )

    # So now it's time to group these bits into 8
    # using some weird ass Python nonsense
    hidden_bits = [ hidden_bits[ i:i+8 ] for i in range( 0, len( hidden_bits ), 8 ) ]

    message = ""

    # Basically decrypt the letters until the tag is reached
    for string in hidden_bits:
        if message[-5:] == "$t3g0":
            break
        else:
            message += chr( int( string, 2 ) )

    # It's possible there is no message to be found
    # or there actually IS one but it doesn't have the
    # "$t3g0" tag so uhhhhh
    if "$t3g0" in message:
        #print( "\nDecoded Message:\n\n" + message[:-5] + '\n' )
        print( "Decoded Message Saved to: decoded_message.txt\n" )
        with open( "decoded_message.txt", encoding="ascii", mode="w" ) as f:
            f.write( message )
    else:
        print( "\nNo Hidden Message Found\n" )
        #print( message + "\n:(\n" )

def read_book( book_path ):
    words = None

    with open( book_path, errors="backslashreplace", encoding="ascii", mode="r" ) as f:
        words = f.read()

    return words

def image_stego( clear_screen ):
    global delimiter
    clear_screen()

    stopped = False
    allowed = set( "textimage" )
    image_wanted = False

    while not stopped:
        print( "\nWhat are you hiding? \n" )
        print( "- Text" )
        print( "- Image" )

        answer = input( "\nEnter Input: " ).lower()
        if answer and allowed.issuperset( answer ):

            clear_screen()
            print()

            stopped = True

            if answer == "text":
                message = input( "Type in your message: " ) + delimiter

            elif answer == "image":
                image_wanted = True
                image_hide_path = input( "Make My Life Harder Why Don't You.\n\nGive the Image Path Then: " )
                hidden_image = cv.imread( image_hide_path )

                while hidden_image is None:
                    clear_screen()
                    image_hide_path = input( "\nERROR: Image to Hide Not Found. Try Again: " )
                    hidden_image = cv.imread( image_hide_path )

    sys.exit(0)

    # Read in the image
    # 'image' is now an array of BGR pixels
    # Reading the image reverses the color model
    image = cv.imread( file_path )
    
    if image is None:
        sys.exit( "ERROR: File Not Found" )

    # - - -
    height, width, channels = image.shape
    # Total amount of pixels is 
    # the multiplication of dimensions
    total_pixels = image.size // channels

    # Message to encrypt with added delimiter tag
    # delimiter = "$t3g0"
    # message = perry + delimiter

    # Convert message to binary characters
    # format() forces the string to an 8-bit binary string
    b_msg = ''.join( [ format( ord(i), "08b" ) for i in message ] )
    # To know how many pixels we need, we look
    # to the length of the binary string
    needed_pixels = len( b_msg )

    # Check if there isn't enough space to fit the message
    if needed_pixels > total_pixels:
        sys.exit( "ERROR: Larger File Size Needed to Fit Data" )
    else:
        new_path = encode_message( b_msg, image, total_pixels, needed_pixels )
        #decode_message( new_path )


if __name__ == "__main__":
    clear_screen = lambda : os.system( "cls" if os.name == "nt" else "clear" )

    clear_screen()
    stopped = False
    allowed = set( "0123" )

    while not stopped:
        print( "\nPick a medium: \n" )
        print( "0. Exit" )
        print( "1. Image" )
        print( "2. Audio" )
        print( "3. Video" )

        answer = input( "Enter Number: " )
        if answer and allowed.issuperset( answer ):
            
            if answer == "0": stopped = True
            elif answer == "1": image_stego( clear_screen )
            else: print( "Wack ass input\n" )

    clear_screen()
    cv.destroyAllWindows()

    