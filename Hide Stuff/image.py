'''
LSB - Least Significant Bit Steganography
# Each pixel under openCV is a collection of BGR - 8bit values
# The idea is to hide 3 bits at a time into each set of BGR
# Of course, the target is the LSB of each channel
# Bitwise manipulation is needed here, solved by set_bit()
'''

import cv2 as cv
import os
import sys

delimiter = "di3ly"

def set_bit( num, index, bit ):
    # Shift mask to specified bit
    mask = 1 << index 
    # NAND masked bit to clear it
    num &= ~mask 
    adjusted_bit = ( ( bit << index ) & mask )
    return ( num | adjusted_bit )

def save_image( name, image ):
    # cv.imwrite() is a bool function
    # Use as a flag for saving errors
    saved = cv.imwrite( name, image )

    # - - -
    if not saved:
        sys.exit( "Error While Saving Image" )
    else:
        print( "Image Saved Successfully to \"" + name + "\"\n" )
        return name

# Worst Case Time Complexity: height * width * channels
# Scroll across each pixel hiding the data
def fruit_loops( secret, needed_pixels, image ):
    index = 0
    height, width, channels = image.shape

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

def encode_message( message, carrier, save_loc ):
    # Convert message to binary characters
    # format() forces the string to an 8-bit binary string
    global delimiter
    b_msg = ''.join( [ format( ord(i), "08b" ) for i in message ] ) + delimiter
    # To know how many pixels we need, we look
    # to the length of the binary string
    needed_pixels = len( b_msg )
    # - - -
    height, width, channels = carrier.shape
    total_pixels = carrier.size // channels

    # Check if there isn't enough space to fit the message
    if needed_pixels > total_pixels:
        sys.exit( "ERROR: Larger File Size Needed to Hide Text" )
    
    # MMMMMMMMMTHISMAKESMEUNCOMFYYYYYYYYYAAAAAAAAAAAAAAAAAAA
    image = fruit_loops( b_msg, needed_pixels, carrier )
    
    # Save the new image and return the file path
    return save_image( save_loc, image )

def encode_image( img_secret, carrier, save_loc ):
    # The image to be hidden can at most be == to the carrier image dimensions
    img_secret = cv.imread( img_secret )
    hide_h, hide_w, hide_chan = img_secret.shape
    height, width, channels = carrier.shape

    # Check if there's enough space to fit the image
    if hide_h+2 > height or hide_w+2 > width:
        sys.exit( "ERROR: Larger File Size Needed to Hide Image" )

    '''
    h = ff ffff
    1111 1111 --- 1111 1111 1111 1111
    Needs: 2 pixels
    w = ff ffff
    Needs: 2 pixels
    Total: 4 pixels
    '''
    h = '{:12b}'.format( hide_h )
    w = '{:12b}'.format( hide_w )

    for i in range( 3 ):
        x = '{0:08b}'.format( carrier[0][0][i] )
        y = '{0:08b}'.format( carrier[0][1][i] )

        x = x[:4] + h[4*i:4*i+4]
        y = y[:4] + w[4*i:4*i+4]

        carrier[0][0][i] = int( x, 2 )
        carrier[0][1][i] = int( y, 2 )


    for i in range( height ):
        for j in range( width ):
            color_og = carrier[i][j]

            b1, g1, r1 = '{:08b}'.format( color_og[0] ), '{:08b}'.format( color_og[1] ), '{:08b}'.format( color_og[2] )
            b2, g2, r2 = b1, g1, r1

            if i >= hide_h and j >= hide_w: 
                break
            
            elif i < hide_h and j < hide_w:
                color_hide = img_secret[i][j]
                b2, g2, r2 = '{:08b}'.format( color_hide[0] ), '{:08b}'.format( color_hide[1] ), '{:08b}'.format( color_hide[2] )

            str_bin = b1[:4] + b2[:4], g1[:4] + g2[:4], r1[:4] + r2[:4]
            for k in range( channels ):
                carrier[i][j][k] = int( str_bin[k], 2 )
        else: 
            continue
        break
            
    # Save the new image and return the file path
    return save_image( save_loc, carrier )

def decode_image( path ):
    pass


def decode_message( path ):
    global delimiter 

    # Open the desired image
    decode = cv.imread( path )
    # Retreive dimensions of the desired image
    height, width, channels = decode.shape
    total_pixels = height * width

    # Hold the raw encrypted data
    hidden_bits = ""

    # 
    def fruit_loops2( hidden_bits, height, width, decode ):
        for y in range( height ):
            for x in range( width ):
                # Bush through the BGR of a pixel
                for i in range( channels ):
                    hidden_bits += ( bin( decode.item( y, x, i ) )[2:][-1] )
        # "hidden_bits" is just 1 string of everything
        return hidden_bits
    
    # ISTILLDONTLIKETHISAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    hidden_bits = fruit_loops2( hidden_bits, height, width, decode )

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
    if delimiter in message:
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