from imports_file import *

print("Python version")
print (sys.version)


if __name__ == "__main__":

    globals.root = tk.Tk()
    stop_threads = False
    t1 = threading.Thread(target=MainClass, args=[], daemon=True)
    t1.start()
    globals.robot_gui = GUI(globals.root)
    globals.root.mainloop()
    sys.exit()

