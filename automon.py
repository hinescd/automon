import subprocess
import time

def xrandr():
    '''
    Capture output of 'xrandr -q' as an array of lines
    '''
    return subprocess.run(['xrandr', '-q'], capture_output=True).stdout.decode('utf-8').split('\n')[1:-1]

def get_monitors():
    '''
    Return a sorted list of currently connected monitors. For laptop lids, inclusion in the list is
    determined by the state of the laptop lid.
    '''
    lines = xrandr()
    conn = list(filter(lambda line: " connected " in line, lines))
    mons = [ mon.split()[0] for mon in conn ]
    lid_state = open('/proc/acpi/button/lid/LID/state', 'r').readlines()[0].split()[1]
    if lid_state == 'closed':
        mons.remove('eDP-1')
    return sorted(mons)

def get_all_monitors():
    '''
    Return a list of all monitors reported by xrandr, regardless of whether they're connected
    '''
    return [ mon.split()[0] for mon in list(filter(lambda line: not line.startswith(' '), xrandr())) ]

def main():
    '''
    Repeatedly polls for a list of connected monitors, using xrandr to set connected monitors to
    auto and disconnected monitors to off
    '''
    old_monitors = []
    while True:
        time.sleep(1)
        monitors = get_monitors()
        if monitors != old_monitors:
            # At least one monitor was either connected or disconnected

            # Get the monitors that have been disconnected, if any
            disconnecteds = list(filter(lambda mon: mon not in monitors, get_all_monitors()))

            # Building the command to configure monitors
            args = ['xrandr']
            for disconnected in disconnecteds:
                # Turn off disconnected monitors
                args.extend(['--output', disconnected, '--off'])
            if len(monitors) > 0:
                # Set the first monitor as primary
                args.extend(['--output', monitors[0], '--auto', '--primary'])
                for monitor in monitors[1:]:
                    # Auto-config all the monitors
                    args.extend(['--output', monitor, '--auto'])
            command = ' '.join(args)
            subprocess.run(args)
            old_monitors = monitors

if __name__ == '__main__':
    main()
