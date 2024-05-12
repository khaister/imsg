#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import platform
from enum import Enum


class Platform(Enum):
    OTHER = 0
    LINUX = 1
    MAC = 2
    WINDOWS = 3


def get_platform() -> str:
    system = platform.system()
    if system == "Linux":
        return str(Platform.LINUX.name)
    if system == "Darwin":
        return str(Platform.MAC.name)
    if system == "Windows":
        return str(Platform.WINDOWS.name)
    raise NotImplementedError(f"Platform {system} is not supported")
