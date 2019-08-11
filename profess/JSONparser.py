from collections.abc import Iterable
import re

class JsonParser:
    # @search returns a list with results
    # @searchIn is the dict/list we search in
    # @searchFor is the String we search for
    # @returnsAll if true, returns all where searchFor fits, even if searchID doesn't fit
    def __init__(self):
        self.topology = ""

    def search(self, search_in, search_for, search_id, returns_all):

        search_result = []
        dummy_list = search_in
        if type(search_in) == list:
            dummy_list = []
            for element in range(len(search_in)):
                dummy_list.append(element)
        for value in dummy_list:
            if type(value) == dict or type(value) == list:
                for element in value:
                    if isinstance(value[element], Iterable) and type(value[element]) != str:
                        search_result = search_result + self.search(value[element], search_for, search_id, returns_all)
            else:
                if str(value).startswith(search_for):
                    if str(search_in[value]).startswith(search_id) or returns_all:
                        if returns_all:
                            if type(search_in[value]) == list:
                                helpList = {}
                                for element in search_in[value]:
                                    search_result.append(element)
                            else:
                                search_result.append(search_in[value])
                        else:

                            search_result.append(search_in)
                if isinstance(search_in[value], Iterable) and type(search_in[value]) != str:
                    search_result = search_result + self.search(search_in[value], search_for, search_id, returns_all)

        return search_result

    def set_topology(self, json_topology):
        global topology
        self.topology = json_topology

    def get_node_element_list(self):
        node_element_list = []
        node_list = self.search(self.topology["radials"][0]["storageUnits"], "bus1", "", True)
        count = 0
        for element in node_list:
            pattern = re.compile("[^.]*")  # regex to find professID
            m = pattern.findall(element)
            element = m[0]
            node_element_list.append({element: [{"storageUnits": self.topology["radials"][0]["storageUnits"][count]}]})
            node_element_list[count][element].append(
                {"loads": (self.search(self.topology["radials"][0]["loads"], "bus", element, False))})
            # TODO PV etc
            count = count + 1
        return node_element_list

    def get_node_name_list(self):
        name_list = []
        for element in self.get_node_element_list():
            for value in element:
                name_list.append(value)
        return name_list
