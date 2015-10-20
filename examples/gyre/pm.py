"""Example of particles in double gyre hitting wall."""
import particle_model as pm
import numpy

S = '40'

N = 400

X = 0.5+0.25*(numpy.random.random((N, 3))-0.5)
X[:, 0] += 0.2
X[:, 2] = 0

V = numpy.zeros((N, 3))
V[:, 0] = -2.0*numpy.pi*numpy.sin(numpy.pi*X[:, 0])*numpy.cos(2.0*numpy.pi*X[:, 1])
V[:, 1] = numpy.pi*numpy.cos(numpy.pi*X[:, 0])*numpy.sin(2.0*numpy.pi*X[:, 1])
U = numpy.zeros((N, 3))
GP = numpy.zeros((N, 3))

NAME = 'gyre%sx%s'%(S, S)

BOUNDARY = pm.IO.BoundaryData('Gyre_boundary.vtu')
TEMP_CACHE = pm.TemporalCache.TemporalCache(NAME)

PB = pm.Particles.ParticleBucket(X, V, 0.0, 1.0e-3, temporal_cache=TEMP_CACHE,
                                 U=U, GP=GP,
                                 boundary=BOUNDARY, diameter=1e-3)

TEMP_CACHE.data[1][0] = 100.0

PD = pm.IO.PolyData(NAME+'.vtp')
PD.append_data(PB)
pm.IO.write_level_to_polydata(PB, 0, NAME)

for i in range(300):
    print PB.time
    print 'min, max: pos_x', PB.pos[:, 0].ravel().min(), PB.pos[:, 0].ravel().max()
    print 'min, max: vel_x', PB.vel[:, 0].ravel().min(), PB.vel[:, 0].ravel().max()
    PB.update()
    PD.append_data(PB)
    pm.IO.write_level_to_polydata(PB, i+1, NAME)
    pm.IO.write_level_to_unstructured_grid(PB, i+1, NAME, PB.temporal_cache.data[0][2])
PD.write()
pm.IO.collision_list_to_polydata(PB.collisions(), 'collisions%s.vtp'%NAME)


