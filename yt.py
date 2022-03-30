import subprocess
from os import system, path
import signal
import sys
args = sys.argv[1:]
args = ' '.join(args)

def handler(signum, frame):
        system(f"pkill -f {path.basename(__file__)}")
signal.signal(signal.SIGINT, handler)

history = []

while True:
    if not args:
        search_query = input("Search Query: ")
    else:
        search_query = args
    if search_query == "history":
        out = subprocess.check_output(['ytfzf', '-t', '-I', 'R', '-q'])
    elif not search_query:
        if not history:
            continue
        out = subprocess.check_output(['ytfzf', '-t', '-I', 'R', history[len(history)-1]])
    else: 
        out = subprocess.check_output(['ytfzf', '-t', '-I', 'R', search_query])
        history.append(search_query)

    out = out.decode('utf-8')
    title = out.split('|')[0]
    link = "http"+out.split("http")[1].strip()
    print("\nPlaying:", title, "\n", "link:", link)

    system("mpv --loop -fs --screen=1 --ytdl-raw-options='sub-lang=\"en\",write-sub=,write-auto-sub=' "+ link)

