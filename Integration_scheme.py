# Making the integration_scheme
import pickle
from matplotlib import pyplot as plt
from Coordinates import d, Nx, Nz, x_list


def integral(x1, x2, y1, y2):
    # Calculating parameters for linear equation y = ax + b
    a = (y2-y1)/(x2-x1)
    b = y1-((y2-y1)/(x2-x1))*x1

    # Integration scheme for f(x)=ax+b
    int_axb = (a/2)*(x2**2 - x1**2) + b*(x2-x1)
    # should be similar to: (y1 + y2)*(x2 - x1)/2

    # Integration scheme for f(x)=(ax+b)*x
    xh = 0.17679203  # distance from shear center
    int_x_axb = (1/3)*a*(x2**3 - x1**3) + 0.5*(b-a*xh)*(x2**2-x1**2) - b*xh*(x2-x1)

    return int_axb, int_x_axb


'''
def double_integral(x1, x2, y1, y2):
    # Calculating parameters for linear equation y = ax + b
    a = (y2-y1)/(x2-x1)
    b = y1-((y2-y1)/(x2-x1))*x1

    # Integration scheme for f(x)=ax+b
    int_axb_var = (a/6)*(x2**3 - x1**3) + (b/2)*(x2**2-x1**2)
    # should be similar to: (y1 + y2)*(x2 - x1)/2

    return int_axb_var


def triple_integral(x1, x2, y1, y2):
    # Calculating parameters for linear equation y = ax + b
    a = (y2 - y1) / (x2 - x1)
    b = y1 - ((y2 - y1) / (x2 - x1)) * x1

    # Integration scheme for f(x)=ax+b
    int_axb_var = (a / 24) * (x2 ** 4 - x1 ** 4) + (b / 6) * (x2 ** 3 - x1 ** 3)
    # should be similar to: (y1 + y2)*(x2 - x1)/2

    return int_axb_var


def quadruple_integral(x1, x2, y1, y2):
    # Calculating parameters for linear equation y = ax + b
    a = (y2 - y1) / (x2 - x1)
    b = y1 - ((y2 - y1) / (x2 - x1)) * x1

    # Integration scheme for f(x)=ax+b
    int_axb_var = (a / 120) * (x2 ** 5 - x1 ** 5) + (b / 24) * (x2 ** 4 - x1 ** 4)
    # should be similar to: (y1 + y2)*(x2 - x1)/2

    return int_axb_var
'''


def main():
    index = 0
    line_load, torques = [], []

    for i in range(0, Nx):

        load = 0        # kN / m (both variables are integrated once,
        torque = 0      # kN*m /m      they become a 2D representation of the 3D distributed load)

        for j in range(0, Nz-1):

            intaxb, intxaxb = integral(d[index][1], d[index+1][1], d[index][2], d[index+1][2])

            load += intaxb
            torque += intxaxb
            index += 1

        #
        line_load.append(load)         #
        torques.append(-torque)         # Torque becomes negative

    # check if found loads and torques have reasonable numbers
    print("line_load_3: ", line_load[3])
    print("torque on line3: ", torques[3])
    # for total torque calculate sum of found torques ( for torque/Mx)
    # for moment in z- direction integrate the line load once again to obtain the moment
    print("first value: ", x_list[0])
    # print(d[0][1])
    # print(d[1][1])

    # x / dx
    # setting up integral
    # list of X is imported

    def compute_func_list(y_list):
        func_list_ = []
        for q in range(len(x_list) - 1):
            x1 = x_list[q]
            x2 = x_list[q + 1]
            y1 = y_list[q]
            y2 = y_list[q + 1]
            # define a and b
            a = (y2 - y1) / (x2 - x1)
            b = (y1 - a * x1)

            if len(func_list_) != 0:
                var_a, var_b = func_list_[-1]
                c = a - var_a
                new_a = var_a + c
                new_b = var_b - c * x1
                func_list_.append((new_a, new_b))
            else:
                func_list_.append((a, b))

        return func_list_

    func_list = compute_func_list(line_load)
    print(func_list)
    func_list_torque = compute_func_list(torques)

    force, moment, torque = 0, 0, 0
    force_list, moment_list, torque_list = [], [], []

    # steps taken to estimate integral, can be changed
    steps = 500000

    # define length from first known value to last known value (what to do with the unknown part???
    length = x_list[-1] - x_list[0]
    print(x_list[0], x_list[-1])
    print(length)
    # print("length: ", len(x_list))
    step_size = length / steps
    print("step size: ", step_size)
    # define func list
    moment_I, moment_II, torque_I = 0, 0, 0
    moment_II_list, torque_I_list = [], []

    x_step_list = []
    for i in range(steps):
        # first find x in list:
        # x value is step size times i ?? VERIFY
        x_value = step_size * i + x_list[0]
        x_step_list.append(x_value)
        for idx, elem in enumerate(x_list):
            if elem > x_value:
                func_idx = idx - 1
                break
        # x is found, now take the right dist func from func list
        g, h = func_list[func_idx]
        dist = g*x_value + h

        # calculate new force and moment using the current dist func
        # force is basically the term that is needed for Sy
        # moment is Mz
        force = force + dist * step_size
        moment = moment + force * step_size - dist * step_size * step_size / 2
        moment_I += moment * step_size
        moment_II += moment_I * step_size

        # append them to a list
        force_list.append(force)
        moment_list.append(moment)
        moment_II_list.append(moment_II)

        # compute torque integral
        s, t = func_list_torque[func_idx]
        dist2 = s*x_value + t
        # same procedure, f
        torque += dist2 * step_size
        torque_I += torque * step_size
        torque_list.append(torque)
        torque_I_list.append(torque_I)

    filename = 'aeroloading'
    save_object = (force_list, moment_list, torque_list, moment_II_list, torque_I_list, step_size)
    with open(filename, "wb") as f:
        pickle.dump(save_object, f)

    # check values
    print(force_list[0:5])
    print(force_list[-5:-1])
    #
    print(moment_list[0:5])
    print(moment_list[-5:-1])

    ###
    plt.plot(x_step_list, force_list)
    plt.plot(x_step_list, moment_list)
    plt.plot(x_step_list, torque_list)
    plt.plot(x_step_list, torque_I_list)
    plt.plot(x_step_list, moment_II_list)

    # plt.plot(x_list, line_load)
    # plt.plot(x_list, torques)
    plt.legend(labels=['shear force y', 'moment z', 'torque x', 'torque x int', 'moment z int2'])
    # , 'line_load along x', 'line torque along x'])
    plt.xlabel('x')
    plt.ylabel('magnitude')
    plt.show()


main()

