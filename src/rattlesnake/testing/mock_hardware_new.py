from rattlesnake.hardware.hardware_utilities import HardwareType
from rattlesnake.hardware.abstract_hardware import (
    HardwareMetadata,
    HardwareAcquisition,
    HardwareOutput,
)
from rattlesnake.hardware.hardware_registry import UNIMPLEMENTED_HARDWARE
from rattlesnake.testing.mock_utilities import mock_channel_list

HARDWARE_TYPE = HardwareType.NONE

IMPLEMENTED_HARDWARE = [
    hardware for hardware in HardwareType if hardware not in UNIMPLEMENTED_HARDWARE
]


class MockHardwareMetadata(HardwareMetadata):
    def __init__(
        self,
        channel_list=mock_channel_list(),
        sample_rate=1024,
        time_per_read=0.25,
        time_per_write=0.25,
    ):
        super().__init__(
            HARDWARE_TYPE,
            channel_list,
            sample_rate,
            time_per_read,
            time_per_write,
            output_oversample=1,
        )

    def validate(self):
        super().validate()
        return True

    def valid_channel_dict(self, channel):
        return super().valid_channel_dict(channel)

    @property
    def assist_mode_modules(self):
        return super().assist_mode_modules

    @classmethod
    def load_metadata_from_netcdf(cls, netcdf_dataset):
        (
            hardware_type,
            channel_list,
            sample_rate,
            time_per_read,
            time_per_write,
            output_oversample,
        ) = super().load_metadata_from_netcdf(netcdf_dataset)
        return cls(
            channel_list,
            sample_rate,
            time_per_read,
            time_per_write,
        )

    def save_metadata_to_netcdf(self, netcdf_dataset):
        return super().save_metadata_to_netcdf(netcdf_dataset)

    @classmethod
    def load_metadata_from_workbook(cls, workbook):
        (
            hardware_type,
            channel_list,
            sample_rate,
            time_per_read,
            time_per_write,
            output_oversample,
        ) = super().load_metadata_from_workbook(workbook)

        return cls(
            channel_list,
            sample_rate,
            time_per_read,
            time_per_write,
        )

    def save_metadata_to_workbook(self, workbook):
        return super().save_metadata_to_workbook(workbook)
