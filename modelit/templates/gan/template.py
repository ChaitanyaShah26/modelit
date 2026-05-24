# =========================================================
# GENERATIVE ADVERSARIAL NETWORK (GAN) FOR 2D DISTRIBUTION
# Learning the y = -x Manifold from Scratch
# Built using PyTorch
# =========================================================


# =========================================================
# IMPORTS
# =========================================================

import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt


# =========================================================
# HYPERPARAMETERS & DEVICE CONFIGURATION
# =========================================================

batch_size = 128

noise_dim = 2

lr = 0.0002

epochs = 2000

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# =========================================================
# DATA GENERATION FUNCTION (REAL DISTRIBUTION)
# =========================================================

def get_real_samples(batch_size):

    x = torch.randn(batch_size, 1)

    y = -x

    data = torch.cat([x, y], dim=1)

    return data.to(device)


# =========================================================
# GENERATOR ARCHITECTURE
# =========================================================

class Generator(nn.Module):

    def __init__(self):

        super().__init__()

        self.model = nn.Sequential(

            nn.Linear(noise_dim, 16),

            nn.ReLU(),

            nn.Linear(16, 16),

            nn.ReLU(),

            nn.Linear(16, 2)

        )


    def forward(self, z):

        return self.model(z)


# =========================================================
# DISCRIMINATOR ARCHITECTURE
# =========================================================

class Discriminator(nn.Module):

    def __init__(self):

        super().__init__()

        self.model = nn.Sequential(

            nn.Linear(2, 16),

            nn.ReLU(),

            nn.Linear(16, 16),

            nn.ReLU(),

            nn.Linear(16, 1),

            nn.Sigmoid()

        )


    def forward(self, x):

        return self.model(x)


# =========================================================
# MODEL INITIALIZATION & OPTIMIZERS
# =========================================================

G = Generator().to(device)

D = Discriminator().to(device)

criterion = nn.BCELoss()

optimizer_G = optim.Adam(G.parameters(), lr=lr)

optimizer_D = optim.Adam(D.parameters(), lr=lr)


# =========================================================
# GAN TRAINING LOOP
# =========================================================

print("\n=================================================")
print("TRAINING GENERATIVE ADVERSARIAL NETWORK")
print("=================================================")

for epoch in range(epochs):


    # =========================================================
    # TRAIN DISCRIMINATOR
    # =========================================================

    real_data = get_real_samples(batch_size)

    real_labels = torch.ones(batch_size, 1).to(device)

    noise = torch.randn(batch_size, noise_dim).to(device)

    fake_data = G(noise)

    fake_labels = torch.zeros(batch_size, 1).to(device)

    real_preds = D(real_data)

    fake_preds = D(fake_data.detach())

    loss_real = criterion(real_preds, real_labels)

    loss_fake = criterion(fake_preds, fake_labels)

    loss_D = loss_real + loss_fake

    optimizer_D.zero_grad()

    loss_D.backward()

    optimizer_D.step()


    # =========================================================
    # TRAIN GENERATOR
    # =========================================================

    noise = torch.randn(batch_size, noise_dim).to(device)

    fake_data = G(noise)

    fake_preds = D(fake_data)

    loss_G = criterion(fake_preds, real_labels)

    optimizer_G.zero_grad()

    loss_G.backward()

    optimizer_G.step()


    # =========================================================
    # PROGRESS LOGGING
    # =========================================================

    if epoch % 200 == 0:

        print(f"Epoch {epoch:04d} | D Loss: {loss_D.item():.4f} | G Loss: {loss_G.item():.4f}")


print("\nGAN Training Complete.")


# =========================================================
# EVALUATION & IMAGE GENERATION
# =========================================================

noise = torch.randn(1000, noise_dim).to(device)

generated = G(noise).detach().cpu()

real = get_real_samples(1000).cpu()


# =========================================================
# VISUALIZATION
# =========================================================

plt.figure(figsize=(6, 6))

plt.scatter(
    real[:, 0], 
    real[:, 1], 
    label="Real (y=-x)", 
    alpha=0.5
)

plt.scatter(
    generated[:, 0], 
    generated[:, 1], 
    label="Generated", 
    alpha=0.5
)

plt.legend()

plt.title("GAN Learning y = -x Distribution")

plt.show()