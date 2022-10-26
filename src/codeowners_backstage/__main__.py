
import argparse
from pathlib import Path

import requests
from codeowners_backstage.backstage_user_groups import BackstageUserGroups
from codeowners_backstage.codeowners_file import preprocess_codeowners_inlining_group_members


parser = argparse.ArgumentParser(description="Preprocesses CODEOWNERS file, substituting group names with member "
                                             "emails using information taken from a Backstage catalog."
                                             "Group names are expected to start with the \"@\" symbol.")
parser.add_argument('file', type=Path, help='Input file')
parser.add_argument('-H', '--host', required=True, type=str, help='URL to the Backstage host')
parser.add_argument('--disable-ssl-verification', action='store_const', const=True, default=False)
parser.add_argument('-n', '--namespace', default='default', type=str,
                    help='Namespace in Backstage (default: %(default)r)')
parser.add_argument('-o', '--out', type=Path, help='Output file (default: stdout)')


def substitute(read_input, write_output, get_group_members):
    input_str = read_input()
    output_str = preprocess_codeowners_inlining_group_members(input_str, get_group_members)
    write_output(output_str)


if __name__ == "__main__":
    args = parser.parse_args()
    session = requests.Session()
    session.verify = args.disable_ssl_verification
    user_groups = BackstageUserGroups.load(args.host, args.namespace, session)
    substitute(read_input=args.file.read_text,
               write_output=args.out.write_text if args.out is not None else print,
               get_group_members=user_groups.get_group_members)
