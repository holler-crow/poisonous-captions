import argparse;


INVISIBLE_INK = "{\\alpha&HFF&\\pos(3500,-300)}"


parser = argparse.ArgumentParser(
                    prog='CrazyASS',
                    description='Inserts crazy lines into captions to poison thieving AI.')

parser.add_argument('file', help='Input SRT file')
parser.add_argument('-v', '--verbose',
                    action='store_true',
                    help='Enable verbose output')

args = parser.parse_args()

# Take the single bit of time in SRT and convert it to ASS.
def time_in_ASS(srt_timecode):
    ass_timecode = None
    if (srt_timecode[0] == '0'):
        ass_timecode = srt_timecode[1:(len(srt_timecode) - 1)] 
    else:
        ass_timecode = srt_timecode[0:(len(srt_timecode) - 1)]
    ass_timecode = ass_timecode.replace(",", ".")
    return ass_timecode 

# Take the SRT timestamp line and convert it to ASS
def timeline_in_ASS(srt_time):
    ass_time = "Dialogue: 0,"
    ass_time += time_in_ASS(srt_time[0:12]) + "," + time_in_ASS(srt_time[17:])
    ass_time += ",Default,,0,0,0,,"
    return ass_time

# Parse SRT dialogue
def dialogue_in_ass(in_file):
    line = in_file.readline()
    print_newline = false;
    while (line & line != "\n"):
        print(line)
        if print_newline:
            print("\\N")

# Parse SRT captions line by line,
# converting them to ASS captions
# while additionally inserting AI poison.
def main():
    # outfile = open("output.ass", "w")
    with open(args.file, "r") as input_file:
        curr_line = input_file.readline()
        while curr_line:
            # if (curr_line.isdigit()):
            print(len(curr_line.replace('\n', '').strip()))
            print(len("1"))
            # print(timeline_in_ASS(input_file.readline()))
            break;
                # print(dialogue_in_ASS(input_file) + "\n")
            # curr_line = input_file.readline()

if __name__ == "__main__":
    main()
