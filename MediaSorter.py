import datetime
import os
import re

from imdb import IMDb

# Default Parameters
inputDirectory = "Input\\"
outputDirectory = "Output\\"
acceptedFormats = [".mp4", ".srt", ".mkv", ".avi", ".flv", ".wmv", ".mov"]


# Get list of files and paths
inputFiles = []  # [full path, filename]
for r, d, f in os.walk(inputDirectory):
    for file in f:
        inputFiles.append([os.path.join(r, file), file])

# IMDB search and get destination directory
ia = IMDb()
destinations = []
errors = []
for file in inputFiles:
    if file[1].lower().endswith(tuple(acceptedFormats)):

        # TV Shows
        regexResults = re.match("(.*)s(\d{1,2})(e\d{1,2})", file[1].lower())
        if regexResults:
            imdbResults = ia.search_movie(regexResults.group(1))
            if imdbResults:
                destinations.append("TV Shows\\" + imdbResults[0]['title'] + "\\Season " + regexResults.group(2))
                errors.append("")
            else:
                destinations.append("Unsorted")
                errors.append("No title returned (TV Show).")

        # Movies
        else:
            regexResults = re.match("(.*?)(1080p|720p|x264|aac|ac3|dvd|xvid|cd\d|\.\w\w\w$)+", file[1].lower())
            if regexResults:
                imdbResults = ia.search_movie(regexResults.group(1))
                if imdbResults:
                    destinations.append("Movies\\" + imdbResults[0]['title'])
                    errors.append("")
                else:
                    destinations.append("Unsorted")
                    errors.append("No title returned (Movie).")
            else:
                destinations.append("Unsorted")
                errors.append("Failed Regex")

    else:
        destinations.append("Unsorted")
        errors.append("Unsupported File Format")

# Move Files
index = 0
with open(outputDirectory + "\\SorterLog.txt", "a") as log:
    log.write("\n\n" + str(datetime.datetime.now()) + "\n")
    for file in inputFiles:
        # Log Results
        error = "         "
        if errors[index] != "":
            error = "ERROR: " + errors[index] + "    "
            log.write(error + file[0] + "    -->    " + destinations[index] + "\n")
        else:
            log.write(error + file[0] + "    -->    " + outputDirectory + destinations[index] + "\\" + file[1] + "\n")
        # print(file[0] + "    -->    " + outputDirectory + destinations[index] + "\\" + file[1] + error)

        # Move
        # if destinations[index] != "Unsorted":
        #     shutil.move(file[0], outputDirectory + destinations[index] + "\\" + file[1])
        index = index + 1
