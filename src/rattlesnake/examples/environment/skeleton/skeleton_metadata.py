import openpyxl
import netCDF4 as nc4

import rattlesnake.examples.defaults

from rattlesnake.environment.environment_utilities import EnvironmentType
from rattlesnake.environment.skeleton_environment import (
    SkeletonCommands,
    SkeletonMetadata,
    SkeletonInstructions,
)

ENVIRONMENT_NAME = "Skeleton 0"


def manual_skeleton_metadata(hardware_metadata):
    channel_list_bools = [True] * len(hardware_metadata.channel_list)
    window_size = 10

    metadata = SkeletonMetadata(
        ENVIRONMENT_NAME,
        channel_list_bools,
        hardware_metadata.sample_rate,
        window_size,
    )

    return metadata


def skeleton_instructions():
    test_level = 1
    return SkeletonInstructions(ENVIRONMENT_NAME, test_level)
