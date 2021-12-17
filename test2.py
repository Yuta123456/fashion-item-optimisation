import glob

dir_pathes = glob.glob('../images/RichWearImageSprited/**/**/')[800:2000]
for p in dir_pathes:    
    with open("new_dir_path.txt", mode="a") as f:
        f.write(p + "\n")
