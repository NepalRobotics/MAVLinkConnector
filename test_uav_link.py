import time
import _uav_link

def test_uav_status():
  uav_link = _uav_link.UavLink()
  print "Uav link connected. Getting state."
  for count in range(0,10):
    print uav_link.get_state().encode()
    time.sleep(.5)
  uav_link.close()

if __name__ == "__main__":
  test_uav_status()
