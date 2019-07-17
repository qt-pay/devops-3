import os
from fabric import Connection


class FabricApi:
    def __init__(self, ip, user, password):
        self.conn = Connection(ip, user, connect_kwargs={'password': password})

    def update_symbolic_link(self, src, dest):
        try:
            self.conn.run("[ -e {} ]".format(src))
            self.conn.run("rm -rf {}".format(src))
        except:
            pass

        self.conn.run("ln -s {} {}".format(dest, src))

    def send_file(self, src, dest):
        try:
            self.conn.run("[ -e {} ]".format(dest))
            return True
        except:
            pass

        self.conn.run("mkdir -p {}".format(os.path.dirname(dest)))
        self.conn.put(src, "{}.tar.gz".format(dest))
        self.conn.run("tar -xf {}.tar.gz -C {}".format(dest, os.path.dirname(dest)))
        self.conn.run("rm -rf {}.tar.gz".format(dest))
