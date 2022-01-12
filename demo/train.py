import os
import sys
from argparse import ArgumentParser

from runner.base_runner import *
from runner.base_runner import *
from util.utils import *
from util.config import *

o_path = os.getcwd()
sys.path.append(o_path)


def parse_args():
    '''parse args'''
    parser = ArgumentParser(description='Training scripts')
    parser.add_argument('--config', help='train config file path')
    parser.add_argument(
        '--dump-config',
        type=bool,
        default=False,
        help='dump complete configuration to complete_config.py',
    )
    return parser.parse_known_args()


def main():
    '''main functions'''
    args, unknown = parse_args()

    cfg = Config.fromfile(args.config)
    cfg.update(Config.from_list(unknown))
    print(cfg)
    if args.dump_config:
        cfg.dump("./complete_config.py")

    runner = BaseRunner(cfg)
    if not cfg.get('inference', None):
        runner.run()
    return runner


if __name__ == '__main__':
    main()
