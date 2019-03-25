from numpy import *
from numpy.linalg import norm

def collision(p1, r1, p2, r2):
    ''' 
    Returns collision information from circle (p1,r1) with circle (p2,r2). 
    '''

    # The vector between the objects
    v_diff = p1 - p2

    # The length between the objects
    d = max(norm(v_diff),0.01)

    # Calculate the overlap (sum of radii - distance between centers)
    overlap = (r1 + r2) - d 

    return v_diff, overlap, d

def overlap(p1, r1, p2, r2):
    ''' 
    Returns the overlap of circle (p1,r1) with circle (p2,r2).
    Note: The overlap will be positive if the circles are colliding. 
    '''
    return collision(p1,r1,p2,r2)[1]

def slide_apart(obj_1,obj_2):
    ''' Objects obj_1 and obj_2 slide away from each other until they no longer
        touch each other '''

    # Calculate the collision / overlap
    v_diff, overlap, d = collision(obj_1.pos,obj_1.radius,obj_2.pos,obj_2.radius)

    # If objects are are overlapping ...
    if overlap > 0:
        # ... slide them apart 
        u = v_diff / d
        velocity = u * overlap/1.9 + 1.
        obj_1.pos = obj_1.pos + velocity
        obj_2.pos = obj_2.pos - velocity

def slide_off(s,p,min_dist=5.):
    ''' Object 's' slides off point 'p' acccording to its own velocity 
    (and by at least 'min_dist') '''
    # TODO - calculate the exact distance required to move it
    s.speed = max(min_dist,s.speed)
    s.unitv = unitv(s.pos - p)
    s.pos = s.pos + s.unitv * s.speed

def rotate(v, theta=0.1):
    ''' rotation vector v by angle theta '''
    c = cos(theta)
    s = sin(theta)
    M = array([[c,-s],[s,c]])
    return M.dot(v)

def unitv(v):
    ''' unit vector of v '''
    d = norm(v)
    if d == 0:
        return [0., 1.]
    return v / d

def angle_deg(v):
    ''' angle of a vector v (in degrees) '''
    a = int(arctan2(v[0],v[1]) * 180. / pi)
    if a < 0:
        a = 360 + a
    return a

def angle_cos(v1,v2):
    ''' return the cosine of the angle between v1 and v2 (not normalized) '''
    return arccos(dot(v1,v2)/(norm(v1)*norm(v2)))

def angle_of_attack(obj_1, obj_2):
    ''' the angle between two objects: obj_1 and a obj_2 
    wrt obj_1 approaching obj_2 '''
    x = obj_2.pos - obj_1.pos
    xnorm = norm(x) # vector between the two
    if xnorm <= 0:
        # they objects are the same
        return 0.
    # The angle between vector x and v
    return arccos(dot(x/xnorm,obj_1.unitv))

def angles_of_attack(obj_1, obj_2):
    ''' the angles between two objects: obj_1 and a obj_2 
    wrt each other.'''
    return [arccos(dot(unitv(obj_2.pos - obj_1.pos),obj_1.unitv)), 
            arccos(dot(unitv(obj_1.pos - obj_2.pos),obj_2.unitv))]

