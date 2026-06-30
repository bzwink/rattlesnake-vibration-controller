import queue as thqueue
import threading
import inspect

import netCDF4 as nc4
import openpyxl
import pytest
from unittest.mock import Mock

from rattlesnake.utilities import RattlesnakeError
from rattlesnake.environment.environment_utilities import EnvironmentType
from rattlesnake.environment.environment_registry import (
    ENVIRONMENT_COMMANDS,
    ENVIRONMENT_METADATA,
    ENVIRONMENT_CLASS,
)
from rattlesnake.examples.example_registry import ENVIRONMENT_DICT
from rattlesnake.testing.mock_utilities import (
    instantiate_with_mocks,
    mock_channel_list,
    mock_channel_list_bools,
)
from rattlesnake.testing.mock_environment_new import (
    IMPLEMENTED_ENVIRONMENT,
    MockEnvironmentCommands,
    MockEnvironmentMetadata,
    MockEnvironmentInstructions,
    MockEnvironment,
    mock_environment_process,
)
from rattlesnake.testing.mock_hardware_new import MockHardwareMetadata


# region Fixtures
@pytest.fixture
def hardware_metadata():
    return MockHardwareMetadata()


# endregion


# region Environment Commands
@pytest.mark.parametrize("environment_type", IMPLEMENTED_ENVIRONMENT)
def test_environment_commands_have_unique_integer_values(environment_type):
    """
    Iterates through each enum member to confirm unique integer values.
    Verifies that ``VALID_PROFILE_COMMANDS`` is a tuple of ints and
    ``VALID_DATA`` is a dict mapping ints to types.
    """
    command_class = ENVIRONMENT_COMMANDS[environment_type]

    command_members = [
        member
        for name, member in command_class.__members__.items()
        if name not in {"VALID_PROFILE_COMMANDS", "VALID_DATA"}
    ]

    values = [member.value for member in command_members]

    assert all(isinstance(value, int) for value in values)
    assert len(values) == len(set(values))

    valid_profile_commands = command_class.VALID_PROFILE_COMMANDS.value
    valid_data = command_class.VALID_DATA.value

    assert isinstance(valid_profile_commands, tuple)
    assert all(isinstance(command, int) for command in valid_profile_commands)

    assert isinstance(valid_data, dict)
    assert all(isinstance(key, int) for key in valid_data.keys())
    assert all(isinstance(value, type) for value in valid_data.values())


def test_environment_commands_label():
    """
    Checks that labels replace underscores with spaces and use title
    case.
    """
    assert MockEnvironmentCommands.PROFILE_COMMAND.label == "Profile Command"


def test_environment_commands_valid_profile_commands():
    """
    Ensures this method returns a tuple of EnvironmentCommands
    members corresponding to VALID_PROFILE_COMMANDS.
    """
    assert MockEnvironmentCommands.valid_profile_commands() == (
        MockEnvironmentCommands.PROFILE_COMMAND,
        MockEnvironmentCommands.FLOAT_COMMAND,
    )


def test_environment_commands_valid_data():
    """
    Verifies this method returns a dict mapping enum members to their
    predefined types.
    """
    assert MockEnvironmentCommands.valid_data() == {
        MockEnvironmentCommands.PROFILE_COMMAND: type(None),
        MockEnvironmentCommands.FLOAT_COMMAND: float,
    }


# endregion


# region Environment Metadata
@pytest.mark.parametrize("environment_type", IMPLEMENTED_ENVIRONMENT)
def test_environment_metadata(environment_type):
    """
    Verifies that subclasses within ``ENVIRONMENT_METADATA`` in the
    registry initialize required metadata attributes and preserve the
    supplied environment type, name, channel mask, and sample rate.
    """
    metadata_class = ENVIRONMENT_METADATA[environment_type]
    channel_list_bools = mock_channel_list_bools()
    metadata = instantiate_with_mocks(
        metadata_class,
        environment_name="test_environment",
        channel_list_bools=channel_list_bools,
        sample_rate=2048,
    )

    assert metadata.environment_name == "test_environment"
    assert metadata.channel_list_bools == channel_list_bools
    assert metadata.sample_rate == 2048


def test_environment_metadata_init():
    """
    Confirms that initialization stores the environment type,
    environment name, sample rate, channel list bools, and
    initializes ``queue_name`` to ``None``.
    """
    metadata = MockEnvironmentMetadata(
        environment_name="Env A",
        channel_list_bools=[True, False, True],
        sample_rate=2048,
    )

    assert metadata.environment_type == EnvironmentType.NONE
    assert metadata.environment_name == "Env A"
    assert metadata.channel_list_bools == [True, False, True]
    assert metadata.sample_rate == 2048
    assert metadata.queue_name is None


def test_environment_metadata_channel_indices():
    """
    Verifies that selected channel indices correspond to true
    entries in ``channel_list_bools``.
    """
    metadata = MockEnvironmentMetadata(channel_list_bools=[True, False, True, False])

    assert metadata.channel_indices == [0, 2]


def test_environment_metadata_environment_channel_list():
    """
    Confirms that the returned channel list contains only channels
    selected by ``channel_list_bools`` and preserves their original
    order.
    """
    metadata = MockEnvironmentMetadata(channel_list_bools=[True, False, True])
    channel_list = ["ch0", "ch1", "ch2"]

    assert metadata.environment_channel_list(channel_list) == ["ch0", "ch2"]


def test_environment_metadata_validate_truth(hardware_metadata):
    """
    Verifies that valid mock metadata class passes the validation check.
    """
    metadata = MockEnvironmentMetadata(
        environment_name="Env A",
        channel_list_bools=[True, False],
    )

    metadata.validate(hardware_metadata)


def test_environment_metadata_validate_invalid_environment_type(hardware_metadata):
    """
    Verifies that an error is thrown with an invalid environment type object.
    """
    metadata = MockEnvironmentMetadata()
    metadata.environment_type = object()

    with pytest.raises(RattlesnakeError):
        metadata.validate(hardware_metadata)


def test_environment_metadata_validate_invalid_environment_name(hardware_metadata):
    """
    Verifies that an error is thrown when the environment name is not a string.
    """
    metadata = MockEnvironmentMetadata()
    metadata.environment_name = 123

    with pytest.raises(RattlesnakeError):
        metadata.validate(hardware_metadata)


def test_environment_metadata_validate_invalid_channel_list(hardware_metadata):
    """
    Verifies that an error is thrown when an invalid channel list is given to the metadata.
    """
    metadata = MockEnvironmentMetadata()
    metadata.channel_list_bools = [True, False, True]

    with pytest.raises(RattlesnakeError):
        metadata.validate(hardware_metadata)


@pytest.mark.parametrize("environment_type", IMPLEMENTED_ENVIRONMENT)
def test_environment_metadata_load_save_netcdf(
    environment_type, tmp_path, hardware_metadata
):
    """
    Saves a valid metadata subclass to a netcdf file and then loads
    it back into a metadata object. Verifies that the metadata object
    is valid and that the netcdf handle contains environment_name and
    environment_type.
    """
    metadata_class = ENVIRONMENT_METADATA[environment_type]
    metadata = ENVIRONMENT_DICT[environment_type]["manual"](hardware_metadata)
    metadata.environment_name = "Environment Name"

    path = tmp_path / "metadata.nc"

    with nc4.Dataset(path, "w") as dataset:
        group = dataset.createGroup(metadata.environment_name)
        metadata.save_metadata_to_netcdf(group)

    with nc4.Dataset(path, "r") as dataset:
        loaded = metadata_class.load_metadata_from_netcdf(
            netcdf_handle=dataset,
            environment_name="Mock Environment",
            channel_list_bools=mock_channel_list_bools(),
            hardware_metadata=hardware_metadata,
        )

        group = dataset.groups["Environment Name"]
        assert group.environment_name == "Environment Name"
        assert group.environment_type == str(environment_type)
        assert int(group.sample_rate) == 4096

    assert loaded.environment_name == "Environment Name"
    assert loaded.channel_list_bools == [True, False, True]
    assert loaded.sample_rate == 4096
    loaded.validate(hardware_metadata)


# def test_environment_metadata_load_save_worksheet(hardware_metadata):
#     metadata = MockEnvironmentMetadata(
#         environment_name="Mock Environment",
#         channel_list_bools=[True, False, True],
#         sample_rate=8192,
#     )

#     workbook = openpyxl.Workbook()
#     worksheet = workbook.active

#     metadata.save_metadata_to_worksheet(worksheet)

#     assert worksheet.cell(1, 1).value == "Control Type"
#     assert worksheet.cell(1, 2).value == str(ENVIRONMENT_TYPE)
#     assert worksheet.cell(1, 3).value == "v4.0"
#     assert worksheet.cell(2, 2).value == "Mock Environment"
#     assert worksheet.cell(3, 2).value == 8192

#     loaded = MockEnvironmentMetadata.load_metadata_from_worksheet(
#         worksheet=worksheet,
#         environment_name="Mock Environment",
#         channel_list_bools=[True, False, True],
#         hardware_metadata=hardware_metadata,
#     )

#     assert loaded.environment_name == "Mock Environment"
#     assert loaded.channel_list_bools == [True, False, True]
#     assert loaded.sample_rate == 8192
#     loaded.validate(hardware_metadata)


# # ---------------------------------------------------------------------------
# # EnvironmentInstructions tests
# # ---------------------------------------------------------------------------


# def test_environment_instructions_init():
#     instructions = MockEnvironmentInstructions(environment_name="Env A")

#     assert instructions.environment_type == ENVIRONMENT_TYPE
#     assert instructions.environment_name == "Env A"


# def test_environment_instructions_validate_truth():
#     instructions = MockEnvironmentInstructions()

#     instructions.validate()


# def test_environment_instructions_validate_error():
#     instructions = MockEnvironmentInstructions(should_raise=True)

#     with pytest.raises(RattlesnakeError):
#         instructions.validate()


# # ---------------------------------------------------------------------------
# # Environment tests
# # ---------------------------------------------------------------------------


# def test_environment_init(environment):
#     assert environment.environment_name == "Mock Environment"
#     assert environment.queue_name == "mock_environment_queue"
#     assert environment.hardware_metadata is None
#     assert environment.environment_metadata is None

#     assert GlobalCommands.QUIT in environment.command_map
#     assert GlobalCommands.INITIALIZE_HARDWARE in environment.command_map
#     assert GlobalCommands.INITIALIZE_ENVIRONMENT in environment.command_map
#     assert GlobalCommands.STOP_ENVIRONMENT in environment.command_map


# def test_environment_command_map(environment):
#     assert environment.command_map[GlobalCommands.QUIT] == environment.quit
#     assert environment.command_map[GlobalCommands.INITIALIZE_HARDWARE] == (
#         environment.initialize_hardware
#     )
#     assert environment.command_map[GlobalCommands.INITIALIZE_ENVIRONMENT] == (
#         environment.initialize_environment
#     )
#     assert environment.command_map[GlobalCommands.STOP_ENVIRONMENT] == (
#         environment.stop_environment
#     )


# def test_environment_map_command(environment):
#     command = object()

#     def handler(data):
#         return data

#     environment.map_command(command, handler)

#     assert environment.command_map[command] == handler


# def test_environment_set_ready(environment):
#     environment.set_ready()

#     assert environment.ready is True


# def test_environment_clear_ready(environment):
#     environment.set_ready()
#     environment.clear_ready()

#     assert environment.ready is False


# def test_environment_ready(environment):
#     assert environment.ready is False

#     environment.set_ready()

#     assert environment.ready is True


# def test_environment_set_active(environment):
#     environment.set_active()

#     assert environment.active is True


# def test_environment_clear_active(environment):
#     environment.set_active()
#     environment.clear_active()

#     assert environment.active is False


# def test_environment_active(environment):
#     assert environment.active is False

#     environment.set_active()

#     assert environment.active is True


# def test_environment_acquisition_active(environment):
#     assert environment.acquisition_active is False

#     environment._acquisition_active_event.set()  # pylint: disable=protected-access

#     assert environment.acquisition_active is True


# def test_environment_output_active(environment):
#     assert environment.output_active is False

#     environment._output_active_event.set()  # pylint: disable=protected-access

#     assert environment.output_active is True


# def test_environment_initialize_hardware(environment, hardware_metadata):
#     environment.initialize_hardware(hardware_metadata)

#     assert environment.hardware_metadata is hardware_metadata
#     assert environment.ready is True


# def test_environment_initialize_environment(environment):
#     metadata = MockEnvironmentMetadata(environment_name="Updated Environment")

#     environment.initialize_environment(metadata)

#     assert environment.environment_metadata is metadata
#     assert environment.environment_name == "Updated Environment"
#     assert environment.ready is True


# def test_environment_queue_name(environment):
#     assert environment.queue_name == "mock_environment_queue"


# def test_environment_environment_command_queue(environment, command_queue):
#     assert environment.environment_command_queue is command_queue


# def test_environment_data_in_queue(environment):
#     assert (
#         environment.data_in_queue is environment._data_in_queue
#     )  # pylint: disable=protected-access


# def test_environment_data_out_queue(environment):
#     assert (
#         environment.data_out_queue is environment._data_out_queue
#     )  # pylint: disable=protected-access


# def test_environment_gui_update_queue(environment):
#     assert (
#         environment.gui_update_queue is environment._gui_update_queue
#     )  # pylint: disable=protected-access


# def test_environment_controller_command_queue(environment, controller_command_queue):
#     assert environment.controller_command_queue is controller_command_queue


# def test_environment_log_file_queue(environment):
#     assert (
#         environment.log_file_queue is environment._log_file_queue
#     )  # pylint: disable=protected-access


# def test_environment_log(environment):
#     environment.log("hello world")

#     log_message = environment.log_file_queue.get_nowait()

#     assert "Mock Environment -- hello world" in log_message


# def test_environment_run_quit(controller_command_queue):
#     command_queue = FakeVerboseMessageQueue(
#         messages=[
#             (GlobalCommands.QUIT, None),
#         ]
#     )

#     environment = MockEnvironment(
#         environment_name="Mock Environment",
#         queue_name="mock_environment_queue",
#         command_queue=command_queue,
#         gui_update_queue=thqueue.Queue(),
#         controller_command_queue=controller_command_queue,
#         log_file_queue=thqueue.Queue(),
#         data_in_queue=thqueue.Queue(),
#         data_out_queue=thqueue.Queue(),
#         acquisition_active_event=threading.Event(),
#         output_active_event=threading.Event(),
#         active_event=threading.Event(),
#         ready_event=threading.Event(),
#     )

#     shutdown_event = threading.Event()

#     environment.run(shutdown_event)

#     logs = []
#     while not environment.log_file_queue.empty():
#         logs.append(environment.log_file_queue.get_nowait())

#     assert any("Starting Process" in message for message in logs)
#     assert any("Stopping Process" in message for message in logs)


# def test_environment_run_undefined_command(controller_command_queue):
#     undefined_command = object()
#     command_queue = FakeVerboseMessageQueue(
#         messages=[
#             (undefined_command, None),
#             (GlobalCommands.QUIT, None),
#         ]
#     )

#     environment = MockEnvironment(
#         environment_name="Mock Environment",
#         queue_name="mock_environment_queue",
#         command_queue=command_queue,
#         gui_update_queue=thqueue.Queue(),
#         controller_command_queue=controller_command_queue,
#         log_file_queue=thqueue.Queue(),
#         data_in_queue=thqueue.Queue(),
#         data_out_queue=thqueue.Queue(),
#         acquisition_active_event=threading.Event(),
#         output_active_event=threading.Event(),
#         active_event=threading.Event(),
#         ready_event=threading.Event(),
#     )

#     shutdown_event = threading.Event()

#     environment.run(shutdown_event)

#     logs = []
#     while not environment.log_file_queue.empty():
#         logs.append(environment.log_file_queue.get_nowait())

#     assert any("Undefined Message" in message for message in logs)
#     assert any("Stopping Process" in message for message in logs)


# def test_environment_run_command_exception(controller_command_queue):
#     failing_command = object()
#     command_queue = FakeVerboseMessageQueue(
#         messages=[
#             (failing_command, None),
#             (GlobalCommands.QUIT, None),
#         ]
#     )

#     environment = MockEnvironment(
#         environment_name="Mock Environment",
#         queue_name="mock_environment_queue",
#         command_queue=command_queue,
#         gui_update_queue=thqueue.Queue(),
#         controller_command_queue=controller_command_queue,
#         log_file_queue=thqueue.Queue(),
#         data_in_queue=thqueue.Queue(),
#         data_out_queue=thqueue.Queue(),
#         acquisition_active_event=threading.Event(),
#         output_active_event=threading.Event(),
#         active_event=threading.Event(),
#         ready_event=threading.Event(),
#     )

#     def boom(data):  # pylint: disable=unused-argument
#         raise RuntimeError("boom")

#     environment.map_command(failing_command, boom)

#     shutdown_event = threading.Event()

#     environment.run(shutdown_event)

#     gui_message, gui_data = environment.gui_update_queue.get_nowait()

#     assert gui_message == UICommands.ERROR
#     assert gui_data[0] == "Mock Environment Error"
#     assert "RuntimeError: boom" in gui_data[1]


# def test_environment_stop_environment(environment):
#     environment.set_active()

#     environment.stop_environment("shutdown data")

#     assert environment.stopped_with == "shutdown data"
#     assert environment.active is False


# def test_environment_quit(environment):
#     assert environment.quit(None) is True


# def test_process_is_abstract_template(command_queue, controller_command_queue):
#     """
#     The abstract module-level process() function attempts to instantiate
#     Environment directly. Since Environment is abstract, this documents that
#     concrete environment modules should provide their own process entry point.
#     """

#     with pytest.raises(TypeError):
#         process(
#             environment_name="Mock Environment",
#             queue_name="mock_environment_queue",
#             input_queue=command_queue,
#             gui_update_queue=thqueue.Queue(),
#             controller_command_queue=controller_command_queue,
#             log_file_queue=thqueue.Queue(),
#             data_in_queue=thqueue.Queue(),
#             data_out_queue=thqueue.Queue(),
#             acquisition_active_event=threading.Event(),
#             output_active_event=threading.Event(),
#             active_event=threading.Event(),
#             ready_event=threading.Event(),
#             shutdown_event=threading.Event(),
#             sysid_active_event=threading.Event(),
#             sysid_stored_event=threading.Event(),
#             ping_alive_event=threading.Event(),
#             threaded=True,
#         )
