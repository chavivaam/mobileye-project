import numpy as np
import matplotlib.pyplot as plt


def visualize(prev_container, curr_container, focal, pp):
    plt.subplot(3, 1, 3)
    plt.ylabel("Distance")
    norm_prev_pts, norm_curr_pts, R, norm_foe, tZ = prepare_3D_data(prev_container, curr_container, focal, pp)
    norm_rot_pts = rotate(norm_prev_pts, R)
    rot_pts = unnormalize(norm_rot_pts, focal, pp)
    foe = np.squeeze(unnormalize(np.array([norm_foe]), focal, pp))

    plt.imshow(curr_container.img)
    curr_p = np.array(curr_container.traffic_light)
    plt.plot(curr_p[:, 0], curr_p[:, 1], 'g.')

    for i in range(len(curr_p)):
        if curr_container.valid[i]:
            plt.text(curr_p[i, 0], curr_p[i, 1],
                          r'{0:.1f}'.format(curr_container.traffic_lights_3d_location[i, 2]), color='r')

    print("after filter", len(curr_p))

def calc_TFL_dist(prev_container, curr_container, focal, pp):
    norm_prev_pts, norm_curr_pts, R, foe, tZ = prepare_3D_data(prev_container, curr_container, focal, pp)

    if (abs(tZ) < 10e-6):
        print('tz = ', tZ)
    elif (norm_prev_pts.size == 0):
        print('no prev points')
    elif (norm_curr_pts.size == 0):
        print('no curr points')
    else:
        curr_container.corresponding_ind, curr_container.traffic_lights_3d_location, curr_container.valid = calc_3D_data(norm_prev_pts, norm_curr_pts, R, foe, tZ)
    return curr_container


def prepare_3D_data(prev_container, curr_container, focal, pp):
    norm_prev_pts = normalize(prev_container.traffic_light, focal, pp)
    norm_curr_pts = normalize(curr_container.traffic_light, focal, pp)
    R, foe, tZ = decompose(np.array(curr_container.EM))
    return norm_prev_pts, norm_curr_pts, R, foe, tZ


def calc_3D_data(norm_prev_pts, norm_curr_pts, R, foe, tZ):
    norm_rot_pts = rotate(norm_prev_pts, R)
    pts_3D = []
    corresponding_ind = []
    validVec = []
    for p_curr in norm_curr_pts:
        corresponding_p_ind, corresponding_p_rot = find_corresponding_points(p_curr, norm_rot_pts, foe)
        Z = calc_dist(p_curr, corresponding_p_rot, foe, tZ)
        valid = (Z > 0)
        if not valid:
            Z = 0
        validVec.append(valid)
        P = Z * np.array([p_curr[0], p_curr[1], 1])
        pts_3D.append((P[0], P[1], P[2]))
        corresponding_ind.append(corresponding_p_ind)
    return corresponding_ind, np.array(pts_3D), validVec


def normalize(pts, focal, pp):
    # transform pixels into normalized pixels using the focal length and principle point
    normalized_points = []
    for point in pts:
        x_ = (point[0] - pp[0])/focal
        y_ = (point[1] - pp[1])/focal
        normalized_points.append([x_, y_])
    return np.array(normalized_points)


def unnormalize(pts, focal, pp):
    unnormalized_points = [[(point[0]*focal + pp[0]), (point[1]*focal + pp[1])] for point in pts]
    return  np.array(unnormalized_points)
    # transform normalized pixels into pixels using the focal length and principle point


def decompose(EM):
    R = EM[:3, :3]
    tX = EM[0, 3]
    tY = EM[1, 3]
    tZ = EM[2, 3]
    if (abs(tZ) > 10e-6):
        foe = np.array([tX / tZ, tY/tZ])
    else:
        foe = []
    return R, foe, tZ
    # extract R, foe and tZ from the Ego Motion


def rotate(pts, R):
    # rotate the points - pts using R
    rotated_points = []
    for point in pts:
        rotated_point = np.matmul(R, np.array([point[0], point[1], 1]))
        rotated_point /= rotated_point[2]
        rotated_points.append(rotated_point[:2])
    return np.array(rotated_points)


def distance(x, y, n, m):
    mone = m * x + n - y
    denominator = np.sqrt(m ** 2 + 1)
    dist = abs(mone / denominator)
    return dist


def find_corresponding_points(p, norm_pts_rot, foe):
    # compute the epipolar line between p and foe
    # run over all norm_pts_rot and find the one closest to the epipolar line
    # return the closest point and its index
    e_x = foe[0]
    e_y = foe[1]
    m = (e_y - p[1]) / (e_x - p[0])
    n = (p[1]*e_x - e_y*p[0]) / (e_x - p[0])
    closest_point_distance = np.Infinity
    closest_point_index = 0
    for i, point in enumerate(norm_pts_rot):
        p_distance = distance(point[0], point[1], n, m)
        if p_distance < closest_point_distance:
            closest_point_distance = p_distance
            closest_point_index = i
    return closest_point_index, norm_pts_rot[closest_point_index]


def calc_dist(p_curr, p_rot, foe, tZ):
    # print("data")
    # print('p_curr', p_curr)
    # print('p_rot', p_rot)
    # print('foe', foe)
    # print('tZ', tZ)
    # calculate the distance of p_curr using x_curr, x_rot, foe_x and tZ
    distance_by_x = abs(tZ*(foe[0] - p_rot[0]) / (p_curr[0] - p_rot[0]))
    # print('distance by x ', distance_by_x, abs(tZ*(foe[0] - p_rot[0])), abs((p_curr[0] - p_rot[0])))
    # calculate the distance of p_curr using y_curr, y_rot, foe_y and tZ
    distance_by_y = abs(tZ * (foe[1] - p_rot[1]) / (p_curr[1] - p_rot[1]))
    # print('distance by y ', distance_by_y)
    # print("===========\n")
    # combine the two estimations and return estimated Z
    return (distance_by_x + distance_by_y) / 2
