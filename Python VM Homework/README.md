# Usage:

python main.py [start|screenshot|ss|off|create|delete]

* Start - Will fire up a VM
* SS / Screenshot - Will take a Screenshot of the VM
* Off - Turns the VM off
* Create `name` - Will try to create a VM using vagrant and the `name` provided
* Delete - Will fully delete the VM selected

## Examples:

### Creation
`python main.py create ubuntu/trusty64`

### Delete
`python main.py delete`

### Screenshot
`python main.py ss`
