"""
    Title: parser.py
    Author: Graysen Meyers
    Description: This is the main file for the HLS or m3u8 file parser that I will be writing for the Disney Streaming Assessment. This file will
    take in a url to a .m3u8 file and will sort it by a given attribute (at minimum Bandwidth and Codecs).
    Purpose: The purpose of this program is to pass the Disney Streaming Assessment but technically to return a sorted version of the give .m3u8 file.
"""
# Import the requests module to handle getting the file from a url
import string
import requests

# Import the module for creating and working on a model for the m3u8 files
from m3u8 import m3u8

#Import modules necessary for creating a command-line interface (CLI)
import os
import argparse

def download(url) -> None:
    """
        This function downloads a m3u8 file from the given url and creates a m3u8 file within the current directory. 

        Args:
            url (str): This is a url link to where the m3u8 file is located.
        
        Returns:
            None
    """
    r = requests.get(url, stream = True)
    
    with open('presorted.m3u8','wb') as file:
        for chunk in r.iter_content(chunk_size=1024):
    
            # writing one chunk at a time to local m3u8 file
            if chunk:
                file.write(chunk)

def main():
    argparser = argparse.ArgumentParser()

    # Required argument: The url where we will fetch the file
    argparser.add_argument('url', help='The url that we will be downloading the file from', type=str)

    # Required argument: What we will be sorting our input by
    argparser.add_argument('sortBy', help='The attribute that we will be sorting the tags by. Must be in all caps and follow the form of the tags. Ex: BANDWIDTH',
                            type=str)
    
    # Optional argument: The filename that we would like to set for our output
    argparser.add_argument('--outFile', help='Use to specify the name of the output file. The default value will be sorted.m3u8', type=str, default='sorted.m3u8')

    args = argparser.parse_args()

    url = args.url
    sortBy = args.sortBy
    outFile = args.outFile

    download(url)

    m = m3u8('presorted.m3u8')
    m.parse()
    m.sort(sortBy)
    m.dump(outFile)

# main function
if __name__ == '__main__':
    main()