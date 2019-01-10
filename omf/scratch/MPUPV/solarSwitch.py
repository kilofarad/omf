import sys
sys.path.append('../CIGAR')
from cosim import GridLabWorld

glw = GridLabWorld('6267', 'localhost', 'GC-solarAdd.glm', '2000-01-01 0:00:00')
glw.start()
print (glw.readClock())
print (glw.read('test_solar', 'generator_status'))
glw.write('test_solar','generator_status', 'OFFLINE')
print ('Switched off solar')
print (glw.read('test_solar', 'generator_status'))
#glw.waitUntil('2000-01-01 0:30:00')
#print ('Stepped ahead 12 hours')
print (glw.readClock())
glw.resume()
print (glw.readClock())
#glw.shutdown()