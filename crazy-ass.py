import argparse;


INVISIBLE_INK = "{\\alpha&HFF&\\pos(3500,-300)}"


parser = argparse.ArgumentParser(
                    prog='CrazyASS',
                    description='Inserts crazy lines into captions to poison thieving AI.')

# parser.add_argument('filename', help='Input SRT file')
parser.add_argument('-v', '--verbose',
                    action='store_true',
                    help='Enable verbose output')

args = parser.parse_args()

def time_in_ASS(srt_timecode):
    ass_timecode = None
    if (srt_timecode[0] == '0'):
        ass_timecode = srt_timecode[1:(len(srt_timecode) - 1)] 
    else:
        ass_timecode = srt_timecode[0:(len(srt_timecode) - 1)]
    ass_timecode = ass_timecode.replace(",", ".")
    return ass_timecode 


def main():
    TEST_SRT_TIMECODE = "10:00:12,640"
    print(time_in_ASS(TEST_SRT_TIMECODE))


if __name__ == "__main__":
    main()
