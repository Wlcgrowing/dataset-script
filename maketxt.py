
import os


def maketxt(path):
        with open('./small.txt','w') as f:
            for file in os.listdir(path):
                    pic='./grip/'+file
                    f.write(str(pic))
                    f.write('\n')    

if __name__ == "__main__":
    path = './grip'
    maketxt(path)
