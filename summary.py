import os
import matplotlib.pyplot as plt


def count_lines_and_characters(filename):
    with open(filename, "r", encoding="utf-8") as file:
        lines = sum(1 for _ in file)
        file.seek(0)
        characters = sum(len(line) for line in file)

    return lines, characters


def process_directory(directory):
    python_files = [file for file in os.listdir(directory) if file.endswith(".py")]

    file_data_lines = {}
    file_data_characters = {}
    for file in python_files:
        file_path = os.path.join(directory, file)
        lines, characters = count_lines_and_characters(file_path)
        file_data_lines[file] = lines
        file_data_characters[file] = characters

    return file_data_lines, file_data_characters


def plot_subplots(file_data_lines, file_data_characters):
    # Sort by filename (x-axis labels)
    names = sorted(file_data_lines.keys())
    values_lines = [file_data_lines[name] for name in names]
    values_characters = [file_data_characters[name] for name in names]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    bars_lines = ax1.bar(names, values_lines, color="skyblue", edgecolor="black")
    ax1.set_ylabel("Number of Lines")
    ax1.set_title("Lines and Characters of Python Files in Subdirectories")
    ax1.grid(axis="y", linestyle="--", alpha=0.7)

    bars_characters = ax2.bar(
        names, values_characters, color="lightcoral", edgecolor="black"
    )
    ax2.set_xlabel("File Name")
    ax2.set_ylabel("Number of Characters")
    ax2.grid(axis="y", linestyle="--", alpha=0.7)

    for bar in bars_lines:
        yval = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            yval + 0.1,
            round(yval, 2),
            ha="center",
            va="bottom",
        )

    for bar in bars_characters:
        yval = bar.get_height()
        ax2.text(
            bar.get_x() + bar.get_width() / 2,
            yval + 0.1,
            round(yval, 2),
            ha="center",
            va="bottom",
        )

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("summary.png")
    plt.show()


def main():
    root_directory = "./2025/"  # Change this to your desired root directory

    file_data_lines = {}
    file_data_characters = {}
    for root, dirs, files in os.walk(root_directory):
        for file in files:
            if file.endswith(".py") or file.endswith(".cpp"):
                file_path = os.path.join(root, file)
                lines, characters = count_lines_and_characters(file_path)
                file_data_lines[file] = lines
                file_data_characters[file] = characters

    plot_subplots(file_data_lines, file_data_characters)


if __name__ == "__main__":
    main()
