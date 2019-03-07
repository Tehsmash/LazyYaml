import argparse
import json
import ruamel.yaml
import sys

import lazyyaml

yaml = ruamel.yaml.YAML()
yaml.indent(sequence=4, offset=2)

parser = argparse.ArgumentParser()
parser.add_argument("yaml_doc", help="A YAML doc with templates to render")


def main():
    args = parser.parse_args()
    with open(args.yaml_doc, 'r') as f:
        doc = lazyyaml.load(f)
    yaml.dump(doc.to_native(), sys.stdout)
