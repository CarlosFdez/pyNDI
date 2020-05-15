import typing
import re

from lib import lib, ffi

def create_ndi_finder():
    pNDI_find = lib.NDIlib_find_create_v2(ffi.NULL)
    if not pNDI_find:
        print("Failed to create find API instance")

    return NDIFinder(lib, pNDI_find)

class NDISource():
    def __init__(self, raw, name: str, address: str):
        self.raw = raw
        self.name = name
        self.address = address

    @property
    def simple_name(self):
        """Returns the user submitted source name.
        Parsed from inside the parenthesis of the source name"""
        return self._parse_name()[1]

    @property
    def device_name(self):
        """Returns the device name.
        Parsed from the first string in the source name"""
        return self._parse_name()[0]

    def _parse_name(self):
        """Internal helper to return a (Device Name, Simple Name) tuple.
        """
        match = re.match(r"(.+) \((.+)\)", self.name)
        if match:
            return (match.group(1), match.group(2))
        else:
            return (self.name, self.name)

class NDIFinder():
    def __init__(self, lib, pNDI_find):
        self.pNDI_find = pNDI_find

        self.current_sources = []

    def __del__(self):
        lib.NDIlib_find_destroy(self.pNDI_find)

    def get_sources(self, wait_ms=5000) -> typing.Iterable[NDISource]:
        "Returns all sources that can be accessed on the current network"
        changed = lib.NDIlib_find_wait_for_sources(self.pNDI_find, wait_ms)
        if not changed:
            return self.current_sources

        # Changed, get new sources
        # num_sources = c_int()

        p_nsources = ffi.new("uint32_t *")
        sources = lib.NDIlib_find_get_current_sources(self.pNDI_find, p_nsources)

        num_sources = p_nsources[0]
        #print(len(num_sources))
        # Update sources (create a new list so that the caller's == checks work)
        self.current_sources = []
        for i in range(num_sources):
            source = sources[i]
            self.current_sources.append(NDISource(
                raw=source,
                name=ffi.string(source.p_ndi_name).decode('utf-8'),
                address=ffi.string(source.p_url_address).decode('utf-8')
            ))


        return self.current_sources
