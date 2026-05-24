# =========================================================
# DENOISING DIFFUSION PROBABILISTIC MODEL (DDPM)
# Learning the y = -x Manifold via Reverse Diffusion
# Built using PyTorch
# =========================================================


# =========================================================
# IMPORTS
# =========================================================

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt


# =========================================================
# DATA GENERATION FUNCTION (REAL MANIFOLD)
# =========================================================

def sample_line_data(n_samples=512):

    x = torch.empty(n_samples, 1).uniform_(-4.5, 4.5)

    y = -x

    return torch.cat([x, y], dim=1)


# =========================================================
# DIFFUSION HYPERPARAMETERS & SCHEDULING
# =========================================================

steps = 120

betas = torch.linspace(2e-4, 0.015, steps)

alphas = 1.0 - betas

alpha_cum = torch.cumprod(alphas, dim=0)


# =========================================================
# FORWARD DIFFUSION PROCESS (NOISING)
# =========================================================

def diffuse(x0, t_idx):

    noise = torch.randn_like(x0)

    a_bar = alpha_cum[t_idx].view(-1, 1)

    x_t = torch.sqrt(a_bar) * x0 + torch.sqrt(1 - a_bar) * noise

    return x_t, noise


# =========================================================
# NOISE ESTIMATOR NETWORK (MLP WITH TIME EMBEDDING)
# =========================================================

class NoiseEstimator(nn.Module):

    def __init__(self, dim=2, hidden=128):

        super().__init__()

        self.mlp = nn.Sequential(

            nn.Linear(dim + 16, hidden),

            nn.SiLU(),

            nn.Linear(hidden, hidden),

            nn.SiLU(),

            nn.Linear(hidden, dim)

        )


    def time_embed(self, t):

        half = 8

        freqs = torch.exp(torch.linspace(0, 3, half))

        t = t.float().unsqueeze(1)

        emb = torch.cat(
            [torch.sin(t / freqs), torch.cos(t / freqs)], 
            dim=1
        )

        return emb


    def forward(self, x, t):

        t_emb = self.time_embed(t)

        return self.mlp(torch.cat([x, t_emb], dim=1))


# =========================================================
# INITIALIZATION & CONFIGURATION
# =========================================================

model = NoiseEstimator()

opt = optim.Adam(model.parameters(), lr=2e-3)

loss_fn = nn.L1Loss()

epochs = 1800

batch = 128


# =========================================================
# DIFFUSION MODEL TRAINING LOOP
# =========================================================

print("\n=================================================")
print("TRAINING DENOISING DIFFUSION MODEL")
print("=================================================")

for ep in range(epochs):

    x0 = sample_line_data(batch)

    t = torch.randint(0, steps, (batch,))

    xt, eps = diffuse(x0, t)

    eps_hat = model(xt, t)

    loss = loss_fn(eps_hat, eps)

    opt.zero_grad()

    loss.backward()

    opt.step()


    # =========================================================
    # PROGRESS LOGGING
    # =========================================================

    if ep % 300 == 0:

        print(f"Epoch {ep:04d} | L1 Loss: {loss.item():.5f}")


print("\nDiffusion Training Complete.")


# =========================================================
# REVERSE DIFFUSION PROCESS (GENERATION)
# =========================================================

@torch.no_grad()
def generate(n=800):

    x = torch.randn(n, 2)

    for t in reversed(range(steps)):

        t_batch = torch.full((n,), t)

        eps = model(x, t_batch)

        a = alphas[t]

        a_bar = alpha_cum[t]

        b = betas[t]

        coef1 = 1 / torch.sqrt(a)

        coef2 = (1 - a) / torch.sqrt(1 - a_bar)

        noise = torch.randn_like(x) if t > 0 else 0

        x = coef1 * (x - coef2 * eps) + torch.sqrt(b) * noise

    return x


# =========================================================
# GENERATING SAMPLES FOR EVALUATION
# =========================================================

real = sample_line_data(1000)

fake = generate(1000)


# =========================================================
# VISUALIZATION
# =========================================================

plt.figure(figsize=(6, 6))

plt.scatter(
    real[:, 0], 
    real[:, 1], 
    s=5, 
    alpha=0.4, 
    label="Real data"
)

plt.scatter(
    fake[:, 0], 
    fake[:, 1], 
    s=5, 
    alpha=0.4, 
    label="Generated"
)

plt.legend()

plt.title("Diffusion learns y = -x manifold")

plt.axis("equal")

plt.show()