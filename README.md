# DisneyHLSParser
This is an HLS parser that I am writing for my take home coding assessment for Disney Streaming. Build details will be provided.

This is written in Python3 and so Python 3 is required to run it. (Pip as well)

Need the requests package. Run 'pip3 install requests' on the command line to get it.
Need the regex package. Run 'pip3 install regex' on the command line to get it.
Need the argparse package. I believe that this is default with Python3 but you may need to get it via pip.

# Command-Line Interface (CLI)
I am not sure if these are dependencies but the os and argparse packages have been imported for the purpose of making a CLI so that it will be easier for you the user
to interact with the program.

This CLI has two required positional arguments:
    1. url (str): The url that we will be downloading the .m3u8 file from
    2. sortBy (str): The attribute that we will be sorting the tags by. Must be in all caps and follow the form of the tags. Ex: BANDWIDTH

It also has one optional argument:
    1. --outFile (str): The name that will be given to the output file from the program. If none is specified, the default value will be 'sorted.m3u8'

Example run: python3 parser.py https://... BANDWIDTH --outFile out.m3u8