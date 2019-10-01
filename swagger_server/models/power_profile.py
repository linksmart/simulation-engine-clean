# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class PowerProfile(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, id: str=None, items: List[float]=None, interval: float=None, m_interval: float=None, s_interval: float=None, multiplier: float=None):  # noqa: E501
        """PowerProfile - a model defined in Swagger

        :param id: The id of this PowerProfile.  # noqa: E501
        :type id: str
        :param items: The items of this PowerProfile.  # noqa: E501
        :type items: List[float]
        :param interval: The interval of this PowerProfile.  # noqa: E501
        :type interval: float
        :param m_interval: The m_interval of this PowerProfile.  # noqa: E501
        :type m_interval: float
        :param s_interval: The s_interval of this PowerProfile.  # noqa: E501
        :type s_interval: float
        :param multiplier: The multiplier of this PowerProfile.  # noqa: E501
        :type multiplier: float
        """
        self.swagger_types = {
            'id': str,
            'items': List[float],
            'interval': float,
            'm_interval': float,
            's_interval': float,
            'multiplier': float
        }

        self.attribute_map = {
            'id': 'id',
            'items': 'items',
            'interval': 'interval',
            'm_interval': 'm_interval',
            's_interval': 's_interval',
            'multiplier': 'multiplier'
        }

        self._id = id
        self._items = items
        self._interval = interval
        self._m_interval = m_interval
        self._s_interval = s_interval
        self._multiplier = multiplier

    @classmethod
    def from_dict(cls, dikt) -> 'PowerProfile':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The PowerProfile of this PowerProfile.  # noqa: E501
        :rtype: PowerProfile
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> str:
        """Gets the id of this PowerProfile.


        :return: The id of this PowerProfile.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id: str):
        """Sets the id of this PowerProfile.


        :param id: The id of this PowerProfile.
        :type id: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def items(self) -> List[float]:
        """Gets the items of this PowerProfile.


        :return: The items of this PowerProfile.
        :rtype: List[float]
        """
        return self._items

    @items.setter
    def items(self, items: List[float]):
        """Sets the items of this PowerProfile.


        :param items: The items of this PowerProfile.
        :type items: List[float]
        """
        if items is None:
            raise ValueError("Invalid value for `items`, must not be `None`")  # noqa: E501

        self._items = items

    @property
    def interval(self) -> float:
        """Gets the interval of this PowerProfile.


        :return: The interval of this PowerProfile.
        :rtype: float
        """
        return self._interval

    @interval.setter
    def interval(self, interval: float):
        """Sets the interval of this PowerProfile.


        :param interval: The interval of this PowerProfile.
        :type interval: float
        """

        self._interval = interval

    @property
    def m_interval(self) -> float:
        """Gets the m_interval of this PowerProfile.


        :return: The m_interval of this PowerProfile.
        :rtype: float
        """
        return self._m_interval

    @m_interval.setter
    def m_interval(self, m_interval: float):
        """Sets the m_interval of this PowerProfile.


        :param m_interval: The m_interval of this PowerProfile.
        :type m_interval: float
        """

        self._m_interval = m_interval

    @property
    def s_interval(self) -> float:
        """Gets the s_interval of this PowerProfile.


        :return: The s_interval of this PowerProfile.
        :rtype: float
        """
        return self._s_interval

    @s_interval.setter
    def s_interval(self, s_interval: float):
        """Sets the s_interval of this PowerProfile.


        :param s_interval: The s_interval of this PowerProfile.
        :type s_interval: float
        """

        self._s_interval = s_interval

    @property
    def multiplier(self) -> float:
        """Gets the multiplier of this PowerProfile.


        :return: The multiplier of this PowerProfile.
        :rtype: float
        """
        return self._multiplier

    @multiplier.setter
    def multiplier(self, multiplier: float):
        """Sets the multiplier of this PowerProfile.


        :param multiplier: The multiplier of this PowerProfile.
        :type multiplier: float
        """

        self._multiplier = multiplier
