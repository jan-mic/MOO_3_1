import methods
import interface


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # print(f'Method 1: {method_1.result}')
    root = interface.tk.Tk()
    app = interface.TableEditor(root)
    root.mainloop()

