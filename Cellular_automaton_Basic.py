import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class CellularAutomatonBasic:
    '''construcor, create 2d grid'''
    def __init__(self):
        self.height = 100
        self.width = 100
        self.max_generations = 250  # Number of generations to simulate
        self.pause_time = 0.2 # Pause time between generations (for visualization)
        
    def initialize_automaton(self, height=100, width=100, percentage=50):
        """
        Initialize the grid with random 0s and 1s.

        Parameters: height (int),width (int), percentage (int): Probability that the cell is 1
    
        Returns: df (np.ndarray): Initialized grid generation (int): Starting generation number
        """        
        probability = percentage / 100
        df = np.random.choice([1, 0], size=(height, width), p=[probability, 1-probability])
        generation = 1
        return df, generation

    def automaton_logic(self, df, i, j):
        """
        automaton rules to a 2x2 block starting at (i, j).
        Rules depend on the number of 1s in the block.
        Parameters:df (np.ndarray): Grid, i (int): Row index, j (int): Column index
        """
        if i+1 >= len(df) or j+1 >= len(df[0]):
            return  # Avoid index out of bounds
        # count the number of ones in the block
        count_ones = df[i, j] + df[i, j+1] + df[i+1, j] + df[i+1, j+1]
        
        if count_ones == 2:
            pass  # Continue without changes
        elif count_ones in (0, 1, 4):
            # Flip all bits in the 2x2 block
            df[i, j] = (df[i, j] + 1) % 2
            df[i, j+1] = (df[i, j+1] + 1) % 2
            df[i+1, j] = (df[i+1, j] + 1) % 2
            df[i+1, j+1] = (df[i+1, j+1] + 1) % 2
        elif count_ones == 3:
            # Flip all bits and then swap diagonally
            df[i, j] = (df[i, j] + 1) % 2
            df[i, j+1] = (df[i, j+1] + 1) % 2
            df[i+1, j] = (df[i+1, j] + 1) % 2
            df[i+1, j+1] = (df[i+1, j+1] + 1) % 2
            
            # Swap diagonals
            df[i, j], df[i+1, j+1] = df[i+1, j+1], df[i, j]
            df[i+1, j], df[i, j+1] = df[i, j+1], df[i+1, j]

    def automaton_logic_wrapped(self, df, i, j):
        """
        Apply automaton rules to a 2x2 block, wrapping around the edges.
        
        Parameters: df (np.ndarray): Grid, i (int): Row index, j (int): Column index
        """        
        height, width = df.shape
        
        # Get the wrapped indices for the 2x2 block
        i1, i2 = i % height, (i + 1) % height
        j1, j2 = j % width, (j + 1) % width
        
        count_ones = df[i1, j1] + df[i1, j2] + df[i2, j1] + df[i2, j2]
        
        if count_ones == 2:
            pass  # Continue without changes
        elif count_ones in (0, 1, 4):
            # Flip all bits in the 2x2 block
            df[i1, j1] = (df[i1, j1] + 1) % 2
            df[i1, j2] = (df[i1, j2] + 1) % 2
            df[i2, j1] = (df[i2, j1] + 1) % 2
            df[i2, j2] = (df[i2, j2] + 1) % 2
        elif count_ones == 3:
            # Flip all bits and then swap diagonally
            df[i1, j1] = (df[i1, j1] + 1) % 2
            df[i1, j2] = (df[i1, j2] + 1) % 2
            df[i2, j1] = (df[i2, j1] + 1) % 2
            df[i2, j2] = (df[i2, j2] + 1) % 2
            
            # Swap diagonals
            df[i1, j1], df[i2, j2] = df[i2, j2], df[i1, j1]
            df[i2, j1], df[i1, j2] = df[i1, j2], df[i2, j1]


    def odd_gen(self, df):
        """
        Appling rules to odd genertion.
        Parameters: df (np.ndarray): Grid
        """
        height, width = df.shape
        for i in range(0, height-1, 2):
            for j in range(0, width-1, 2):
                self.automaton_logic(df, i, j)

    def even_gen(self, df, wrap_around):
        """
        Appling rules to even genertion.
        Parameters: df (np.ndarray): Grid, wrap_around (bool): Whether to apply wrap-around logic at borders
        """
        height, width = df.shape
        for i in range(1, height-1, 2):
            for j in range(1, width-1, 2):
                self.automaton_logic(df, i, j)
        if wrap_around:
            i = height - 1
            for j in range(1, width-1, 2):
                self.automaton_logic_wrapped(df, i, j)
                
            # Handle right-left wrapping
            j = width - 1
            for i in range(1, height-1, 2):
                self.automaton_logic_wrapped(df, i, j)
                
            # Handle corner wrapping (bottom-right corner)
            self.automaton_logic_wrapped(df, height-1, width-1)

    def display_automaton(self, df, generation, fig, ax, img, pause_time=0.5):
        """
        Visualize the current generation of the automaton.

        Parameters:
            df (np.ndarray): Grid, generation (int), fig (matplotlib.figure.Figure)
            ax (matplotlib.axes.Axes): Axes object, img (AxesImage): Image object for updates
            pause_time (float): Pause time between frames
        
        Returns:
            tuple: Updated image object for animation
        """
        ax.clear()
        img = ax.imshow(df, cmap='binary', vmin=0, vmax=1)
        ax.set_title(f'Generation: {generation}')
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Force the figure to update
        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.pause(pause_time)
        return img,

    def get_user_choice(self):
        """
        Get from user initial percentage of black (1) cells.
        
        Returns:
            int: Percentage (25, 50, or 75)
        """
        print("\nChoose the initial percentage of black cells:")
        print("a: 25% black cells")
        print("b: 50% black cells")
        print("c: 75% black cells")
        
        while True:
            choice = input().lower()
            if choice == 'a':
                return 25
            elif choice == 'b':
                return 50
            elif choice == 'c':
                return 75
            else:
                print("Invalid choice. Please enter a, b, or c.")

    def automatkind(self):
        """
        Get from user if the automat is wrap-around.
        
        Returns:
            bool: True if wrap-around, False otherwise
        """
        print("\nChoose kind of automat:")
        print("a: no wrap-around")
        print("b: wrap-around")
        while True:
            choice = input().lower()
            if choice == 'a':
                return False
            elif choice == 'b':
                return True
            else:
                print("Invalid choice. Please enter a, b")

    def run(self):
        """
        Run the basic cellular automaton simulation
        """
        height, width = self.height, self.width
        wrap_around = self.automatkind()
        
        # Get user choice for initial percentage
        percentage = self.get_user_choice()
        print(f"Initializing with {percentage}% black cells...")
        
        df, generation = self.initialize_automaton(height, width, percentage)
        
        # Set up the plot for visualization
        fig, ax = plt.subplots()
        img = ax.imshow(df, cmap='binary')  # binary colormap: 0=white, 1=black
        # Remove axis numbers/ticks
        ax.set_xticks([])
        ax.set_yticks([])
        
        max_generations = self.max_generations
        pause_time = self.pause_time  # Time in seconds to display each generation
        
        for i in range(max_generations):
            if generation % 2 == 1:
                self.odd_gen(df)  # Changes happen in-place
            else:
                self.even_gen(df, wrap_around)  # Changes happen in-place
        
            # Update visualization
            self.display_automaton(df, generation, fig, ax, img, pause_time)
            generation += 1

        plt.draw()
        plt.pause(3)  # Wait for 3 seconds
        plt.close(fig)

# For standalone execution
if __name__ == "__main__":
    basic_automaton = CellularAutomatonBasic()
    basic_automaton.run()
