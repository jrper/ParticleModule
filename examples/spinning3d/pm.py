"""Example of particles in a centrifuge."""
import particle_model as pm
import numpy
from numpy import pi

S = '160'

N = 20

X = 0.5*(numpy.random.random((N, 3))-0.5)
X[:, 2] += 1.0

V = numpy.zeros((N, 3))

NAME = 'cylinder'

TEMP_CACHE = pm.TemporalCache.TemporalCache(NAME)
BOUNDARY = pm.IO.BoundaryData('cylinder_boundary.vtu')
SYSTEM = pm.System.System(BOUNDARY, gravity=numpy.array((0, 0, -1)),
                          omega=numpy.array((0, 0, 2*pi)),
                          temporal_cache=TEMP_CACHE,)
PAR = pm.ParticleBase.PhysicalParticle(diameter=400e-6)

PB = pm.Particles.ParticleBucket(X, V, 0.0, 1.0e-3,
                                 system=SYSTEM,
                                 parameters=PAR)

TEMP_CACHE.data[1][0] = 100.0

PD = pm.IO.PolyData(NAME+'.vtp')
PD.append_data(PB)
pm.IO.write_level_to_polydata(PB, 0, NAME)

for i in range(2000):
    print PB.time
    print 'min, max: pos_z', PB.pos[:, 2].ravel().min(), PB.pos[:, 2].ravel().max()
    print 'min, max: vel_z', PB.vel[:, 2].ravel().min(), PB.vel[:, 2].ravel().max()
    PB.update()
    if i%10 == 0:
        PD.append_data(PB)
        pm.IO.write_level_to_polydata(PB, i/10+1, NAME)

PD.write()
pm.IO.collision_list_to_polydata(PB.collisions(), 'collisions%s.vtp'%NAME)


