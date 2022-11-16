import numpy
import pandas
import seaborn
from pathlib import Path
import matplotlib.pyplot as plt

output = Path("barplots")
output.mkdir(exist_ok=True)

colors = {
    "blue": "#456990",
    "red": "#EC5B60",
    "green": "#41B4A1"
}

def main():
    n = 15
    N = 10

    names = ["healthy", "diseased"]
    probabilities = numpy.asarray([
        [1, 1, 1],
        [1, .1, .1]
    ])
    probabilities /= probabilities.sum(axis=1)[..., numpy.newaxis]

    for i, proba in enumerate(probabilities):
        (output / names[i]).mkdir(exist_ok=True)
        for j in range(N):
            sample = numpy.random.choice(["rood", "groen", "blauw"], size=n, p=proba)

            ax = seaborn.countplot(
                x=sample,
                order=["rood", "groen", "blauw"],
                palette=[colors["red"], colors["green"], colors["blue"]]
            )
            ax.set_xlabel("")
            plt.savefig(str(output / names[i] / f"{j}.png"), bbox_inches="tight")
            plt.close()

if __name__ == "__main__":
    main()