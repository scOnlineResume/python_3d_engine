def cross_product(vec1,vec2):
    x_new = vec1[1]*vec2[2] - vec1[2]*vec2[1]
    y_new = -vec1[0]*vec2[2] + vec1[2]*vec2[0]
    z_new = vec1[0]*vec2[1] - vec1[1]*vec2[0]
    return (x_new,y_new,z_new)

def dot_product(vec1,vec2):
    return vec1[0]*vec2[0] + vec1[1]*vec2[1] +vec1[2]*vec2[2]

def vector_addition(vec1,vec2):
    vec3 = []
    vec3.append(vec1[0] + vec2[0])
    vec3.append(vec1[1] + vec2[1])
    vec3.append(vec1[2] + vec2[2])
    return vec3

def vector_scale(vector,scaling_factor):
    vec3 = []
    vec3.append(vector[0]*scaling_factor)
    vec3.append(vector[1]*scaling_factor)
    vec3.append(vector[2]*scaling_factor)
    return vec3

def vector_subtraction(vec1,vec2):
    vec3 = []
    vec3.append(vec1[0] - vec2[0])
    vec3.append(vec1[1] - vec2[1])
    vec3.append(vec1[2] - vec2[2])
    return vec3

