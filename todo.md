lri = lr.Instance(name='API Service')
lri.Log.info('Hello, World!')
# Doesn't have the LogManager, uses the name instead.
# >>> [10:05:31] <API Service> [i] Hello, World!
# Has access to all other methods, just like the normal `lr` instance.

lr.Instance.set_state(instance_name='API Service', state='disabled')
lr.Instance.set_state(instance_name=<Object>, state='disabled')
# Disable all logging from the specified instance.

lr.Instance.get_instances()
# Get a list of instance objects.
# >>> [<Instance:API Service>, ...]
