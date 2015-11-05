import dronekit, time, uuid, logging
import IPC.message_object

logger = logging.getLogger(__name__)

class UavLink(object):
  """Encapsulates communications with Flight Controller"""

  def __init__(self):
    """
      Args:
        None
      Returns:
        None
    """

    logger.debug("Generating unique ID for craft")
    self._uuid = uuid.getnode()

    # Open MAV connection

    self._vehicle = dronekit.connect("127.0.0.1:14550", await_params=True)
    def wait_initialized(vehicle):
      logger.info("Waiting for Flight Controller to initialize...")
      while vehicle.mode.name == "INITIALIZING":
        logger.trace("Sleeping")
        time.sleep(.5)

      # Wait for vehicle state to be  come valid

      logger.info("Waiting for MAV messages to propagate")
      while vehicle.attitude.pitch == None:
        logger.trace("Sleeping")
        time.sleep(.5)
    wait_initialized(self._vehicle)
    logger.info("Vehicle fully initialized")

  #TODO: arm, takeoff, land

  def get_state(self):
    logger.debug("Getting vehicle state")

    altitude_local = None
    altitude_absolute = None
    if self._vehicle.location.global_frame.is_relative:
      altitude_local = self._vehicle.location.global_frame.alt
    else:
      altitude_absolute = self._vehicle.location.global_frame.alt

    state_message = IPC.message_object.VehicleState(self._uuid,
      vehicle_is_armed = self._vehicle.armed,
      attitude_pitch = self._vehicle.attitude.pitch,
      attitude_roll = self._vehicle.attitude.roll,
      velocity_array = self._vehicle.velocity,
      airspeed = self._vehicle.airspeed,
      groundspeed = self._vehicle.groundspeed,
      gps_fix_type = self._vehicle.gps_0.fix_type,
      latitude = self._vehicle.location.global_frame.lat,
      longitude = self._vehicle.location.global_frame.lon,
      altitude_absolute = altitude_absolute,
      altitude_relative = altitude_local,
      battery_level = self._vehicle.battery.level)
    return state_message
    #TODO

  def close(self):
    """
      Gracefully terminate UAV connection

      Args:
        None
      Returns:
        None
    """
    self._vehicle.close()
    self.__closed = True

  def __del__(self):
    if not self.__closed:
      self.close()
