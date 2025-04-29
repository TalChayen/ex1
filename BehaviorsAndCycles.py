import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

def insert_blinker(df, x, y):
    """
    Insert a blinker pattern 
    Pattern size: 3x3
    """
    pattern = np.array([
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
    ])
    df[x:x+3, y:y+3] = pattern

def insert_traffic_light(df, x, y):
    """
    Insert a traffic light pattern 
    Pattern size: 4x4
    """
    pattern = np.array([
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 0],
    ])
    df[x:x+4, y:y+4] = pattern

def insert_small_oscillator(df, x, y):
    """
    Insert a small oscillator pattern 
    Pattern size: 2x2
    """
    pattern = np.array([
        [1, 0],
        [0, 1]
    ])
    df[x:x+2, y:y+2] = pattern

def insert_zigzag_glider(df, x, y):
    """
    Insert an interesting pattern that might produce glider-like behavior (we found it when we tried to find a glider)
    Pattern size: 3x3
    """
    pattern = np.array([
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0],
    ])
    df[x:x+3, y:y+3] = pattern

def insert_plus_shape(df, x, y):
    """
    Insert a plus shape pattern
    Pattern size: 5x5
    """
    pattern = np.array([
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [1, 1, 1, 1, 1],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0]
    ])
    df[x:x+5, y:y+5] = pattern

def insert_square_shape(df, x, y):
    """
    Insert a square shape pattern (creates gliders)
    Pattern size: 5x5
    """
    pattern = np.array([
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1]
    ])
    df[x:x+5, y:y+5] = pattern

def insert_x_shape(df, x, y):
    """
    Insert an X shape pattern
    Pattern size: 5x5
    """
    pattern = np.array([
        [1, 0, 0, 0, 1],
        [0, 1, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 0, 1, 0],
        [1, 0, 0, 0, 1]
    ])
    df[x:x+5, y:y+5] = pattern

def insert_single_cell(df, x, y):
    """
    Insert a single live cell
    Pattern size: 1x1
    """
    df[x, y] = 1

def initialize_automaton(height=100, width=100, pattern_type="blinker"):
    """
    Initialize the automaton with the selected pattern
    
    Parameters:
    - height, width: dimensions of the grid
    - pattern_type: which pattern to include
        "blinker", "traffic_light", "small_oscillator", 
        "zigzag_glider", "plus_shape", 
        "square_shape", "x_shape", "single_cell"
    """
    df = np.zeros((height, width))
    
    if pattern_type == "blinker":
        insert_blinker(df, 25, 25)
        insert_blinker(df, 45, 45)
        insert_blinker(df, 65, 65)
    
    elif pattern_type == "traffic_light":
        insert_traffic_light(df, 25, 25)
        insert_traffic_light(df, 45, 45)
        insert_traffic_light(df, 65, 65)
    
    elif pattern_type == "small_oscillator":
        insert_small_oscillator(df, 25, 25)
        insert_small_oscillator(df, 45, 45)
        insert_small_oscillator(df, 65, 65)
            
    elif pattern_type == "zigzag_glider":
        insert_zigzag_glider(df, 25, 25)
        insert_zigzag_glider(df, 45, 45)
        insert_zigzag_glider(df, 65, 65)
            
    elif pattern_type == "plus_shape":
        insert_plus_shape(df, 25, 25)
        insert_plus_shape(df, 45, 45)
        insert_plus_shape(df, 65, 65)
            
    elif pattern_type == "square_shape":
        insert_square_shape(df, 25, 25)
        insert_square_shape(df, 45, 45)
        insert_square_shape(df, 65, 65)
    
    elif pattern_type == "x_shape":
        insert_x_shape(df, 25, 25)
        insert_x_shape(df, 45, 45)
        insert_x_shape(df, 65, 65)
    
    elif pattern_type == "single_cell":
        insert_single_cell(df, 25, 25)
        insert_single_cell(df, 45, 45)
        insert_single_cell(df, 65, 65)
    
    generation = 1
    return df, generation

def automaton_logic(df, i, j):
    """Apply the automaton rules to a 2x2 block"""
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

def automaton_logic_wrapped(df, i, j):
    """Apply the automaton rules to a 2x2 block with wrapping"""
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

def odd_gen(df):
    """Process odd generations"""
    height, width = df.shape
    df_copy = df.copy()
    
    for i in range(0, height-1, 2):
        for j in range(0, width-1, 2):
            automaton_logic(df_copy, i, j)
    
    df[:] = df_copy[:]

def even_gen(df, wrap_around):
    """Process even generations"""
    height, width = df.shape
    df_copy = df.copy()
    
    for i in range(1, height-1, 2):
        for j in range(1, width-1, 2):
            automaton_logic(df_copy, i, j)
            
    if wrap_around:
        i = height - 1
        for j in range(1, width-1, 2):
            automaton_logic_wrapped(df_copy, i, j)
            
        # Handle right-left wrapping
        j = width - 1
        for i in range(1, height-1, 2):
            automaton_logic_wrapped(df_copy, i, j)
            
        # Handle corner wrapping (bottom-right corner)
        automaton_logic_wrapped(df_copy, height-1, width-1)
    
    df[:] = df_copy[:]

def detect_cycle(state_history):
    """
    Detect cycles in the automaton's state history
    
    Parameters:
    - state_history: list of previous states (numpy arrays)
    
    Returns:
    - period: length of cycle if detected, 0 otherwise
    - cycle_start: index where cycle starts
    """
    if len(state_history) < 3:
        return 0, 0
    
    current_state = state_history[-1]
    
    # Check for cycles, comparing with all previous states
    for i in range(len(state_history) - 2, -1, -1):
        if np.array_equal(state_history[i], current_state):
            period = len(state_history) - 1 - i
            return period, i
    
    return 0, 0

def display_automaton(df, generation, fig, ax, img, state_history, pause_time=0.5):
    """
    Display the current state of the automaton and check for cycles
    
    Parameters:
    - df: current state of the automaton
    - generation: current generation number
    - fig, ax, img: matplotlib objects for visualization
    - state_history: list of previous states
    - pause_time: time to pause between frames
    
    Returns:
    - img: updated image object
    - cycle_detected: True if a cycle was detected, False otherwise
    - period: length of the detected cycle
    """
    ax.clear()
    img = ax.imshow(df, cmap='binary', vmin=0, vmax=1)
    
    # Add current state to history
    state_history.append(df.copy())
    
    # Check for cycles only if we have enough history
    period, cycle_start = detect_cycle(state_history)
    cycle_detected = period > 0
    
    if cycle_detected:
        ax.set_title(f'Generation: {generation} - Period: {period}')
    else:
        ax.set_title(f'Generation: {generation}')
    
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Force the figure to update
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(pause_time)
    
    return img, cycle_detected, period

def automatkind():
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

def pattern_choice():
    print("\nChoose pattern type:")
    print("1: Blinker")
    print("2: Traffic Light")
    print("3: Small oscillator")
    print("4: Zigzag Glider (we found it when we searched for a glider)")
    print("5: Plus Shape")
    print("6: Square Shape (creates gliders)")
    print("7: X Shape")
    print("8: Single Cell")
    
    while True:
        choice = input().strip()
        if choice == "1":
            return "blinker"
        elif choice == "2":
            return "traffic_light"
        elif choice == "3":
            return "small_oscillator"
        elif choice == "4":
            return "zigzag_glider"
        elif choice == "5":
            return "plus_shape"
        elif choice == "6":
            return "square_shape"
        elif choice == "7":
            return "x_shape"
        elif choice == "8":
            return "single_cell"
        else:
            print("Invalid choice. Please enter a number between 1 and 8")

def run_analysis(wrap_around=True):
    """
    Run analysis of cycle periods for all patterns
    
    Parameters:
    - wrap_around: whether to use wrap-around boundary conditions
    
    Returns:
    - results: dictionary with cycle periods for each pattern
    """
    height, width = 100, 100
    patterns = ["blinker", "traffic_light", "small_oscillator", 
                "zigzag_glider", "plus_shape", 
                "square_shape", "x_shape", "single_cell"]
    
    results = {}
    
    print(f"\nAnalyzing cycles with wrap-around={wrap_around}:")
    
    for pattern in patterns:
        print(f"Analyzing {pattern}...")
        df, generation = initialize_automaton(height, width, pattern)
        state_history = [df.copy()]
        
        cycle_detected = False
        period = 0
        
        # Run for at most 100 generations or until we detect a cycle
        for i in range(100):
            if generation % 2 == 1:
                odd_gen(df)
            else:
                even_gen(df, wrap_around)
            generation += 1
            
            # Check for cycles
            current_state = df.copy()
            for j, past_state in enumerate(state_history):
                if np.array_equal(past_state, current_state):
                    cycle_detected = True
                    period = len(state_history) - j
                    break
            
            if cycle_detected:
                break
                
            state_history.append(current_state)
        
        if cycle_detected:
            results[pattern] = period
            print(f"  {pattern}: Period {period}")
        else:
            results[pattern] = "No cycle detected (> 100 generations)"
            print(f"  {pattern}: No cycle detected")
    
    return results

def main():
    print("\nChoose mode:")
    print("1: Run visualization")
    print("2: Analyze cycle periods for all patterns")
    
    mode_choice = input().strip()
    
    if mode_choice == "2":
        # Run analysis of cycle periods
        print("\nAnalyzing with wrap-around:")
        results_wrap = run_analysis(True)
        
        print("\nAnalyzing without wrap-around:")
        results_no_wrap = run_analysis(False)
        
        # Print summary
        print("\nSummary of cycle periods:")
        print("Pattern             | With wrap-around | Without wrap-around")
        print("--------------------|------------------|-------------------")
        for pattern in ["blinker", "traffic_light", "small_oscillator", 
                        "zigzag_glider", "plus_shape", 
                        "square_shape", "x_shape", "single_cell"]:
            wrap_result = results_wrap.get(pattern, "Unknown")
            no_wrap_result = results_no_wrap.get(pattern, "Unknown")
            print(f"{pattern.ljust(20)}| {str(wrap_result).ljust(18)}| {no_wrap_result}")
    else:
        # Run visualization
        height, width = 100, 100
        wrap_around = automatkind()
        
        # Choose which pattern to display
        pattern = pattern_choice()
        
        df, generation = initialize_automaton(height, width, pattern)
        
        # Set up the plot for visualization
        fig, ax = plt.subplots(figsize=(10, 10))
        img = ax.imshow(df, cmap='binary')
        ax.set_title(f'Generation: {generation}')
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Display the initial state and wait for window to appear
        fig.canvas.draw()
        plt.pause(2.0)  # Initial pause of 2 seconds to see Generation 1
        
        # For cycle detection
        state_history = [df.copy()]
        cycle_detected = False
        period = 0
        
        max_generations = 300  # Increased to 300 generations as requested
        pause_time = 0.2
        
        for i in range(max_generations):
            if generation % 2 == 1:
                odd_gen(df)
            else:
                even_gen(df, wrap_around)
            generation += 1
            
            # Update visualization and check for cycles
            img, cycle_detected, period = display_automaton(df, generation, fig, ax, img, state_history, pause_time)
            
            # If we detected a cycle, run a few more generations to show it
            if cycle_detected and i < max_generations - 10:
                # Continue for a few more generations to show the cycle
                continue
            elif cycle_detected:
                break
        
        plt.draw()
        plt.pause(3)
        plt.close(fig)

if __name__ == "__main__":
    main()