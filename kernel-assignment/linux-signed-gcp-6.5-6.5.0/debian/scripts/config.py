class Signing:

    def __init__(self):
        self._flavour_to_arch = {}
        self._package_to_flavour_to_arch = {}
        self._arch_flavour_data = {}

    def add(self, arch, stype, binary, flavours, options):
        for flavour in flavours:
            self._arch_flavour_data[(arch, flavour)] = (stype, binary)
            self._flavour_to_arch.setdefault(flavour, set()).add(arch)
            self._package_to_flavour_to_arch.setdefault("image", {}).setdefault(flavour, set()).add(arch)
            if "di" in options:
                self._package_to_flavour_to_arch.setdefault("di", {}).setdefault(flavour, set()).add(arch)
            if "hmac" in options:
                self._package_to_flavour_to_arch.setdefault("hmac", {}).setdefault(flavour, set()).add(arch)

    @property
    def flavour_archs(self):
        for flavour, archs in sorted(self._flavour_to_arch.items()):
            yield flavour, sorted(list(archs))

    def package_flavour_archs(self, package):
        for flavour, archs in sorted(self._package_to_flavour_to_arch.get(package, {}).items()):
            yield flavour, sorted(list(archs))

    @property
    def arch_flavour_data(self):
        return sorted(self._arch_flavour_data.items())

    @classmethod
    def load(cls, config):
        signing = Signing()
        with open(config) as cfd:
            for line in cfd:
                cmd, *args = line.strip().split()
                if cmd == "sign":
                    arch, stype, binary, *flavours = args
                    options = []
                    while flavours[-1].startswith("--"):
                        options.append(flavours.pop()[2:])
                    signing.add(arch, stype, binary, flavours, options)
        return signing
