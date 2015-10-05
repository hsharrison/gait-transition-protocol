"""Gait transition test protocol.

Usage:
  trial.py <speeds> <plateau-time> [<device>]
  trial.py --help

<speeds> specifies the speeds (in mph) in the format first:change:last
<plateau-time> is the time (in seconds) between speed changes
<device> (optional) is the path to the serial device connected to the treadmill.
  The default is /dev/ttyUSB0 which usually works.
  If not, try incrementing the integer, e.g. /dev/ttyUSB1.

Example:
  python trial.py 1:0.5:8 10

This would start at 1 mph, increase speed every 10 s in increments of 0.5 mph, and stop at 8 mph.
To do the reverse you would run:
  python trial.py 8:-0.5:1 10

"""
from time import sleep
import numpy as np
from docopt import docopt
from trackmaster import Treadmill


def run_trial(treadmill, speeds, plateau_time):
    treadmill.speed = speeds[0]
    print('Set speed to {:.1f}.'.format(speeds[0]))
    print('Instruct participant to start walking.')
    input('Press ENTER to continue.')

    try:
        for speed in speeds:
            treadmill.speed = speed
            print('Set speed to {:.1f}.'.format(speed))
            sleep(plateau_time)

    finally:
        print('Stopping treadmill...')
        treadmill.auto_stop()


def main(args=None):
    args = docopt(__doc__, argv=args)

    treadmill = Treadmill(args.get('<device>', '/dev/ttyUSB0'))

    first, change, last = (float(x) for x in args['<speeds>'].split(':'))
    speeds = np.arange(first, last + change, change)

    plateau_time = args['<plateau-time>']

    run_trial(treadmill, speeds, float(plateau_time))


if __name__ == '__main__':
  main()
