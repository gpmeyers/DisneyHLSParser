"""
    Name: m3u8.py
    Author: Graysen Meyers
    Description: This file contains the m3u8 class which we be used as a model and provide functions necessary for parsing.
    Purpose: This file will be a module that will be imported to grant access to the other files to be able to use functions related to the m3u8 files.
"""

import regex as re

class m3u8:
    """
        The m3u8 object serves as a model to represent the .m3u8 files and to provide functions necessary for working on .m3u8 files.

        Args:
            None

        Attributes:
            filename (str): The name of the file that we are populating the model from
            independentSegments (bool): Is a flag set by an independent segments 
            sortBy (str): This is what determines what the elements will be sorted by in the sort function. (Default = 'BANDWIDTH')
            data (dict): This is where the information of the model will be stored and sorted in-place
    """

    def __init__(self, filename) -> None:
        self.filename = filename
        self.independentSegments = False
        self.sortBy = 'BANDWIDTH'

        self.data = {
            'media': [],
            'stream_inf': [],
            'iframe_stream_inf': []
        }

    def parse(self) -> None:
        """
            This function parses the information from the retrieved .m3u8 file and then populates the necessary attributes.

            Args:
                None
            
            Returns:
                None
        """
        with open(self.filename, 'r') as f:
            lines = f.readlines()

            for i in range(0, len(lines)):
                if lines[i].startswith('#EXTM3U'):  # This is the file header indicating Extended M3U and must be first line of the file. We pass
                    pass

                elif lines[i].startswith('#EXT-X-INDEPENDENT-SEGMENTS'): # Indicates that all media samples are independent and can be decoded without other segments
                    self.independentSegments = True

                elif lines[i].startswith('#EXT-X-MEDIA'): # Relates Media Playlists that contain alternative Renditions of the same content
                    info = lines[i].split(':')[1]

                    rx = re.compile(r'"[^"]*"(*SKIP)(*FAIL)|,\s*')  # Regex to split by commas not within quotes

                    parts = rx.split(info)

                    data = []
                    for item in parts:
                        key = item.split('=')[0].replace('"', '').strip()
                        val = item.split('=')[1].replace('"', '').strip()
                        data.append({key: val})
                    
                    self.data['media'].append(data)

                elif lines[i].startswith('#EXT-X-STREAM-INF'): # Specifies a Variant Stream that is a part of the Renditions
                    info = lines[i].split(':')[1]

                    rx = re.compile(r'"[^"]*"(*SKIP)(*FAIL)|,\s*')  # Regex to split by commas not within quotes

                    parts = rx.split(info)

                    data = []
                    for item in parts:
                        key = item.split('=')[0].replace('"', '').strip()
                        val = item.split('=')[1].replace('"', '').strip()
                        data.append({key: val})

                    if not lines[i + 1].startswith('#') and not lines[i + 1].startswith('\n'):
                        data.append({'URI': lines[i + 1].strip()})
                    
                    self.data['stream_inf'].append(data)

                elif lines[i].startswith('#EXT-X-I-FRAME-STREAM-INF'): # indicates that the playlist file contains I-frames of Multimedia presentation
                    info = lines[i].split(':')[1]

                    rx = re.compile(r'"[^"]*"(*SKIP)(*FAIL)|,\s*')  # Regex to split by commas not within quotes

                    parts = rx.split(info)

                    data = []
                    for item in parts:
                        key = item.split('=')[0].replace('"', '').strip()
                        val = item.split('=')[1].replace('"', '').strip()
                        data.append({key: val})
                    
                    self.data['iframe_stream_inf'].append(data)

    def sort(self, sortBy='BANDWITH') -> None:
        """
            This function sorts the elements parsed from the file depending on the input given by sortBy.

            Args:
                sortBy (str): This determines what the elements of the file will be sorted by. (Default = 'BANDWIDTH')
            
            Returns:
                None
        """

        # self.data {'media': tagType [elemList [{attr: data}]]}

        for key in self.data:
            self.sortBy = sortBy
            tagType = self.data[key]
            missing = []

            i = 0
            while i < len(tagType): # Removes files that do not contain the attribute being sorted by
                elemList = tagType[i]
                missingSortBy = True
                for dict in elemList:
                    if list(dict.keys())[0] == sortBy:
                        missingSortBy = False
                        break
                
                if missingSortBy:
                    missing.append(elemList)
                    tagType = tagType[:i] + tagType[i + 1:]
                else:
                    i += 1
            
            # Sort the remaining elements using the sorting function
            tagType.sort(key=self._sortBy)

            # Append the elements that do not contain the attribute to the end
            self.data[key] = tagType + missing

    def _sortBy(self, l):
        """
            This is the sorting helper function used in sort to sort the tag groups.

            Args:
                l (list): We are sorting lists within a list. We find the dictionary in the list with the matching attribute and .

            Returns:
                A value from the keys within the list, will either be a number or a string depending.
        """
        for elem in l:
            if list(elem.keys())[0] == self.sortBy:
                value = elem[list(elem.keys())[0]]

                try:
                    numVal = float(value)
                    return numVal
                except ValueError:
                    return value

    def dump(self, filename) -> None:
        """
            This function dumps the newly sorted elements out to a .m3u8 file output.

            Args:
                filename (str): This is the name of the file that we are going to be writing out to.

            Returns:
                None
        """
        with open(filename, 'w') as out:
            out.write('#EXTM3U\n')

            if self.independentSegments:
                out.write('#EXT-X-INDEPENDENT-SEGMENTS\n\n')

            for elem in self.data['media']:
                outLine = '#EXT-X-MEDIA:'

                for attr in elem:
                    outLine = outLine + list(attr.keys())[0] + '=' + list(attr.values())[0] + ','

                outLine = outLine[:-1] + '\n'
                out.write(outLine)

            for elem in self.data['stream_inf']:
                outLine = '#EXT-X-STREAM-INF:'

                if list(elem[-1].keys())[0] == 'URI':
                    for attr in elem[:-1]:
                        outLine = outLine + list(attr.keys())[0] + '=' + list(attr.values())[0] + ','

                    outLine = outLine[:-1] + '\n'
                    out.write(outLine)
                    out.write((list(elem[-1].values())[0] + '\n'))
                else:
                    for attr in elem:
                        outLine = outLine + list(attr.keys())[0] + '=' + list(attr.values())[0] + ','

                    outLine = outLine[:-1] + '\n'
                    out.write(outLine)

            for elem in self.data['iframe_stream_inf']:
                outLine = '#EXT-X-I-FRAME-STREAM-INF:'

                for attr in elem:
                    outLine = outLine + list(attr.keys())[0] + '=' + list(attr.values())[0] + ','

                outLine = outLine[:-1] + '\n'
                out.write(outLine)
