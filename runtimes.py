import os
import subprocess
import time
import statistics
import matplotlib.pyplot as plt


def measure_runtime(script_path, runs=10):
    runtimes = []

    for _ in range(runs):
        start_time = time.time()

        try:
            subprocess.run(["python", script_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running {script_path}: {e}")
            return None

        end_time = time.time()
        runtime = end_time - start_time
        runtimes.append(runtime)

    return runtimes


def main():
    root_directory = "./2022/"  # Change this to your desired root directory
    runs = 2  # Number of times to run each script

    all_runtimes = {}  # Dictionary to store script filenames and their runtimes

    for root, dirs, files in os.walk(root_directory):
        for file in files:
            if file.endswith(".py"):
                script_path = os.path.join(root, file)
                runtimes = measure_runtime(script_path, runs)

                if runtimes is not None:
                    all_runtimes[file] = runtimes
                    print(f"Script: {script_path}, Runtimes: {runtimes}")

    plot_mean_runtime_bar_chart(all_runtimes)


def plot_mean_runtime_bar_chart(all_runtimes):
    means = {
        script: statistics.mean(runtimes) for script, runtimes in all_runtimes.items()
    }
    std_devs = {
        script: statistics.stdev(runtimes) for script, runtimes in all_runtimes.items()
    }

    names = list(means.keys())
    values = list(means.values())
    std_dev_values = [std_devs[name] for name in names]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(
        names, values, color="orange", edgecolor="black", yerr=std_dev_values, capsize=5
    )

    for name, bar, std_dev in zip(names, bars, std_dev_values):
        yval = bar.get_height()
        # plt.text(
        #    bar.get_x() + bar.get_width() / 2,
        #    yval + 0.01,
        #    f"{yval:.3f}",
        #    ha="center",
        #    va="bottom",
        # )
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            yval + 0.01 + std_dev,
            f"{means[name]:.2f} s",
            ha="center",
            va="bottom",
        )

    plt.xlabel("Script Name")
    plt.ylabel("Mean Runtime (seconds)")
    plt.title(
        f"Mean Runtimes with Standard Deviation (averaged over {len(all_runtimes[next(iter(all_runtimes))])} runs)"
    )
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
