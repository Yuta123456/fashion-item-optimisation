filepath = "./data/sim.txt"
new_file_path = "./data/sim_new.txt"
with open(filepath,encoding='utf-8')as f:
    lines = f.readlines()
    # tensor(479.4646)
    lines = list(map(lambda x: x[7:-2], lines))
    # print(lines)
with open(new_file_path, mode='a') as f:
    f.writelines("\n".join(lines))
