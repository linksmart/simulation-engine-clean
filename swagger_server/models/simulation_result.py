# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.error import Error  # noqa: F401,E501
from swagger_server.models.voltage import Voltage  # noqa: F401,E501
from swagger_server import util


class SimulationResult(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, node_id: str=None, voltage: Voltage=None, error: Error=None):  # noqa: E501
        """SimulationResult - a model defined in Swagger

        :param node_id: The node_id of this SimulationResult.  # noqa: E501
        :type node_id: str
        :param voltage: The voltage of this SimulationResult.  # noqa: E501
        :type voltage: Voltage
        :param error: The error of this SimulationResult.  # noqa: E501
        :type error: Error
        """
        self.swagger_types = {
            'node_id': str,
            'voltage': Voltage,
            'error': Error
        }

        self.attribute_map = {
            'node_id': 'nodeId',
            'voltage': 'voltage',
            'error': 'error'
        }

        self._node_id = node_id
        self._voltage = voltage
        self._error = error

    @classmethod
    def from_dict(cls, dikt) -> 'SimulationResult':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The SimulationResult of this SimulationResult.  # noqa: E501
        :rtype: SimulationResult
        """
        return util.deserialize_model(dikt, cls)

    @property
    def node_id(self) -> str:
        """Gets the node_id of this SimulationResult.


        :return: The node_id of this SimulationResult.
        :rtype: str
        """
        return self._node_id

    @node_id.setter
    def node_id(self, node_id: str):
        """Sets the node_id of this SimulationResult.


        :param node_id: The node_id of this SimulationResult.
        :type node_id: str
        """

        self._node_id = node_id

    @property
    def voltage(self) -> Voltage:
        """Gets the voltage of this SimulationResult.


        :return: The voltage of this SimulationResult.
        :rtype: Voltage
        """
        return self._voltage

    @voltage.setter
    def voltage(self, voltage: Voltage):
        """Sets the voltage of this SimulationResult.


        :param voltage: The voltage of this SimulationResult.
        :type voltage: Voltage
        """

        self._voltage = voltage

    @property
    def error(self) -> Error:
        """Gets the error of this SimulationResult.


        :return: The error of this SimulationResult.
        :rtype: Error
        """
        return self._error

    @error.setter
    def error(self, error: Error):
        """Sets the error of this SimulationResult.


        :param error: The error of this SimulationResult.
        :type error: Error
        """

        self._error = error
