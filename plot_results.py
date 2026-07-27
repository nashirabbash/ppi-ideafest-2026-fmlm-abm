"""
Publication-ready plotting script for ABM simulation results.
Generates 5 figures for Bab 4 (Hasil dan Pembahasan) of the KTI paper.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import config

# Global Plotting Options for High-Quality Academic Figures
plt.style.use('seaborn-v0_8-paper' if 'seaborn-v0_8-paper' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 9.5
plt.rcParams['ytick.labelsize'] = 9.5
plt.rcParams['legend.fontsize'] = 9.5
plt.rcParams['figure.titlesize'] = 13

PALETTE = {
    "Arm_A": "#d95f02",  # Orange (Baseline)
    "Arm_B": "#7570b3",  # Purple (Gross BTS)
    "Arm_C": "#e7298a",  # Pink (Unprotected Flexible)
    "Arm_D": "#1b9e77"   # Teal Green (Proposed Unified Framework)
}

ARM_LABELS = {
    "Arm_A": "Arm A: Baseline Setoran",
    "Arm_B": "Arm B: Gross BTS Kaku",
    "Arm_C": "Arm C: Unprotected Dispatch",
    "Arm_D": "Arm D: Unified Framework"
}

def load_data():
    csv_path = os.path.join(config.RESULTS_DIR, "simulation_results.csv")
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Results CSV not found at {csv_path}. Please run run_simulation.py first.")
    df = pd.read_csv(csv_path)
    df["arm_label"] = df["arm"].map(ARM_LABELS)
    return df


def plot_fig1_headway_cv(df):
    """Figure 1: Headway Coefficient of Variation (CV_headway) Comparison."""
    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=300)

    sns.boxplot(
        data=df, x="arm_label", y="cv_headway", palette=[PALETTE[a] for a in config.TREATMENT_ARMS.keys()],
        ax=ax, width=0.45, boxprops=dict(alpha=0.85)
    )

    # Threshold target line (CV <= 0.18)
    ax.axhline(0.18, color='red', linestyle='--', linewidth=1.5, label='HCM 7th Target (CV ≤ 0.18)')

    ax.set_title("Gambar 4.1: Perbandingan Stabilitas Headway (CV_headway) antar Skenario", pad=12, fontweight='bold')
    ax.set_xlabel("Skenario Operasional Feeder", labelpad=8)
    ax.set_ylabel("Headway CV (σ_H / μ_H)", labelpad=8)
    ax.set_ylim(0.05, 0.45)
    ax.legend(loc='upper right', frameon=True)
    ax.grid(True, linestyle=':', alpha=0.6)

    plt.tight_layout()
    out_file = os.path.join(config.PLOTS_DIR, "fig1_headway_cv_comparison.png")
    plt.savefig(out_file)
    plt.close()
    print(f"[✓] Figure 1 saved to: {out_file}")


def plot_fig2_ewt_distribution(df):
    """Figure 2: Excess Passenger Waiting Time (EWT) Distribution."""
    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=300)

    for arm_key in config.TREATMENT_ARMS.keys():
        sub_df = df[df["arm"] == arm_key]
        sns.kdeplot(
            data=sub_df["ewt_min"], ax=ax, label=ARM_LABELS[arm_key],
            color=PALETTE[arm_key], linewidth=2.0, fill=True, alpha=0.15
        )

    ax.set_title("Gambar 4.2: Distribusi Densitas Excess Passenger Waiting Time (EWT)", pad=12, fontweight='bold')
    ax.set_xlabel("Excess Waiting Time / EWT (menit)", labelpad=8)
    ax.set_ylabel("Kerapatan Probabilitas (Density)", labelpad=8)
    ax.legend(loc='upper right', frameon=True)
    ax.grid(True, linestyle=':', alpha=0.6)

    plt.tight_layout()
    out_file = os.path.join(config.PLOTS_DIR, "fig2_ewt_distribution.png")
    plt.savefig(out_file)
    plt.close()
    print(f"[✓] Figure 2 saved to: {out_file}")


def plot_fig3_farebox_recovery_ratio(df):
    """Figure 3: Farebox Recovery Ratio (FRR) Comparison."""
    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=300)

    sns.barplot(
        data=df, x="arm_label", y="frr", palette=[PALETTE[a] for a in config.TREATMENT_ARMS.keys()],
        ax=ax, capsize=0.1, err_kws={'linewidth': 1.5}, alpha=0.9
    )

    # Benchmark FRR = 1.0 (Break-even financial sustainability)
    ax.axhline(1.0, color='darkgreen', linestyle='-.', linewidth=1.5, label='Kemandirian Finansial (FRR ≥ 1.0)')

    ax.set_title("Gambar 4.3: Perbandingan Farebox Recovery Ratio (FRR) dan Kemandirian Finansial", pad=12, fontweight='bold')
    ax.set_xlabel("Skenario Operasional Feeder", labelpad=8)
    ax.set_ylabel("Farebox Recovery Ratio (FRR)", labelpad=8)
    ax.set_ylim(0.0, 1.4)
    ax.legend(loc='upper left', frameon=True)
    ax.grid(True, linestyle=':', alpha=0.6)

    # Annotate values
    means = df.groupby("arm")["frr"].mean()
    for i, arm_key in enumerate(config.TREATMENT_ARMS.keys()):
        val = means[arm_key]
        ax.text(i, val + 0.03, f"{val:.2f}", ha='center', fontweight='bold', fontsize=9.5)

    plt.tight_layout()
    out_file = os.path.join(config.PLOTS_DIR, "fig3_farebox_recovery_ratio.png")
    plt.savefig(out_file)
    plt.close()
    print(f"[✓] Figure 3 saved to: {out_file}")


def plot_fig4_boycott_driver_retention(df):
    """Figure 4: Driver Boycott & Turnover Rate %."""
    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=300)

    sns.barplot(
        data=df, x="arm_label", y="boycott_rate_pct", palette=[PALETTE[a] for a in config.TREATMENT_ARMS.keys()],
        ax=ax, capsize=0.1, err_kws={'linewidth': 1.5}, alpha=0.9
    )

    ax.axhline(0.0, color='blue', linestyle='--', linewidth=1.2, label='Target Mitigasi Boikot (0%)')

    ax.set_title("Gambar 4.4: Tingkat Boikot / Resign Pengemudi Informal (%)", pad=12, fontweight='bold')
    ax.set_xlabel("Skenario Operasional Feeder", labelpad=8)
    ax.set_ylabel("Tingkat Boikot / Turnover (%)", labelpad=8)
    ax.set_ylim(0.0, 25.0)
    ax.legend(loc='upper right', frameon=True)
    ax.grid(True, linestyle=':', alpha=0.6)

    means = df.groupby("arm")["boycott_rate_pct"].mean()
    for i, arm_key in enumerate(config.TREATMENT_ARMS.keys()):
        val = means[arm_key]
        ax.text(i, val + 0.5, f"{val:.1f}%", ha='center', fontweight='bold', fontsize=9.5)

    plt.tight_layout()
    out_file = os.path.join(config.PLOTS_DIR, "fig4_driver_utility_retention.png")
    plt.savefig(out_file)
    plt.close()
    print(f"[✓] Figure 4 saved to: {out_file}")


def plot_fig5_anti_gaming_sensitivity():
    """Figure 5: Anti-Gaming Penalty (P_gaming) Sensitivity Curve."""
    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=300)

    excess_dwell = np.linspace(0.0, 8.0, 100)  # minutes of excess dwelling
    alpha_vals = [0.5, 1.5, 3.0]

    for alpha in alpha_vals:
        p_gaming = alpha * (excess_dwell ** 2)
        ax.plot(excess_dwell, p_gaming, linewidth=2.0, label=f'Penalti α = {alpha}')

    ax.set_title("Gambar 4.5: Kurva Sensitivitas Penalti Telemetri Anti-Gaming (P_gaming)", pad=12, fontweight='bold')
    ax.set_xlabel("Kelebihan Durasi Ngetem / Excess Dwell Time (τ - τ_max, menit)", labelpad=8)
    ax.set_ylabel("Potongan Skor Penalti P_gaming", labelpad=8)
    ax.legend(loc='upper left', frameon=True)
    ax.grid(True, linestyle=':', alpha=0.6)

    plt.tight_layout()
    out_file = os.path.join(config.PLOTS_DIR, "fig5_anti_gaming_penalty_sensitivity.png")
    plt.savefig(out_file)
    plt.close()
    print(f"[✓] Figure 5 saved to: {out_file}")


def generate_all_plots():
    print("================================================================================")
    print("GENERATING PUBLICATION-READY FIGURES FOR KTI PAPER (BAB 4)")
    print("================================================================================")
    df = load_data()
    plot_fig1_headway_cv(df)
    plot_fig2_ewt_distribution(df)
    plot_fig3_farebox_recovery_ratio(df)
    plot_fig4_boycott_driver_retention(df)
    plot_fig5_anti_gaming_sensitivity()
    print("\n[✓] ALL 5 FIGURES GENERATED SUCCESSFULLY!")


if __name__ == "__main__":
    generate_all_plots()
