import sys
import veux
from Example5 import create_model, analyze

if __name__ == "__main__":

    model = create_model()
    analyze(model)

    # Plot the deformed state of the structure

    artist = veux.render(model, vertical=3, show={"frame.surface"})
    artist = veux.render(model, model.nodeDisp, vertical=3, canvas=artist.canvas)

    # Check the number of arguments that were passed when this
    # script was invoked on the command line.
    if len(sys.argv) > 1:
        print(f"Saving to {sys.argv[1]}")
        artist.save(sys.argv[1])
    else:
        veux.serve(artist)

