import tkinter as tk
from Layout import Layout

# Main file is only to run the App
class SocialNetworkTool:

    def __init__(self,root):
        self.root = root
        self.root.title("Mini Social Network Tool")
        self.layout = Layout(self.root)
        self.layout.LayoutForm()

if __name__ == "__main__":
    root = tk.Tk()
    app = SocialNetworkTool(root)
    root.mainloop()