import os
import subprocess
import time
import matplotlib.pyplot as plt


def measure_runtime(script_path):
    start_time = time.time()

    try:
        subprocess.run(["python", script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_path}: {e}")
        return None

    end_time = time.time()
    runtime = end_time - start_time
    return runtime


def main():
    root_directory = "./2023/"  # Change this to your desired root directory

    runtimes = {}  # Dictionary to store script filenames and their runtimes

    for root, dirs, files in os.walk(root_directory):
        for file in files:
            if file.endswith(".py"):
                script_path = os.path.join(root, file)
                runtime = measure_runtime(script_path)

                if runtime is not None:
                    runtimes[file] = runtime
                    print(f"Script: {script_path}, Runtime: {runtime:.2f} seconds")

    plot_runtime_bar_chart(runtimes)


def plot_runtime_bar_chart(runtimes):
    names = list(runtimes.keys())
    values = list(runtimes.values())

    plt.figure(figsize=(10, 6))
    bars = plt.bar(names, values, color="green", edgecolor="black")

    for bar in bars:
        yval = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            yval + 0.1,
            f"{yval:.2f} s",
            ha="center",
            va="bottom",
        )

    plt.xlabel("Script Name")
    plt.ylabel("Runtime (seconds)")
    plt.title("Script Runtimes in Subdirectories")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
