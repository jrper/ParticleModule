"""Example of particles in a 3d double gyre hitting wall."""
import particle_model as pm
import numpy
from numpy import pi, sin, cos

S = '160'

N = 400

X = 0.5+0.25*(numpy.random.random((N, 3))-0.5)
X[:, 0] += 0.2

V = numpy.zeros((N, 3))
V[:, 0] = -2.0*pi*sin(pi*X[:, 0])*sin(2.0*pi*(X[:, 1]+ X[:, 2]))
V[:, 1] = pi*cos(pi*X[:, 0])*sin(2.0*pi*X[:, 1])*sin(2.0*pi*X[:, 2])
V[:, 2] = pi*cos(pi*X[:, 0])*sin(2.0*pi*X[:, 1])*sin(2.0*pi*X[:, 2])

NAME = 'cube'

TEMP_CACHE = pm.TemporalCache.TemporalCache(NAME)
BOUNDARY = pm.IO.BoundaryData('cube_boundary.vtu')
SYSTEM = pm.System.System(BOUNDARY, temporal_cache=TEMP_CACHE)
PAR = pm.ParticleBase.PhysicalParticle(diameter=1e-3)

PB = pm.Particles.ParticleBucket(X, V, 0.0, 1.0e-3,
                                 system=SYSTEM,
                                 parameters=PAR)

TEMP_CACHE.data[1][0] = 100.0

PD = pm.IO.PolyData(NAME+'.vtp')
PD.append_data(PB)
pm.IO.write_level_to_polydata(PB, 0, NAME)

for i in range(300):
    print PB.time
    print 'min, max: pos_x', PB.pos_as_array()[:, 2].min(), PB.pos_as_array()[:, 2].max()
    print 'min, max: vel_x', PB.vel_as_array()[:, 2].min(), PB.vel_as_array()[:, 2].max()
    PB.update()
    PD.append_data(PB)
    pm.IO.write_level_to_polydata(PB, i+1, NAME)
PD.write()
pm.IO.collision_list_to_polydata(PB.collisions(), 'collisions%s.vtp'%NAME)
