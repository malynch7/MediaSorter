import datetime
import os
import re

from imdb import IMDb

# Default Parameters
INPUT_DIRECTORY = "Input\\"
OUTPUT_DIRECTORY = "Output\\"
TV_REGEX = "(.*)s(\d{1,2})(e\d{1,2})"
MOVIE_REGEX = "(.*?)(1080p|720p|x264|aac|ac3|dvd|xvid|cd\d|\.\w\w\w$)+"


def main():
    input_files = get_input_files()
    for i in range(len(input_files)):
        if not file_is_accepted_format(input_files[i]):
            input_files[i].destination = "unsorted"
            input_files[i].error_string = "Unsupported File Format"
        regex_results = re.match(TV_REGEX, input_files[i].filename.lower())
        if regex_results:
            input_files[i] = get_sorted_tv_destination(input_files[i], regex_results)
        else:
            regex_results = re.match(MOVIE_REGEX, input_files[i].filename.lower())
            if regex_results:
                input_files[i] = get_sorted_movie_destination(input_files[i], regex_results)
            else:
                input_files[i].destination = "unsorted"
                input_files[i].error_string = "Failed Regex Match"

    move_files_to_destinations(input_files)


class MediaFile:
    def __init__(self, full_path, filename):
        self.full_path = full_path
        self.filename = filename
        self.destination = ""
        self.error_string = ""


def get_sorted_tv_destination(file, regex_results):
    ia = IMDb()
    imdb_results = ia.search_movie(regex_results.group(1))
    if imdb_results:
        file.destination = "TV Shows\\" + imdb_results[0]['title'] + "\\Season " + regex_results.group(2)
    else:
        file.destination = "unsorted"
        file.error_string = "No title returned (TV Show)."
    return file


def get_sorted_movie_destination(file, regex_results):
    ia = IMDb()
    imdb_results = ia.search_movie(regex_results.group(1))
    if imdb_results:
        file.destination = "Movies\\" + imdb_results[0]['title']
    else:
        file.destination = "unsorted"
        file.error_string = "No title returned (Movie)."
    return file


def move_files_to_destinations(input_files):
    index = 0
    with open(OUTPUT_DIRECTORY + "\\SorterLog.txt", "a") as log:
        log.write("\n\n" + str(datetime.datetime.now()) + "\n")
        for file in input_files:
            # Log Results
            error = "         "
            if file.error_string != "":
                error = "ERROR: " + file.error_string + "    "
                log.write(error + file.full_path + "    -->    " + file.destination + "\n")
            else:
                log.write(error + file.full_path + "    -->    " + OUTPUT_DIRECTORY + file.destination + "\\"
                          + file.filename + "\n")
            # print(file[0] + "    -->    " + outputDirectory + destinations[index] + "\\" + file[1] + error)

            # Move
            # if destinations[index] != "Unsorted":
            #     shutil.move(file[0], outputDirectory + destinations[index] + "\\" + file[1])
            index = index + 1


def get_input_files():
    input_files = []
    for r, d, f in os.walk(INPUT_DIRECTORY):
        for file in f:
            input_files.append(MediaFile(os.path.join(r, file), file))
    return input_files


def file_is_accepted_format(input_file):
    accepted_formats = [".mp4", ".srt", ".mkv", ".avi", ".flv", ".wmv", ".mov"]
    return input_file.filename.lower().endswith(tuple(accepted_formats))


if __name__ == '__main__':
    main()
