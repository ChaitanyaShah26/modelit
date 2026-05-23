# =========================================================
# PERCEPTRON LEARNING ALGORITHM
# AND, OR, NAND, NOR using
# 1. Bipolar Representation
# 2. Unipolar Representation
# =========================================================


# =========================================================
# COMMON FUNCTIONS
# =========================================================

def net_input(w, x, b):
    net = 0

    for i in range(len(w)):
        net = net + w[i] * x[i]

    net = net + b

    return net


# =========================================================
# BIPOLAR ACTIVATION FUNCTION
# output:
#  1  if net > 0
#  0  if net = 0
# -1  if net < 0
# =========================================================

def bipolar_activation(net):

    if net > 0:
        return 1

    elif net == 0:
        return 0

    elif net < 0:
        return -1


# =========================================================
# UNIPOLAR ACTIVATION FUNCTION
# output:
# 1 if net >= 0
# 0 if net < 0
# =========================================================

def unipolar_activation(net):

    if net >= 0:
        return 1

    elif net < 0:
        return 0


# =========================================================
# ERROR CALCULATION
# error = desired_output - actual_output
# =========================================================

def calc_error(output, det_output):

    return (det_output - output)


# =========================================================
# CHANGE IN WEIGHT
# Δw = c * e * x
# =========================================================

def delta_w(c, e, x):

    return c * e * x


# =========================================================
# CHANGE IN BIAS
# Δb = c * e
# =========================================================

def delta_b(c, e):

    return c * e


# =========================================================
# UPDATE FUNCTION
# new_value = old_value + delta
# =========================================================

def update(old, delta):

    return old + delta


# =========================================================
# TRAINING FUNCTION
# =========================================================

def train_perceptron(data, activation_type, gate_name):

    print("\n=================================================")
    print(f"{gate_name}")
    print("=================================================")

    w1 = 0
    w2 = 0
    b = 0

    c = 1
    max_epochs = 100

    print(f"\nInitial weights:")
    print(f"w1 = {w1}, w2 = {w2}")
    print(f"Initial Bias:")
    print(f"b = {b}")

    for epoch in range(max_epochs):

        all_errors = []

        print(f"\nEpoch {epoch + 1}:")
        print("x1\tx2\td\tnet\to\te\tdel_w1\tdel_w2\tdel_b\tw1\tw2\tb")

        for i in range(len(data)):

            x = data[i][:2]
            d = data[i][2]

            # Net Input
            net = net_input([w1, w2], x, b)

            # Activation
            if activation_type == "bipolar":
                output = bipolar_activation(net)

            elif activation_type == "unipolar":
                output = unipolar_activation(net)

            # Error
            error = calc_error(output, d)

            all_errors.append(error)

            # Weight Updates
            d_w1 = delta_w(c, error, x[0])
            w1 = update(w1, d_w1)

            d_w2 = delta_w(c, error, x[1])
            w2 = update(w2, d_w2)

            # Bias Update
            d_b = delta_b(c, error)
            b = update(b, d_b)

            print(
                f"{x[0]}\t{x[1]}\t{d}\t{net}\t{output}\t{error}\t"
                f"{d_w1}\t{d_w2}\t{d_b}\t{w1}\t{w2}\t{b}"
            )

        # Stop if all errors are zero
        if all(e == 0 for e in all_errors):
            break

    print(f"\nAll errors zero at epoch {epoch + 1}")

    print("\nFinal weights:")
    print(f"w1 = {w1}, w2 = {w2}")

    print("Final bias:")
    print(f"b = {b}")


# =========================================================
# AND GATE USING BIPOLAR
# =========================================================

X_and_bi = [
    [-1, -1, -1],
    [1, -1, -1],
    [-1, 1, -1],
    [1, 1, 1]
]

train_perceptron(
    X_and_bi,
    activation_type="bipolar",
    gate_name="AND Gate using Bipolar"
)


# =========================================================
# AND GATE USING UNIPOLAR
# =========================================================

X_and_uni = [
    [0, 0, 0],
    [0, 1, 0],
    [1, 0, 0],
    [1, 1, 1]
]

train_perceptron(
    X_and_uni,
    activation_type="unipolar",
    gate_name="AND Gate using Unipolar"
)


# =========================================================
# OR GATE USING BIPOLAR
# =========================================================

X_or_bi = [
    [-1, -1, -1],
    [1, -1, 1],
    [-1, 1, 1],
    [1, 1, 1]
]

train_perceptron(
    X_or_bi,
    activation_type="bipolar",
    gate_name="OR Gate using Bipolar"
)


# =========================================================
# OR GATE USING UNIPOLAR
# =========================================================

X_or_uni = [
    [0, 0, 0],
    [1, 0, 1],
    [0, 1, 1],
    [1, 1, 1]
]

train_perceptron(
    X_or_uni,
    activation_type="unipolar",
    gate_name="OR Gate using Unipolar"
)


# =========================================================
# NAND GATE USING UNIPOLAR
# =========================================================

X_nand_uni = [
    [0, 0, 1],
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0]
]

train_perceptron(
    X_nand_uni,
    activation_type="unipolar",
    gate_name="NAND Gate using Unipolar"
)


# =========================================================
# NOR GATE USING UNIPOLAR
# =========================================================

X_nor_uni = [
    [0, 0, 1],
    [0, 1, 0],
    [1, 0, 0],
    [1, 1, 0]
]

train_perceptron(
    X_nor_uni,
    activation_type="unipolar",
    gate_name="NOR Gate using Unipolar"
)


# =========================================================
# NAND GATE USING BIPOLAR
# =========================================================

X_nand_bi = [
    [-1, -1, 1],
    [-1, 1, 1],
    [1, -1, 1],
    [1, 1, -1]
]

train_perceptron(
    X_nand_bi,
    activation_type="bipolar",
    gate_name="NAND Gate using Bipolar"
)


# =========================================================
# NOR GATE USING BIPOLAR
# =========================================================

X_nor_bi = [
    [-1, -1, 1],
    [-1, 1, -1],
    [1, -1, -1],
    [1, 1, -1]
]

train_perceptron(
    X_nor_bi,
    activation_type="bipolar",
    gate_name="NOR Gate using Bipolar"
)
