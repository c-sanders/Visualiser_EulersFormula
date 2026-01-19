import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 1. Define the range for the angle (x or theta)
# We'll plot several full rotations (e.g., 4*pi) to clearly show the helix
theta = np.linspace(0, 4 * np.pi, 500)

zero  = np.linspace(0, 0, 500)

# 2. Apply Euler's formula: e^(i*theta) = cos(theta) + i*sin(theta)
# The real part corresponds to the x-coordinate
# x = np.cos(theta)

# The imaginary part corresponds to the y-coordinate
# y = np.sin(theta)

# The angle itself will be the z-coordinate
# z = theta

x = theta
y = np.cos(theta)
z = np.sin(theta)

# 3. Create the 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 4. Plot the helix

print("Number of elements in x = ", len(x))
print("Number of elements in y = ", len(y))
print("Number of elements in z = ", len(z))

print("Number of elements in x = ", x.shape)
print("Number of elements in y = ", y.shape)
print("Number of elements in z = ", z.shape)

ax.plot(x,    y, 0, label='y = cos(x)', color='red')
ax.plot(x, zero, z, label='z = isin(x)', color='green')
ax.plot(x,    y, z, label='e^(ix) = cos(x) + isin(x)', color='blue')

for i in range(0, 500, 5) :

    x_axis = [x[i], x[i]]  # Start and end x values for co-ordinate triplets
    y_axis = [0,    y[i]]  # Start and end y values for co-ordinate triplets
    z_axis = [0,    z[i]]  # Start and end z values for co-ordinate triplets

    ax.plot(x_axis, y_axis, 0, color='red')
    ax.plot(x_axis, [0,0], z_axis, color='green')
    ax.plot(x_axis, y_axis, z_axis, color='blue')

# 5. Customize the plot
ax.set_xlabel('Real Axis (cos(theta))')
ax.set_ylabel('Imaginary Axis (sin(theta))')
ax.set_zlabel('Angle (theta) in Radians')
ax.set_title("3D Plot of Euler's Formula (The Complex Helix)")
ax.legend()
ax.grid(True)

elevation = 45
azimuth   = 0

while (azimuth <= 360) :

    # Optional: Adjust the viewing angle for better perspective

    ax.view_init(elev=45, azim = azimuth + 180)

    string_base      = "base = 2.718"
    string_azimuth   = "azimuth = "   + str(azimuth)
    string_elevation = "elevation = " + str(elevation)

    custom_metadata = {
        "Keywords" : [string_base, string_azimuth, string_elevation]
    }

    filename = "Eulers_formula_(" + str(elevation) + "," + str(azimuth) + ").svg"

    print("Filename = ", filename)

    plt.savefig(
       filename,
        format="svg",
        metadata=custom_metadata)

    # 6. Display the plot
    # plt.show()

    azimuth = azimuth + 1
