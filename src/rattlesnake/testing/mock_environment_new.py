import multiprocessing as mp

from rattlesnake.utilities import VerboseMessageQueue, QueueContainer, EventContainer
from rattlesnake.environment.environment_utilities import EnvironmentType
from rattlesnake.environment.abstract_environment import (
    EnvironmentCommands,
    EnvironmentMetadata,
    EnvironmentInstructions,
    Environment,
)
from rattlesnake.environment.environment_registry import UNIMPLEMENTED_ENVIRONMENT
from rattlesnake.testing.mock_utilities import (
    mock_channel_list_bools,
)

ENVIRONMENT_TYPE = EnvironmentType.NONE

IMPLEMENTED_ENVIRONMENT = [
    environment
    for environment in EnvironmentType
    if environment not in UNIMPLEMENTED_ENVIRONMENT
]


class MockEnvironmentCommands(EnvironmentCommands):
    PROFILE_COMMAND = 1
    FLOAT_COMMAND = 2
    COMMAND = 3

    VALID_PROFILE_COMMANDS = (PROFILE_COMMAND, FLOAT_COMMAND)
    VALID_DATA = {
        PROFILE_COMMAND: type(None),
        FLOAT_COMMAND: float,
    }


class MockEnvironmentMetadata(EnvironmentMetadata):
    def __init__(
        self,
        environment_name="Mock Environment",
        channel_list_bools=mock_channel_list_bools(),
        sample_rate=1024,
    ):
        super().__init__(
            ENVIRONMENT_TYPE,
            environment_name,
            channel_list_bools,
            sample_rate,
        )

    def validate(self, hardware_metadata):
        return super().validate(hardware_metadata)

    def save_metadata_to_netcdf(self, netcdf_group_handle):
        return super().save_metadata_to_netcdf(netcdf_group_handle)

    @classmethod
    def load_metadata_from_netcdf(
        cls,
        netcdf_handle,
        environment_name,
        channel_list_bools,
        hardware_metadata,
    ):
        return cls(
            environment_name,
            channel_list_bools,
            hardware_metadata.sample_rate,
        )

    @classmethod
    def create_blank_worksheet_template(cls, worksheet):
        super().create_blank_worksheet_template(worksheet)
        worksheet.cell(1, 2, "None")

    def save_metadata_to_worksheet(self, worksheet):
        super().save_metadata_to_worksheet(worksheet)

    @classmethod
    def load_metadata_from_worksheet(
        cls,
        worksheet,
        environment_name,
        channel_list_bools,
        hardware_metadata,
    ):
        return cls(
            environment_name,
            channel_list_bools,
            hardware_metadata.sample_rate,
        )


class MockEnvironmentInstructions(EnvironmentInstructions):
    def __init__(
        self,
        environment_name="Mock Environment",
    ):
        super().__init__(
            ENVIRONMENT_TYPE,
            environment_name,
        )

    def validate(self):
        return super().validate()


class MockQueues:
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


class MockEnvironment(Environment):
    def __init__(
        self,
        environment_name: str,
        queue_name: str,
        queue_container: QueueContainer,
        acquisition_active_event,
        output_active_event,
        active_event,
        ready_event,
    ):
        super().__init__(
            environment_name,
            queue_name,
            queue_container.environment_command_queues[queue_name],
            queue_container.gui_update_queue,
            queue_container.controller_command_queue,
            queue_container.log_file_queue,
            queue_container.environment_data_in_queues[queue_name],
            queue_container.environment_data_out_queues[queue_name],
            acquisition_active_event,
            output_active_event,
            active_event,
            ready_event,
        )

        self.set_ready()

    def initialize_hardware(self, hardware_metadata):
        super().initialize_hardware(hardware_metadata)
        self.set_ready()

    def initialize_environment(self, environment_metadata):
        super().initialize_environment(environment_metadata)
        self.set_ready()
        return None

    def stop_environment(self, data):
        super().stop_environment(data)
        self.clear_active()


def mock_environment_process(
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
    ping_alive_event: mp.synchronize.Event,
    threaded: bool,
):
    queue_container = MockQueues(
        input_queue,
        gui_update_queue,
        controller_command_queue,
        data_in_queue,
        data_out_queue,
        log_file_queue,
    )
    environment_class = MockEnvironment(
        environment_name,
        queue_name,
        queue_container,
        acquisition_active_event,
        output_active_event,
        active_event,
        ready_event,
    )
    environment_class.run(shutdown_event)
