def record_data(filepath, score):
    with open(filepath, mode="a") as f:
        f.write(score)
        f.write("\n")