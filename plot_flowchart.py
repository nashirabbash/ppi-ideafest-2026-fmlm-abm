"""
Publication-ready Flowchart Generator for ABM Simulation Workflow (Subbab 3.1).
Outputs high-resolution (300 DPI) PNG figure for KTI Paper.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_abm_flowchart():
    out_dir = "/home/broo/Documents/lomba/PPI/.scratch/cooperative-maas-fmlm-kti/simulation/plots"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "fig0_abm_flowchart.png")

    fig, ax = plt.subplots(figsize=(9, 10), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis("off")

    steps = [
        ("Langkah 1: Inisialisasi Parametrik", "Koridor 8,5 km, 12 Halte, Hub Stasiun KRL\n(Random Seed = 42 for 100% Reproducibility)", "#e6f2ff", "#0066cc"),
        ("Langkah 2: Generasi Kedatangan Komuter", "Non-Homogeneous Poisson Process with Surge Spikes\n(Pulsed Arrivals Peak: 120 pax/jam)", "#e6ffe6", "#009933"),
        ("Langkah 3: Simulasi Agen & Decision Rules", "Pergerakan 50 Driver Agents & Evaluasi Utility RUM U_{i,t}\n(Headway Compliance & Revenue Floor)", "#fff2e6", "#cc6600"),
        ("Langkah 4: Evaluasi Anti-Gaming Penalty", "Pemeriksaan Telemetri Dwell Time (τ > τ_max)\nP_gaming = α · (τ - τ_max)²", "#ffe6e6", "#cc0000"),
        ("Langkah 5: Eksekusi Monte Carlo Runs", "500 Total Runs (125 Runs x 4 Treatment Arms)\nArm A (Baseline), Arm B (Flat), Arm C (Unprotected), Arm D (Unified)", "#f2e6ff", "#6600cc"),
        ("Langkah 6: Evaluasi Statistik SAP", "Uji Shapiro-Wilk, One-Way ANOVA & Tukey-Kramer,\nKruskal-Wallis & Dunn's Post-Hoc Test (α = 0,05)", "#e6f9ff", "#0088cc")
    ]

    y_start = 10.5
    box_height = 1.2
    box_width = 8.4
    x_center = 5.0
    spacing = 0.55

    for i, (title, desc, bg_color, border_color) in enumerate(steps):
        y_top = y_start - i * (box_height + spacing)
        
        # Draw Box Shadow & Main Rounded Box
        rect_shadow = patches.FancyBboxPatch(
            (x_center - box_width/2 + 0.08, y_top - box_height - 0.06), box_width, box_height,
            boxstyle="round,pad=0.15,rounding_size=0.15",
            facecolor="#d9d9d9", edgecolor="none", zorder=1
        )
        ax.add_patch(rect_shadow)

        rect = patches.FancyBboxPatch(
            (x_center - box_width/2, y_top - box_height), box_width, box_height,
            boxstyle="round,pad=0.15,rounding_size=0.15",
            facecolor=bg_color, edgecolor=border_color, linewidth=2.0, zorder=2
        )
        ax.add_patch(rect)

        # Title text
        ax.text(x_center, y_top - 0.3, title, ha="center", va="center", fontsize=11, fontweight="bold", color=border_color, zorder=3)
        # Description text
        ax.text(x_center, y_top - 0.75, desc, ha="center", va="center", fontsize=9.5, color="#222222", zorder=3)

        # Draw connecting arrow to next step
        if i < len(steps) - 1:
            arrow_y_start = y_top - box_height - 0.1
            arrow_y_end = arrow_y_start - spacing + 0.15
            ax.annotate(
                "", xy=(x_center, arrow_y_end), xytext=(x_center, arrow_y_start),
                arrowprops=dict(arrowstyle="->", color="#444444", lw=2.5, mutation_scale=18),
                zorder=4
            )

    plt.title("Gambar 3.1: Alur Metodologi Simulasi Komputasi Agent-Based Model (ABM)", fontsize=13, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(out_file, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"[✓] ABM Flowchart saved to: {out_file}")

if __name__ == "__main__":
    generate_abm_flowchart()
