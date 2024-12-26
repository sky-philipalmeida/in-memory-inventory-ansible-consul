from ansible.plugins.action import ActionBase
from ansible.plugins.loader import action_loader
from ansible.playbook.task import Task
import consul

class ActionModule(ActionBase):

  def getInventoryByNodeMeta(self, vars):
    node_meta = vars['node_meta']
    host = f"{vars['consul']['url']}"
    c = consul.Consul(host=host, port=443, scheme='https')
    dcs = c.catalog.datacenters()
    final_nodes = {}
    for dc in dcs:
      nodes = c.catalog.nodes(node_meta=node_meta,dc=dc)
      for node in nodes[1]:
        final_nodes[node["Address"]] = node
    return final_nodes

  def run(self, tmp=None, task_vars=None):
    if task_vars is None:
        task_vars = dict()

    inventory = self.getInventoryByNodeMeta(self._task.args)

    hosts = []

    for vip in inventory.keys():
      add_hosts_args = dict()
      add_hosts_args["name"] = vip
      add_hosts_args["groups"] = self._task.args["groups"]
      add_hosts_args["node_meta"] = inventory[vip]["Meta"]

      new_task = Task()
      new_task.args = add_hosts_args

      add_host = action_loader.get("ansible.builtin.add_host",
                task=new_task,
                connection=self._connection,
                play_context=self._play_context,
                loader=self._loader,
                templar=self._templar,
                shared_loader_obj=self._shared_loader_obj).run()

      hosts.append(add_host)

    self._task.loop = True

    return { 'results': hosts }
