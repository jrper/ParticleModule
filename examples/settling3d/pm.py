"""Example of particles settling under gravity."""
import particle_model as pm
import numpy

import pylab as p

S = '160'

N = 20

X = 0.5*(numpy.random.random((N, 3))-0.5)
X[:, 2] += 1.0

V = numpy.zeros((N, 3))

NAME = 'cylinder'

BOUNDARY = pm.IO.BoundaryData('cylinder_boundary.vtu')
TEMP_CACHE = pm.TemporalCache.TemporalCache(NAME)
SYSTEM = pm.System.System(BOUNDARY, gravity=numpy.array((0, 0, -1)),
                          temporal_cache=TEMP_CACHE)
PAR = pm.ParticleBase.PhysicalParticle(diameter=400e-6)

PB = pm.Particles.ParticleBucket(X, V, 0.0, 5.0e-3,
                                 system=SYSTEM,
                                 parameters=PAR)

TEMP_CACHE.data[1][0] = 100.0

PD = pm.IO.PolyData(NAME+'.vtp')
PD.append_data(PB)
pm.IO.write_level_to_polydata(PB, 0, NAME)

DATA = []
TIME = []

for i in range(30):
    DATA.append(-numpy.array(list(PB.vel()))[0, 2])
    TIME.append(PB.time)
    print PB.time
    print 'min, max: pos_z', PB.pos_as_array()[:, 2].min(), PB.pos_as_array()[:, 2].max()
    print 'min, max: vel_z', PB.vel_as_array()[:, 2].min(), PB.vel_as_array()[:, 2].max()
    PB.update()
    PD.append_data(PB)
    pm.IO.write_level_to_polydata(PB, i+1, NAME)
DATA.append(-numpy.array(list(PB.vel()))[0, 2])
TIME.append(PB.time)

p.plot(TIME, DATA, lw=2)
p.show()

PD.write()
pm.IO.collision_list_to_polydata(PB.collisions(), 'collisions%s.vtp'%NAME)
