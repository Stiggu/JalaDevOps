import virtualbox
import fire
from pick import pick
import os
import subprocess


def get_machine(box: virtualbox.VirtualBox) -> virtualbox.library.IMachine:
    """:returns: A Virtualbox Instance"""
    option, i = pick([f"{m.name} | {m.state}" for m in box.machines], "Please select the VM.")
    return box.find_machine(option.split(' ')[0])


def delete():
    # Make a VBox Instance
    vbox = virtualbox.VirtualBox()
    # Get the installed VM
    vm = get_machine(vbox)
    # Let the user know the machine has been deleted and run the command for that
    print(f'Virtual machine: {vm.name} has been deleted!')
    # Thanks to Carla for the command! Was using unregister before
    vm.remove()


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


def create(vm_name: str):
    # Removing special Characters from the folder name
    folder_vm_name = ''.join(e for e in vm_name if e.isalnum())
    # Creating the folder and setting up the vagrant files
    os.system(f'mkdir {folder_vm_name} & cd {folder_vm_name} & vagrant init {vm_name}')
    # Trying to get the VM up, using subprocess module to read the output of the console
    process = subprocess.Popen('vagrant up',
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               cwd=f'./{folder_vm_name}')
    stdout, stderr = process.communicate()
    # In case the box isn't found in vagrant
    if "could not be found." in stdout.decode('utf-8'):
        os.system(f'rmdir /s /q {folder_vm_name}')
        print('This box doesn\'t exist, files have been deleted.')
        return

    print('VM has been create thru vagrant!')


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
    print(f'VM {vm.name} is up and running!')


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

    print('VM has been turned off!')


def main():
    # Using a Library from Google, turns the script into a CLI tool
    fire.Fire({
        'off': off,
        'screenshot': screenshot,
        'ss': screenshot,
        'start': start,
        'create': create,
        'delete': delete,
    })


if __name__ == '__main__':
    main()
