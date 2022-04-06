import virtualbox
import fire


def get_machine(box: virtualbox.VirtualBox):
    """:returns: A Virtualbox Instance"""
    return box.find_machine("UBUNTU2004LTS_default_1649164272934_78585")


def lock_vm() -> virtualbox.Session:
    """
    Locks the VM to be used with the script
    :returns: A Session instance
    """
    vbox = virtualbox.VirtualBox()
    vm = get_machine(vbox)
    vs = virtualbox.Session()
    vm.lock_machine(vs, virtualbox.library.LockType.shared)
    if vm.state != virtualbox.library.MachineState.running:
        print(f"Error!! This VM is not Running, the current state is: {vm.state}.")
        quit()
    return vs


def start():
    # Make a VBox Instance
    vbox = virtualbox.VirtualBox()
    # Get the installed VM
    vm = get_machine(vbox)
    # Create a Session
    vs = virtualbox.Session()
    # Start the VM and wait for it to finish
    progress = vm.launch_vm_process(vs, "headless", [])
    progress.wait_for_completion(-1)


def screenshot():
    # Locking the VM first
    vs = lock_vm()

    # Getting the resolution
    height, width, _, _, _, _ = vs.console.display.get_screen_resolution(0)
    # Turning the VM screen into a picture
    picture = vs.console.display.take_screen_shot_to_array(0, height, width, virtualbox.library.BitmapFormat.png)
    # Saving the picture into an image
    with open('screenshot.png', 'wb') as f:
        f.write(picture)
    print('Screenshot has been saved!')


def off():
    # Locking the VM first
    vs = lock_vm()

    # Turning it off
    vs.console.power_down()


def main():
    # Using a Library from Google, turns the script into a CLI tool
    fire.Fire({
        'off': off,
        'screenshot': screenshot,
        'ss': screenshot,
        'start': start
    })


if __name__ == '__main__':
    main()
