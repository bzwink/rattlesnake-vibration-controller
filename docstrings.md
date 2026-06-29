# Global Files


# Hardware

# Environment
<!---
MARK: Environment
--->


## Abstract Environment
<!---
MARK: Abstract Environment
--->
    """
    Abstract environment that can be used to create new environment control strategies
    in the controller.
    """

### Environment Commands
<!---
MARK: Environment Commands
--->
    class EnvironmentCommands:
    """
    Abstract base enum for commands that a controller can send to an environment.

    This enum is intended to be subclassed and used as a common interface for
    environment command definitions. Subclasses should define
    ``VALID_PROFILE_COMMANDS`` and ``VALID_DATA`` as enum members so they can
    be converted into command-specific values by the class methods provided.
    This class should be added to the ``ENVIRONMENT_COMMANDS`` dictionary
    within the environment registry.

    Attributes
    ----------
    VALID_PROFILE_COMMANDS : tuple of int
        Tuple of command values permitted for use in profile events.
    VALID_DATA : dict of int to type
        Mapping from command values to their expected associated data types.
        Used to validate profile event definitions before they are sent to
        the environment.

    Unit Tests
    ----------
    test_environment_commands
        Iterates through each enum member to confirm unique integer values.
        Verifies that ``VALID_PROFILE_COMMANDS`` is a tuple of ints and
        ``VALID_DATA`` is a dict mapping ints to types.
    """

    property
    def label:
    """
    Return a user-friendly label for the command.

    Converts the enum member name by replacing underscores with spaces and
    converting to title case.

    Returns
    -------
    str
        User-friendly command label for the UI.

    Unit Tests
    ----------
    test_environment_commands_label
        Checks that labels replace underscores with spaces and use title
        case.
    """

    classmethod
    def valid_profile_commands:
    """
    Return the commands valid for use in profile events.

    Converts the values in ``VALID_PROFILE_COMMANDS`` into enum members of
    the current class.

    Returns
    -------
    tuple of EnvironmentCommands
        Enum members permitted for profile events.

    Unit Tests
    ----------
    test_environment_commands_valid_profile_commands
        Ensures this method returns a tuple of EnvironmentCommands
        members corresponding to VALID_PROFILE_COMMANDS.
    """

    classmethod
    def valid_data:
    """
    Return the valid data types associated with each command.

    Converts the key-value pairs in ``VALID_DATA`` into enum-member keys
    mapped to their data types.

    Returns
    -------
    dict of EnvironmentCommands to type
        Mapping from command members to expected data types.

    Unit Tests
    ----------
    test_environment_commands_valid_data
        Verifies this method returns a dict mapping enum members to their
        predefined types.
    """

### Environment UI Commands
<!---
MARK: Environment UI Commands
--->
    class EnvironmentUICommands
    """
    Base enum for UI-specific commands associated with environments.

    This enum is intended to define commands that are needed by the user
    interface but are not part of the standard environment command set.
    Subclasses may extend this enum with additional UI-only commands used
    to update widgets, communicate UI state, or trigger UI-specific
    behavior.

    Unit Tests
    ----------
    test_environment_ui_commands
        Verifies that the enum can be instantiated or subclassed for
        UI-specific command definitions and that any defined enum members
        have unique values.
    """

### Environment Metadata
<!---
MARK: Environment Metadata
--->
    class EnvironmentMetadata
    """
    Abstract base class for storing environment metadata.

    This class stores the parameters required to fully define an
    environment. Metadata objects are typically created by environment UI
    classes and passed to the controller during environment initialization.
    Subclasses must include enough information to reconstruct the
    environment configuration, validate it against hardware metadata, and
    serialize or deserialize it from supported file formats.
    This class should be added to the ``ENVIRONMENT_METADATA`` dictionary
    within the environment registry.

    Parameters
    ----------
    environment_type : EnvironmentType
        Type of environment represented by this metadata object.
    environment_name : str
        Environment name used for logging, UI display, and
        task identification.
    channel_list_bools : list of bool
        Boolean mask identifying which hardware channels are used by this
        environment. Each entry corresponds to an entry in the hardware
        channel list.
    sample_rate : int
        Sample rate associated with the environment.

    Attributes
    ----------
    environment_type : EnvironmentType
        Type of environment represented by this metadata object.
    environment_name : str
        Name used for logging, UI display, and task identification.
    sample_rate : int
        Environment sample rate.
    channel_list_bools : list of bool
        Boolean mask identifying channels assigned to the environment.
    queue_name : str
        Unique queue identifier assigned by the controller for routing
        environment-specific messages. This is assigned by the environment
        manager when spinning up the environment process.

    Unit Tests
    ----------
    test_environment_metadata
        Verifies that subclasses within ``ENVIRONMENT_METADATA`` in the 
        registry initialize required metadata attributes and preserve the 
        supplied environment type, name, channel mask, and sample rate.
    """

    def __init__
    """
    Initialize environment metadata.

    Stores the common metadata required by all environment types. The
    environment type should normally be fixed by subclasses when calling
    ``super().__init__`` so users do not need to provide it directly.

    Parameters
    ----------
    environment_type : EnvironmentType
        Type of environment represented by this metadata object.
    environment_name : str
        Environment name used for logging, UI display, and
        task identification.
    channel_list_bools : list of bool
        Boolean mask identifying which hardware channels belong to the
        environment.
    sample_rate : int
        Sample rate associated with the environment.

    Unit Tests
    ----------
    test_environment_metadata_init
        Confirms that initialization stores the environment type,
        environment name, sample rate, channel list bools, and
        initializes ``queue_name`` to ``None``.
    """

    property
    def channel_indices
    """
    Return indices of hardware channels assigned to the environment.

    The indices are computed from ``channel_list_bools`` by returning
    the positions where the mask value is true.

    Returns
    -------
    list of int
        Indices of channels selected for this environment.

    Unit Tests
    ----------
    test_environment_metadata_channel_indices
        Verifies that selected channel indices correspond to true
        entries in ``channel_list_bools``.
    """

    def environment_channel_list
    """
    Return the subset of channels assigned to the environment.

    Applies ``channel_list_bools`` as a Boolean mask to the supplied
    hardware channel list and returns only the channels assigned to
    this environment.

    Parameters
    ----------
    channel_list : list
        Full hardware channel list.

    Returns
    -------
    list of Channel
        Channels from ``channel_list`` whose corresponding
        ``channel_list_bools`` entries are true.

    Unit Tests
    ----------
    test_environment_metadata_environment_channel_list
        Confirms that the returned channel list contains only channels
        selected by ``channel_list_bools`` and preserves their original
        order.
    """

    def validate
    """
    Validate environment metadata against hardware metadata.

    Performs common metadata validation checks required by all
    environments. Subclasses should extend this method with
    environment-specific checks, such as verifying control channels,
    duplicate channel assignments, or environment-specific parameter
    bounds. This should throw an error if metadata fails to pass
    validation.

    Parameters
    ----------
    hardware_metadata : HardwareMetadata
        Hardware metadata containing the available hardware channel
        list and other hardware configuration parameters.

    Raises
    ------
    RattlesnakeError
        If ``environment_type`` is not an ``EnvironmentType``.
    RattlesnakeError
        If ``environment_name`` is not a string.
    RattlesnakeError
        If ``channel_list_bools`` is not the same length as the
        hardware channel list.

    Unit Tests
    ----------
    test_environment_metadata_validate_truth
        Verifies that valid mock metadata class passes the validation check.

    test_environment_metadata_validate_invalid_environment_type
        Verifies that an error is thrown with an invalid environment type object.

    test_environment_metadata_validate_invalid_environment_name
        Verifies that an error is thrown when the environment name is not a string.

    test_environment_metadata_validate_invalid_channel_list
        Verifies that an erros is thrown when an invalid channel list is given to the metadata.
    """

    def save_metadata_to_netcdf
    """
    Save environment metadata to a netCDF group.

    Stores parameters for this environment in the supplied netCDF group.
    Subclasses should write all information required to reconstruct the
    environment metadata, using group attributes, dimensions, or
    variables as appropriate.

    Parameters
    ----------
    netcdf_group_handle : nc4._netCDF4.Group
        netCDF group where this environment's metadata should be
        stored.

    Unit Tests
    ----------
    test_environment_metadata_load_save_netcdf
        Saves a valid metadata subclass to a netcdf file and then loads
        it back into a metadata object. Verifies that the metadata object
        is valid and that the netcdf handle contains environment_name and
        environment_type.
    """

    classmethod
    def load_metadata_from_netcdf
    """
    Load environment metadata from a netCDF dataset or group.

    Retrieves metadata previously written by
    ``save_metadata_to_netcdf`` and constructs an environment metadata
    object. Subclasses should read parameters from the group associated
    with ``environment_name`` and use the supplied hardware metadata as
    needed to reconstruct or validate the environment configuration.

    Parameters
    ----------
    netcdf_handle : nc4._netCDF4.Group
        netCDF dataset or group containing stored environment metadata.
    environment_name : str
        Name of the environment whose metadata should be loaded.
    channel_list_bools : list of bool
        Boolean channel mask identifying channels assigned to the
        environment.
    hardware_metadata : HardwareMetadata
        Hardware metadata associated with the stored environment.

    Returns
    -------
    EnvironmentMetadata
        Instance of the metadata subclass populated from the netCDF
        data.

    Unit Tests
    ----------
    test_environment_metadata_load_save_netcdf
        Saves a valid metadata subclass to a netcdf file and then loads
        it back into a metadata object. Verifies that the metadata object
        is valid and that the netcdf handle contains environment_name and
        environment_type.
    """

    classmethod
    def create_blank_worksheet_template
    """
    Create a blank Excel worksheet template for environment metadata.

    Writes the common worksheet fields required by environment metadata
    exports. Subclasses should extend this template with
    environment-specific metadata fields.

    Parameters
    ----------
    worksheet : openpyxl.worksheet.worksheet.Worksheet
        Worksheet where the blank metadata template should be created.

    Unit Tests
    ----------
    test_environment_metadata_load_save_worksheet
        Saves a valid metadata subclass to a worksheet file and then loads
        it back into a metadata object. Verifies that the metadata object
        is valid and that the worksheet cell 1, 2 contains a string of the
        environment type. 

    Notes
    -----
    Worksheet cell 1, 2 must be set to a string of the environment type.
    """

    def save_metadata_to_worksheet
    """
    Save environment metadata to an Excel worksheet.

    Stores parameters for this environment in the supplied worksheet.
    This method should write all information required to reconstruct the
    metadata from the worksheet. Subclasses should call or extend
    ``create_blank_worksheet_template`` before writing
    environment-specific values.

    Parameters
    ----------
    worksheet : openpyxl.worksheet.worksheet.Worksheet
        Worksheet where this environment's metadata should be stored.

    Unit Tests
    ----------
    test_environment_metadata_load_save_worksheet
        Saves a valid metadata subclass to a worksheet file and then loads
        it back into a metadata object. Verifies that the metadata object
        is valid and that the worksheet cell 1, 2 contains a string of the
        environment type. 
    """

    classmethod
    def load_metadata_from_worksheeet
    """
    Load environment metadata from an Excel worksheet.

    Retrieves metadata previously written by
    ``save_metadata_to_worksheet`` and constructs an environment
    metadata object. Subclasses should read all required
    environment-specific parameters from the worksheet.

    Parameters
    ----------
    worksheet : openpyxl.worksheet.worksheet.Worksheet
        Worksheet containing stored environment metadata.
    environment_name : str
        Name of the environment whose metadata should be loaded.
    channel_list_bools : list of bool
        Boolean channel mask identifying channels assigned to the
        environment.
    hardware_metadata : HardwareMetadata
        Hardware metadata associated with the stored environment.

    Returns
    -------
    EnvironmentMetadata
        Instance of the metadata subclass populated from the worksheet.

    Unit Tests
    ----------
    test_environment_metadata_load_save_worksheet
        Saves a valid metadata subclass to a worksheet file and then loads
        it back into a metadata object. Verifies that the metadata object
        is valid and that the worksheet cell 1, 2 contains a string of the
        environment type. 
    """

### Environment Instructions
<!---
MARK: Environment Instructions
--->
    class EnvironmentInstructions
    """
    Abstract base class for environment startup instructions.

    Environment instructions define runtime parameters that are passed to an
    environment when control is started. These parameters are separate from
    environment metadata because they may change between runs and do not
    necessarily need to be stored as part of the environment definition.

    Instructions are commonly sent to the controller before starting an
    environment or when starting a profile. Subclasses should include any
    environment-specific startup values needed by the environment control
    strategy and should validate that those values are compatible with the
    target environment.

    Parameters
    ----------
    environment_type : EnvironmentType
        Type of environment that these instructions apply to.
    environment_name : str
        Name of the environment that these instructions apply to.

    Attributes
    ----------
    environment_type : EnvironmentType
        Type of environment that these instructions apply to. This is used
        to verify that the instructions are sent to the correct environment.
    environment_name : str
        Name of the environment that these instructions apply to.

    Unit Tests
    ----------
    test_environment_instructions
        Verifies that instruction subclasses initialize the required
        environment type and environment name attributes.
    """

    def __init__
    """
    Initialize environment instructions.

    Stores the common instruction attributes required by all environment
    instruction subclasses. The environment type should normally be fixed by
    subclasses when calling ``super().__init__`` so users do not need to
    provide it directly.

    Parameters
    ----------
    environment_type : EnvironmentType
        Type of environment that these instructions apply to.
    environment_name : str
        Name of the environment that these instructions apply to.

    Unit Tests
    ----------
    test_environment_instructions_init
        Confirms that initialization stores the environment type and
        environment name.
    """

    def validate
    """
    Validate environment startup instructions.

    Subclasses should implement this method to verify that all instruction
    values are valid for the corresponding environment. This should include
    checks for value ranges, compatible modes, required startup parameters,
    and any other environment-specific constraints.

    This method should throw an error if the instructions fail validation.

    Raises
    ------
    RattlesnakeError
        If any instruction value is invalid for the environment.

    Unit Tests
    ----------
    test_environment_instructions_validate_truth
        Verifies that a valid mock instruction subclass passes the validation
        check.
    """

### Environment
<!---
MARK: Environment
--->
    class Environment
    """
    Abstract base class defining the controller-side environment process.

    This class defines the common interface used by the controller to manage
    an environment. Environment subclasses receive commands through an
    environment command queue, map those commands to callable methods, and
    exchange data with acquisition, output, GUI, controller, and logging
    processes through queues and events.

    Subclasses must implement the hardware initialization, environment
    initialization, and graceful shutdown behavior required by the specific
    environment control strategy. Additional environment-specific commands
    can be registered by adding entries to ``command_map`` with
    ``map_command``. This class should be added to the ``ENVIRONMENT_CLASS``
    dictionary within the environment registry.

    Parameters
    ----------
    environment_name : str
        Environment name used for logging, UI display, and
        task identification.
    queue_name : str
        Unique queue identifier assigned by the environment manager for
        routing environment-specific messages.
    command_queue : VerboseMessageQueue
        Queue used to receive commands sent to this environment.
    gui_update_queue : multiprocessing.Queue or queue.Queue
        Queue used to send GUI update commands.
    controller_command_queue : VerboseMessageQueue
        Queue used to send commands back to the controller.
    log_file_queue : multiprocessing.Queue
        Queue used to send messages to the logging process.
    data_in_queue : multiprocessing.Queue or queue.Queue
        Queue used to receive acquired data from the acquisition process.
    data_out_queue : multiprocessing.Queue or queue.Queue
        Queue used to send output data to the output process.
    acquisition_active_event : multiprocessing.synchronize.Event
        Event indicating whether acquisition is active.
    output_active_event : multiprocessing.synchronize.Event
        Event indicating whether output is active.
    active_event : multiprocessing.synchronize.Event
        Event indicating whether this environment is active.
    ready_event : multiprocessing.synchronize.Event
        Event indicating whether this environment is ready.

    Attributes
    ----------
    environment_name : str
        Environment name used for logging, UI display, and
        task identification.
    hardware_metadata : HardwareMetadata
        Hardware metadata used by the environment after initialization.
    environment_metadata : EnvironmentMetadata
        Environment metadata used by the environment after initialization.
    """

    def __init__
    """
    Initialize the environment process object.

    Stores queues, events, names, and default state needed by the environment.
    Also initializes the command map with global controller commands for
    quitting, hardware initialization, environment initialization, and
    environment shutdown.

    Parameters
    ----------
    environment_name : str
        Environment name used for logging, UI display, and
        task identification.
    queue_name : str
        Unique queue identifier assigned by the environment manager.
    command_queue : VerboseMessageQueue
        Queue used to receive environment commands.
    gui_update_queue : multiprocessing.Queue
        Queue used to send GUI updates.
    controller_command_queue : VerboseMessageQueue
        Queue used to send commands to the controller.
    log_file_queue : multiprocessing.Queue
        Queue used to send log messages.
    data_in_queue : multiprocessing.Queue
        Queue used to receive acquired data.
    data_out_queue : multiprocessing.Queue
        Queue used to send output data.
    acquisition_active_event : multiprocessing.synchronize.Event
        Event indicating whether acquisition is active.
    output_active_event : multiprocessing.synchronize.Event
        Event indicating whether output is active.
    active_event : multiprocessing.synchronize.Event
        Event indicating whether this environment is active.
    ready_event : multiprocessing.synchronize.Event
        Event indicating whether this environment is ready.

    Unit Tests
    ----------
    test_environment_init
        Confirms that initialization stores all queues and events, initializes
        metadata attributes to ``None``, and maps the default global commands.
    """

    property
    def command_map
    """
    Return the command-to-function mapping for this environment.

    The command map is used by ``run`` to determine which environment method
    should be called when a command is received from the command queue.

    Returns
    -------
    dict
        Mapping from command enum members to bound environment methods.

    Unit Tests
    ----------
    test_environment_command_map
        Verifies that the default command map contains expected global
        commands and maps them to callable methods.
    """

    def map_command
    """
    Map a command to an environment method.

    Adds or replaces an entry in ``command_map``. The mapped function must
    accept one input argument containing the command data, even if that data
    is ignored.

    Parameters
    ----------
    key : Enum
        Command key that will be received from the environment command queue.
    function : callable
        Function to call when ``key`` is received.

    Unit Tests
    ----------
    test_environment_map_command
        Confirms that a new command can be added to the command map and maps
        to the provided callable.
    """

    def set_ready
    """
    Set the environment ready event.

    Marks the environment as ready for controller operations.

    Unit Tests
    ----------
    test_environment_set_ready
        Verifies that calling this method sets the ready event.
    """

    def clear_ready
    """
    Clear the environment ready event.

    Marks the environment as not ready for controller operations.

    Unit Tests
    ----------
    test_environment_clear_ready
        Verifies that calling this method clears the ready event.
    """

    property
    def ready
    """
    Return whether the environment is ready.

    Returns
    -------
    bool
        ``True`` if the ready event is set, otherwise ``False``.

    Unit Tests
    ----------
    test_environment_ready
        Verifies that this property reflects the state of the ready event.
    """

    def set_active
    """
    Set the environment active event.

    Marks the environment as active.

    Unit Tests
    ----------
    test_environment_set_active
        Verifies that calling this method sets the active event.
    """

    def clear_active
    """
    Clear the environment active event.

    Marks the environment as inactive.

    Unit Tests
    ----------
    test_environment_clear_active
        Verifies that calling this method clears the active event.
    """

    property
    def active
    """
    Return whether the environment is active.

    Returns
    -------
    bool
        ``True`` if the active event is set, otherwise ``False``.

    Unit Tests
    ----------
    test_environment_active
        Verifies that this property reflects the state of the active event.
    """

    property
    def acquisition_active
    """
    Return whether acquisition is active.

    Returns
    -------
    bool
        ``True`` if the acquisition active event is set, otherwise ``False``.

    Unit Tests
    ----------
    test_environment_acquisition_active
        Verifies that this property reflects the state of the acquisition
        active event.
    """

    property
    def output_active
    """
    Return whether output is active.

    Returns
    -------
    bool
        ``True`` if the output active event is set, otherwise ``False``.

    Unit Tests
    ----------
    test_environment_output_active
        Verifies that this property reflects the state of the output active
        event.
    """

    def initialize_hardware
    """
    Initialize hardware metadata for the environment.

    Stores the hardware metadata received from the controller. Subclasses
    should extend this method to perform hardware-dependent setup required by
    the environment. Subclasses should call ``set_ready`` when initialization
    is complete if the environment is ready for operation.

    Parameters
    ----------
    hardware_metadata : HardwareMetadata
        Hardware metadata containing hardware configuration information
        needed by the environment.

    Unit Tests
    ----------
    test_environment_initialize_hardware
        Verifies that a mock environment subclass stores the supplied hardware
        metadata and sets itself as ready at the end of the function.
    """

    def initialize_environment
    """
    Initialize environment-specific metadata.

    Stores environment metadata received from the controller and updates the
    environment name from the metadata object. Subclasses should extend this
    method to perform environment-specific setup. Subclasses should call
    ``set_ready`` when initialization is complete if the environment is ready
    for operation.

    Parameters
    ----------
    environment_metadata : EnvironmentMetadata
        Metadata object containing the parameters defining this environment.

    Unit Tests
    ----------
    test_environment_initialize_environment
        Verifies that a mock environment subclass stores the supplied
        environment metadata and updates the environment name. Checks
        that subclasses set their ready event at the end of the function.
    """

    property
    def queue_name
    """
    Return the unique queue name assigned to the environment.

    Returns
    -------
    str
        Queue name used to route environment-specific messages.

    Unit Tests
    ----------
    test_environment_queue_name
        Verifies that this property returns the queue name supplied during
        initialization.
    """

    property
    def environment_command_queue
    """
    Return the environment command queue.

    Returns
    -------
    VerboseMessageQueue
        Queue used to receive commands sent to this environment.

    Unit Tests
    ----------
    test_environment_environment_command_queue
        Verifies that this property returns the command queue supplied during
        initialization.
    """

    property
    def data_in_queue
    """
    Return the data input queue.

    Returns
    -------
    queue.Queue or multiprocessing.Queue
        Queue used to receive acquired data from the acquisition process.

    Unit Tests
    ----------
    test_environment_data_in_queue
        Verifies that this property returns the data input queue supplied
        during initialization.
    """

    property
    def data_out_queue
    """
    Return the data output queue.

    Returns
    -------
    queue.Queue or multiprocessing.Queue
        Queue used to send output data to the output process.

    Unit Tests
    ----------
    test_environment_data_out_queue
        Verifies that this property returns the data output queue supplied
        during initialization.
    """

    property
    def gui_update_queue
    """
    Return the GUI update queue.

    Returns
    -------
    queue.Queue or multiprocessing.Queue
        Queue used to send update commands to the GUI.

    Unit Tests
    ----------
    test_environment_gui_update_queue
        Verifies that this property returns the GUI update queue supplied
        during initialization.
    """

    property
    def controller_command_queue
    """
    Return the controller command queue.

    Returns
    -------
    VerboseMessageQueue
        Queue used to send commands from the environment back to the
        controller.

    Unit Tests
    ----------
    test_environment_controller_command_queue
        Verifies that this property returns the controller command queue
        supplied during initialization.
    """

    property
    def log_file_queue
    """
    Return the log file queue.

    Returns
    -------
    multiprocessing.Queue
        Queue used to send log messages to the logging process.

    Unit Tests
    ----------
    test_environment_log_file_queue
        Verifies that this property returns the log file queue supplied during
        initialization.
    """

    def log
    """
    Queue a message for the log file.

    Formats the supplied message with the current timestamp and environment
    name, then places it on the log file queue.

    Parameters
    ----------
    message : str
        Message to write to the log file.

    Unit Tests
    ----------
    test_environment_log
        Verifies that calling this method places a formatted log message on
        the log file queue.
    """

    def run
    """
    Run the environment command loop.

    A function that is called by the environment's process function that
    sits in a while loop waiting for instructions on the command queue.

    When the instructions are recieved, they are separated into
    ``(message,data)`` pairs.  The ``message`` is used in conjuction with
    the ``command_map`` to identify which function should be called, and
    the ``data`` is passed to that function as the argument.  If the
    function returns a truthy value, it signals to the ``run`` function
    that it is time to stop the loop and exit.

    Parameters
    ----------
    shutdown_event : multiprocessing.synchronize.Event
        Event used to signal that the environment command loop should stop.

    Unit Tests
    ----------
    test_environment_run_quit
        Verifies that the command loop exits when a mapped command returns a
        truthy halt flag.

    test_environment_run_undefined_command
        Verifies that an undefined command is logged and does not halt the
        environment.

    test_environment_run_command_exception
        Verifies that an exception raised by a mapped command is logged and
        sent to the GUI update queue.
    """

    def stop_environment
    """
    Stop the environment gracefully.

    This function defines the operations to shut down the environment
    gracefully. This should include any operations needed to avoid 
    abrupt output changes, protect test equipment, stop background 
    activity, and clear environment state as appropriate.

    Parameters
    ----------
    data : Any
        Command data supplied through the command queue. This may be ignored
        by implementations that do not require additional shutdown data.

    Unit Tests
    ----------
    test_environment_stop_environment
        Verifies that a mock environment subclass performs graceful shutdown
        behavior and clears or updates expected state.
    """

    def quit
    """
    Signal the environment command loop to stop.

    Returns ``True`` so the ``run`` loop exits after processing the quit
    command.

    Parameters
    ----------
    data : Any
        Command data supplied through the command queue. This value is
        ignored.

    Returns
    -------
    bool
        Always returns ``True`` to indicate that the environment process
        should stop.

    Unit Tests
    ----------
    test_environment_quit
        Verifies that this method returns ``True``.
    """

### Process
<!---
MARK: Process
--->
    def process
    """
    Function executed by ``multiprocessing.Process`` to start an environment.

    This function serves as the entry point for an environment process. It
    constructs an ``Environment`` instance with the supplied communication
    queues and synchronization events, then runs the environment until
    ``shutdown_event`` is set. It is intended to be used as the target of a
    ``multiprocessing.Process`` and should not be called directly.

    Parameters
    ----------
    environment_name : str
        Name of the environment.

    queue_name : str
        Name used to identify the environment's communication queues.

    input_queue : VerboseMessageQueue
        Queue used to receive commands sent to the environment.

    gui_update_queue : queue.Queue or multiproccessing.Queue
        Queue used to send ``(message, data)`` pairs to the GUI.

    controller_command_queue : VerboseMessageQueue
        Queue used to send commands to the controller.

    log_file_queue : multiproccessing.Queue
        Queue used to send log messages to the logging process.

    data_in_queue : queue.Queue or multiproccessing.Queue
        Queue used to receive acquired data from the acquisition process.

    data_out_queue : queue.Queue or multiproccessing.Queue
        Queue used to send output data to the output process.

    acquisition_active_event : multiprocessing.synchronize.Event
        Event indicating whether the acquisition process is active.

    output_active_event : multiprocessing.synchronize.Event
        Event indicating whether the output process is active.

    active_event : multiprocessing.synchronize.Event
        Event indicating whether the environment is running.

    ready_event : multiprocessing.synchronize.Event
        Event set when the environment has completed initialization and is
        ready to receive commands.

    shutdown_event : multiprocessing.synchronize.Event
        Event used to signal the environment to terminate.

    sysid_active_event : multiprocessing.synchronize.Event
        Event indicating whether system identification is active.

    sysid_stored_event : multiprocessing.synchronize.Event
        Event indicating that system identification data has been stored.

    ping_alive_event : multiprocessing.synchronize.Event
        Event used to restart the blocking timeout if environment is going to
        stall the main process for an extended time.

    threaded : bool
        Indicates whether the environment is running in threaded mode rather
        than multiprocessing mode.

    Unit Tests
    ----------
    test_process
        Verifies that valid environment process functions execute without
        starting up processes.
    """


## Abstract Sys Id Environment
<!---
MARK: Abstract Sysid Environment
--->
    """
    Abstract environment that can be used to create new environment control strategies
    in the controller that use system identification.
    """

### System Id Commands
<!---
MARK: System Id Commands
--->
    class SystemIdCommands
    """
    Enumeration of commands that could be sent to the system identification environment

    Unit Tests
    ----------
    test_sysid_commands
        Iterates through each enum member to confirm unique integer values.
    """

    class SystemIdUICommands
    """
    Enumeration of commands that are sent from the system identifcation environment to the
    system identification user interface

    Unit Tests
    ----------
    test_sysid_ui_commands
        Iterates through each enum member to confirm unique integer values.
    """

### System Id Envrionment Metadata
<!---
MARK: System Id Environment Metadata
--->
    class SysIdEnvironmentMetadata
    """
    Abstract base class for metadata used by environments supporting system
    identification.

    Extends ``EnvironmentMetadata`` with the information required to perform
    system identification measurements. In addition to the standard
    environment definition, this class stores a ``SysIdMetadata`` object
    describing excitation signals, spectral processing parameters, averaging,
    and related system identification settings.

    Subclasses must define the physical channel mappings, transformation
    matrices, and any additional environment-specific metadata required to
    perform system identification.

    Parameters
    ----------
    environment_type : EnvironmentType
        Type of environment represented by this metadata.
    environment_name : str
        Name of the environment.
    channel_list_bools : list of bool
        Boolean mask identifying channels assigned to the environment.
    sample_rate : int
        Environment sample rate.
    sysid_metadata : SysIdMetadata, optional
        System identification metadata. If omitted, default metadata is
        created using the supplied sample rate.

    Attributes
    ----------
    sysid_metadata : SysIdMetadata
        Metadata defining excitation signals and processing parameters used
        for system identification.

    Unit Tests
    ----------
    test_sysid_environment_metadata
        Verifies that subclasses initialize the base metadata and create a
        valid ``SysIdMetadata`` instance when one is not supplied.
    """

    def __init__
    """
    Initialize system identification environment metadata.

    Initializes the base environment metadata and stores the associated
    system identification metadata. If no metadata is supplied, a default
    ``SysIdMetadata`` object is created using the supplied sample rate.

    Parameters
    ----------
    environment_type : EnvironmentType
        Type of environment.
    environment_name : str
        Name of the environment.
    channel_list_bools : list of bool
        Boolean channel mask.
    sample_rate : int
        Environment sample rate.
    sysid_metadata : SysIdMetadata, optional
        Metadata defining the system identification parameters.

    Unit Tests
    ----------
    test_sysid_environment_metadata_init
        Verifies that supplied metadata is stored and that default metadata is
        created when no metadata is provided.
    """

# Process

# User Interface

# Examples

# Testing







