from enum import Enum
from typing import List
import multiprocessing as mp

import netCDF4 as nc4
import openpyxl

from rattlesnake.utilities import VerboseMessageQueue
from rattlesnake.hardware.abstract_hardware import HardwareMetadata
from rattlesnake.environment.environment_utilities import EnvironmentType
from rattlesnake.environment.abstract_environment import (
    Environment,
    EnvironmentCommands,
    EnvironmentInstructions,
    EnvironmentMetadata,
)

CONTROL_TYPE = EnvironmentType.READ


# region Commands
class ReadCommands(EnvironmentCommands):
    pass


class ReadUICommands(Enum):
    pass


# endregion


class ReadMetadata(EnvironmentMetadata):
    # region Metadata
    def __init__(
        self,
        environment_type,
        environment_name,
        channel_list_bools,
        sample_rate,
    ):
        super().__init__(
            environment_type, environment_name, channel_list_bools, sample_rate
        )

    # endregion

    # region Validation
    def validate(self, hardware_metadata):
        return super().validate(hardware_metadata)

    # endregion

    def save_metadata_to_netcdf(
        self,
        netcdf_group_handle: nc4._netCDF4.Group,  # pylint: disable=c-extension-no-member
    ):
        pass

    @classmethod
    def load_metadata_from_netcdf(
        cls,
        group: nc4._netCDF4.Dataset,
        environment_name: str,
        channel_list_bools: List[bool],
        hardware_metadata: HardwareMetadata,
    ):
        pass

    @staticmethod
    def create_blank_worksheet_template(worksheet):
        pass

    def save_metadata_to_worksheet(
        self, worksheet: openpyxl.worksheet.worksheet.Worksheet
    ):
        pass

    @classmethod
    def load_metadata_from_worksheet(
        cls,
        worksheet: openpyxl.worksheet.worksheet.Worksheet,
        environment_name: str,
        channel_list_bools: List[bool],
        hardware_metadata: HardwareMetadata,
    ):
        pass


# endregion


# region Instructions
class ReadInstructions(EnvironmentInstructions):
    pass


# endregion


# region Queues
class ReadQueues:
    def __init__(
        self,
        environment_command_queue: VerboseMessageQueue,
        gui_update_queue: mp.queues.Queue,
        controller_communication_queue: VerboseMessageQueue,
        data_in_queue: mp.queues.Queue,
        data_out_queue: mp.queues.Queue,
        log_file_queue: VerboseMessageQueue,
    ):
        self.environment_command_queue = environment_command_queue
        self.gui_update_queue = gui_update_queue
        self.controller_communication_queue = controller_communication_queue
        self.data_in_queue = data_in_queue
        self.data_out_queue = data_out_queue
        self.log_file_queue = log_file_queue


# region Environment
class ReadEnvironment(Environment):
    def __init__(
        environment_name: str,
        queue_name: str,
        queue_container: ReadQueues,
        acquisition_active_event: mp.synchronize.Event,
        output_active_event: mp.synchronize.Event,
        active_event: mp.synchronize.Event,
        ready_event: mp.synchronize.Event,
    ):
        super().__init__(
            environment_name,
            queue_name,
            queue_container.environment_command_queue,
            queue_container.gui_update_queue,
            queue_container.controller_communication_queue,
            queue_container.log_file_queue,
            queue_container.data_in_queue,
            queue_container.data_out_queue,
            acquisition_active_event,
            output_active_event,
            active_event,
            ready_event,
        )


# endregion


# region Process
def read_process(
    environment_name: str,
    queue_name: str,
    input_queue: VerboseMessageQueue,
    gui_update_queue: mp.Queue,
    controller_command_queue: VerboseMessageQueue,
    log_file_queue: mp.Queue,
    data_in_queue: mp.Queue,
    data_out_queue: mp.Queue,
    acquisition_active_event: mp.synchronize.Event,
    output_active_event: mp.synchronize.Event,
    active_event: mp.synchronize.Event,
    ready_event: mp.synchronize.Event,
    shutdown_event: mp.synchronize.Event,
    sysid_active_event: mp.synchronize.Event,
    sysid_stored_event: mp.synchronize.Event,
    threaded: bool,
):
    queue_container = ReadQueues(
        input_queue,
        gui_update_queue,
        controller_command_queue,
        data_in_queue,
        data_out_queue,
        log_file_queue,
    )

    process_class = ReadEnvironment(
        environment_name,
        queue_name,
        queue_container,
        acquisition_active_event,
        output_active_event,
        active_event,
        ready_event,
    )
    process_class.run(shutdown_event)


# endregion
