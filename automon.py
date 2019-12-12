import subprocess
import os
import time
import yaml

def xrandr():
    '''
    Capture output of 'xrandr -q' as an array of lines
    '''
    return subprocess.run(['xrandr', '-q'], capture_output=True).stdout.decode('utf-8').split('\n')[1:-1]

def get_monitors():
    '''
    Return a set of currently connected monitors. For laptop lids, inclusion in the set is
    determined by the state of the laptop lid.
    '''
    lines = xrandr()
    conn = set(filter(lambda line: " connected " in line, lines))
    mons = { mon.split()[0] for mon in conn }
    if 'lid' in config and 'laptop-screen' in config:
        lid_state = open(config['lid'], 'r').readlines()[0].split()[1]
        if lid_state == 'closed':
            mons.remove(config['laptop-screen'])
    return mons

def get_all_monitors():
    '''
    Return a set of all monitors reported by xrandr, regardless of whether they're connected
    '''
    return { mon.split()[0] for mon in list(filter(lambda line: not line.startswith(' '), xrandr())) }

def main():
    '''
    Repeatedly polls for a list of connected monitors, using xrandr to set connected monitors to
    auto and disconnected monitors to off
    '''
    global config

    # Load configuration from ~/.automon.yaml, if present
    try:
        with open(os.path.expanduser('~/.automon.yaml')) as f:
            config = yaml.load(f, Loader=yaml.Loader)
        if 'profiles' not in config:
            config['profiles'] = []
    except:
        config = {'profiles': []}
    old_monitors = set()
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
                profiles = [p for p in config['profiles'] if monitors == set(map(lambda m: m['output'], p))]

                if len(profiles) > 0:
                    # Select the first profile that matched
                    profile = profiles[0]
                    has_primary = False
                    for monitor_config in profile:
                        for prop in monitor_config:
                            if prop == 'mode' and monitor_config[prop] == 'auto':
                                args.append('--auto')
                            else:
                                args.extend(['--' + prop, monitor_config[prop]])
                        if not has_primary:
                            args.append('--primary')
                            has_primary = True
                else:
                    # Default configuration
                    # Set the first monitor as primary
                    has_primary = False
                    for monitor in monitors:
                        # Auto-config all the monitors
                        args.extend(['--output', monitor, '--auto'])
                        if not has_primary:
                            args.append('--primary')
                            has_primary = True
            command = ' '.join(args)
            subprocess.run(args)
            old_monitors = monitors

if __name__ == '__main__':
    main()
