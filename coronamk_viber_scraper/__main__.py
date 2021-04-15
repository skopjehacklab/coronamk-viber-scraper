import argparse
import sys
import json

from . import viber

def sync_cmd(args):
    if args.infile:
        old_msgs = json.load(args.infile)
        last_seq = max(m['seq'] for m in old_msgs) + 1
    else:
        old_msgs = []
        last_seq = 0

    new_msgs = viber.get_all_messages(viber.VIBER_PUBLIC_GROUP_ID, viber.VIBER_PUBLIC_GROUP_TOKEN, last_seq)
    msgs = old_msgs + list(new_msgs)

    json.dump(msgs, args.output)


def main():
    parser = argparse.ArgumentParser(description="Скрипта за влечење податоци од Коронавирус МК Viber групата")
    subparsers = parser.add_subparsers(required=True)

    sync = subparsers.add_parser('sync')
    sync.set_defaults(func=sync_cmd)
    sync.add_argument('--infile', '-i', type=argparse.FileType('r'), default=None)
    sync.add_argument('--output', '-o', type=argparse.FileType('w'), default=sys.stdout)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
