import subprocess
from os import system, path, name
import signal
import sys
args = sys.argv[1:]
args = ' '.join(args)

def clear_termenal():
	if name.startswith("nt"):
		system("cls")
	else:
		system("clear")

def handler(signum, frame):
        system(f"pkill -f {path.basename(__file__)}")
signal.signal(signal.SIGINT, handler)

history = []

while True:
    if not args:
        search_query_org = input("Search Query: ")
    else:
        search_query_org = args
        args = None
    search_query = search_query_org.strip("ao")
    clear_termenal()
    if search_query == "history":
        out = subprocess.check_output(['ytfzf', '-I', 'R', '-q'])
    elif not search_query:
        if not history:
            continue
        out = subprocess.check_output(['ytfzf', '-I', 'R', history[len(history)-1]])
    else: 
        out = subprocess.check_output(['ytfzf','-I', 'R', search_query])
        history.append(search_query)

    out = out.decode('utf-8')
    title = out.split('|')[0]
    link = "http"+out.split("http")[1].strip()
    print("\nPlaying:", title, "\n", "link:", link)

    if search_query_org.startswith("ao"):
        system("mpv --no-video --loop -fs --screen=1 --ytdl-raw-options='sub-lang=\"en\",write-sub=,write-auto-sub=' "+ link)
    else:

        system("mpv --loop -fs --screen=1 --ytdl-raw-options='sub-lang=\"en\",write-sub=,write-auto-sub=' "+ link)
