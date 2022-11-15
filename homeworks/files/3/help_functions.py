def tuple_elems_to_int(t):
    '''Converts all values of input tuple to ints.'''
    assert len(t) == 2, 'Only tuple with two elements is supported!'
    return (int(t[0]), int(t[1]))

def kq_of_line_segment(l_p1, l_p2):
    '''Computes slope (k) and translation (q) of input line segment defined with two points.'''
    a = np.array([[l_p1[0], 1], [l_p2[0], 1]])
    b = np.array([l_p1[1], l_p2[1]])
    
    k, q = np.linalg.solve(a, b)
    
    return k, q

def normal_kq_in_point(p1, k, q):
    '''Computes slope (kn) and translation (qn) of normal (perpendicular) line in point p1.'''
    kn = -1/k
    qn = p1[1] - kn * p1[0]
    return kn, qn

def normal_line_start_end_points(point, k, q, dx):
    '''Computes pixel points of perpendicular line segment of lenght dx in point point 
    to line defined by k and q.'''
    kn, qn = normal_kq_in_point(point, k, q)
    
    x = [point[0]-dx, point[0]+dx]
    y = [kn * x[0] + qn, kn * x[1] + qn]
    
    return (x[0], y[0]), (x[1], y[1])

def draw_norm_line_segment_in_point(l_p1, l_p2, point, dx, image):
    '''Draws perpendicular line segments to line defined with two points of lenght dx
    in point point to input image.'''
    k,q = kq_of_line_segment(l_p1, l_p2)
    start, end = normal_line_start_end_points(point, k, q, dx)
    cv2.line(image, tuple_elems_to_int(start), tuple_elems_to_int(end), (255,255,255), 1, cv2.LINE_4)
    return image

def draw_contour(image, contour):
    '''Draws input contour into image with white color.'''
    cv2.drawContours(image, contour, -1, (255,255,255), 1, cv2.LINE_4)
    return image