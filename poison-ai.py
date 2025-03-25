import argparse;
import re;
import random;
import math;

# Tag to make captions invisible.
INVISIBLE_INK = "{\\alpha&HFF&}"


parser = argparse.ArgumentParser(
                    prog='Poisonous Captions',
                    description='Inserts garbage into captions to poison thieving AI.')

parser.add_argument('file', help='Input SRT file')
parser.add_argument('poison', help='Input poison plaintext file')
parser.add_argument('-o', '--output', help='Output filename')

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

# Write a single ASS caption.
def write_dialogue(lines, timeline, out): 
    out.write(f'{timeline}{lines[0]}')
    # Output captions
    for line in lines[1:(len(lines) - 1)]:
        out.write(f'\\N{line}')
    out.write('\n')

# Parse a SRT caption into an ASS caption.
def parse_SRT(srt, out):
    lines = srt.split('\n')
    timeline = timeline_in_ASS(lines[1])
    write_dialogue(lines[2:], timeline, out)
    return timeline

# Parse SRT captions line by line,
# converting them to ASS captions
# while additionally inserting AI poison.
def main():
    out_filename = args.output if args.output else "output.ass"
    outfile = open(out_filename, "w")
    try:
        poison_file = open(args.poison, "r")
    except FileNotFoundError:
        print(f'{args.poison} does not exist.')
        quit(-1)
    poison = poison_file.readlines()
    num_poison = len(poison)
    
    try:
        input_file = open(args.file, "r")
        with open(args.file, "r") as input_file:
            text = input_file.read()
            pattern = r"[0-9]*\n[0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9] --> [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]\n(?:(?:.+\n)+)"
            matches = re.findall(pattern, text)
            num_captions = len(matches)
            # Choose randomly when to start poisoning.
            n = random.randint(1, math.floor(num_captions / 2))
            i = 1 # index
            block = 1
            
            # Evenly spread poison throughout file
            # based on random position n.
            if (num_captions - n) < num_poison:
                block = math.ceil(num_poison / (num_captions - n))
            for match in matches:
                timeline = parse_SRT(match, outfile)
                # Insert poison if within random range
                idx = (i - n) * block
                if n <= i and idx < num_poison: 
                    poison[idx] = INVISIBLE_INK + poison[idx]
                    write_dialogue(poison[idx:min(idx + block + 1, num_poison)], timeline, outfile)
                i += 1
    except FileNotFoundError:
        print(f'{args.file} does not exist.')
        quit(-2)
    input_file.close()
    outfile.close()
    poison_file.close()
            


if __name__ == "__main__":
    main()
