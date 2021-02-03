from wf_receiver import receiver_run
import sys

args = sys.argv

def main():
    # 第一引数: 入力波形の周波数, 第二引数: トリガーレベル
    #receiver_run(1000000,2.0)
    print(args)
    if len(args) != 1:
        receiver_run(int(args[1]),int(args[2]))
        return 
    receiver_run(500000,2.0)

if __name__ == "__main__":
    main()
    
