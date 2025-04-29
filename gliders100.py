import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class GlidersAutomaton:
    def __init__(self):
        self.height = 100
        self.width = 100
        self.max_generations = 250
        self.pause_time = 0.05
    
    def initialize_central_random_area(self, height=100, width=100, size_ratio=0.3, probability=0.5):
        """
        Initialize grid with random cells in the center 
        
        Parameters:
        - height, width: dimensions of the matrix
        - size_ratio: ratio of the center area to the whole grid
        - probability: probability of a cell being alive
        """
        df = np.zeros((height, width))
        
        # Calculate center area size
        center_size_h = int(height * size_ratio)
        center_size_w = int(width * size_ratio)
        start_h = (height - center_size_h) // 2
        start_w = (width - center_size_w) // 2
        
        # Fill center with random values
        df[start_h:start_h+center_size_h, start_w:start_w+center_size_w] = np.random.choice(
            [0, 1], 
            size=(center_size_h, center_size_w), 
            p=[1-probability, probability]
        )
        
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
        df_copy = df.copy()
        
        for i in range(0, height-1, 2):
            for j in range(0, width-1, 2):
                self.automaton_logic(df_copy, i, j)
        
        df[:] = df_copy[:]

    def even_gen(self, df, wrap_around):
        """ 
        Appling rules to even genertion.
        Parameters: df (np.ndarray): Grid, wrap_around (bool): Whether to apply wrap-around logic at borders
        """
        height, width = df.shape
        df_copy = df.copy()
        
        for i in range(1, height-1, 2):
            for j in range(1, width-1, 2):
                self.automaton_logic(df_copy, i, j)
                
        if wrap_around:
            i = height - 1
            for j in range(1, width-1, 2):
                self.automaton_logic_wrapped(df_copy, i, j)
                
            # Handle right-left wrapping
            j = width - 1
            for i in range(1, height-1, 2):
                self.automaton_logic_wrapped(df_copy, i, j)
                
            # Handle corner wrapping (bottom-right corner)
            self.automaton_logic_wrapped(df_copy, height-1, width-1)
        
        df[:] = df_copy[:]

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
        """Run the gliders cellular automaton simulation"""
        height, width = self.height, self.width
        wrap_around = self.automatkind()
        
        # Initialize with a central random area 
        df, generation = self.initialize_central_random_area(
            height, 
            width, 
            size_ratio=0.3,  # Size of the central random area
            probability=0.6   # Slightly higher chance of live cells
        )
        
        # Set up the plot for visualization
        fig, ax = plt.subplots(figsize=(10, 10))
        img = ax.imshow(df, cmap='binary')
        ax.set_xticks([])
        ax.set_yticks([])
        
        max_generations = self.max_generations
        pause_time = self.pause_time  
        
        for i in range(max_generations):
            if generation % 2 == 1:
                self.odd_gen(df)
            else:
                self.even_gen(df, wrap_around)
            generation += 1
            
            # Update visualization
            self.display_automaton(df, generation, fig, ax, img, pause_time)
        
        plt.draw()
        plt.pause(3)
        plt.close(fig)

# For standalone execution
if __name__ == "__main__":
    gliders_automaton = GlidersAutomaton()
    gliders_automaton.run()