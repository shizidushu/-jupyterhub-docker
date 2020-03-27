# JupyterHub configuration
#
## If you update this file, do not forget to delete the `jupyterhub_data` volume before restarting the jupyterhub service:
##
##     docker volume rm jupyterhub_jupyterhub_data
##
## or, if you changed the COMPOSE_PROJECT_NAME to <name>:
##
##    docker volume rm <name>_jupyterhub_data
##

import os

from dockerspawner import SwarmSpawner
from docker.types import Mount



c = get_config()

## Generic
c.JupyterHub.admin_access = True
c.Spawner.default_url = '/lab'

## Authenticator
c.JupyterHub.authenticator_class = 'nativeauthenticator.NativeAuthenticator'
c.Authenticator.admin_users = {'jovyan'}


class SwarmSpawner2(SwarmSpawner):
    @property
    def mounts(self):
        if len(self.volume_binds):
            driver = self.mount_driver_config
            return [
                Mount(
                    target=vol["bind"],
                    source=host_loc,
                    type="bind",
                    read_only=vol["mode"] == "ro",
                    # driver_config=driver,
                    driver_config=None,
                )
                for host_loc, vol in self.volume_binds.items()
            ]

        else:
            return []

## Docker spawner
c.JupyterHub.spawner_class = SwarmSpawner2
c.SwarmSpawner2.image = os.environ['DOCKER_JUPYTER_CONTAINER']

# JupyterHub requires a single-user instance of the Notebook server, so we
# default to using the `start-singleuser.sh` script included in the
# jupyter/docker-stacks *-notebook images as the Docker run command when
# spawning containers.  Optionally, you can override the Docker run command
# using the DOCKER_SPAWN_CMD environment variable.
# spawn_cmd = os.environ.get('DOCKER_SPAWN_CMD', "start-singleuser.sh")
# c.DockerSpawner.extra_create_kwargs.update({ 'command': spawn_cmd })

# Connect containers to this Docker network
network_name = os.environ['DOCKER_NETWORK_NAME']
c.SwarmSpawner2.network_name = network_name
# Pass the network name as argument to spawned containers
c.SwarmSpawner2.extra_host_config = {'network_mode': network_name}


# See https://github.com/jupyterhub/dockerspawner/blob/master/examples/oauth/jupyterhub_config.py
c.JupyterHub.hub_ip = '0.0.0.0'  # listen on all interfaces os.environ['HUB_IP']
c.JupyterHub.hub_port = 8080
c.JupyterHub.hub_connect_ip = '0.0.0.0' # os.environ['HUB_CONNECT_IP']
c.NotebookApp.ip = '0.0.0.0'


# user data persistence
# see https://github.com/jupyterhub/dockerspawner#data-persistence-and-dockerspawner
# Explicitly set notebook directory because we'll be mounting a host volume to
# it.  Most jupyter/docker-stacks *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'
c.SwarmSpawner2.notebook_dir = notebook_dir
# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.SwarmSpawner2.volumes = { '/home/bi/simon/jupyterhub-docker/jupyterhub_data/notebook/{username}': notebook_dir }
# volume_driver is no longer a keyword argument to create_container()
# c.DockerSpawner.extra_create_kwargs.update({ 'volume_driver': 'local' })
# Remove containers once they are stopped
# c.SwarmSpawner2.remove_containers = True
# For debugging arguments passed to spawned containers
c.SwarmSpawner2.debug = True

# Other stuff
c.Spawner.cpu_limit = 4
c.Spawner.mem_limit = '10G'


## Services
c.JupyterHub.services = [
    {
        'name': 'cull_idle',
        'admin': True,
        'command': 'python3 /srv/jupyterhub/cull_idle_servers.py --timeout=36000'.split(),
    },
]
