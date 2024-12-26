#!/bin/bash
export ANSIBLE_ACTION_PLUGINS=./action_plugins
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
export ANSIBLE_HOST_KEY_CHECKING=False
ansible-playbook ./in-memory.yaml
