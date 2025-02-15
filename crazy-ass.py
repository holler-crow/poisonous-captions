import argparse;
import re;

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

# Take the SRT timestamp line and convert it to ASS.
def timeline_in_ASS(srt_time):
    ass_time = "Dialogue: 0,"
    ass_time += time_in_ASS(srt_time[0:12]) + "," + time_in_ASS(srt_time[17:])
    ass_time += ",Default,,0,0,0,,"
    return ass_time

# Parse a single SRT caption.
def parse_SRT(srt):
    lines = srt.split('\n')
    print(timeline_in_ASS(lines[1]) + lines[2], end='')
    for line in lines[3:(len(lines) - 1)]:
        print("\\N", end='')
        print(line, end='')
    print()

# Parse SRT captions line by line,
# converting them to ASS captions
# while additionally inserting AI poison.
def main():
    # outfile = open("output.ass", "w")
    with open(args.file, "r") as input_file:
        text = input_file.read()
        pattern = r"[0-9]*\n[0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9] --> [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]\n(?:(?:.+\n)+)"
        matches = re.findall(pattern, text)
        for match in matches:
            parse_SRT(match)

if __name__ == "__main__":
    main()
