import pygame
import random
import math
pygame.init()

class VizInfo:

    # creating class attributes
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont('comicsans', 20)
    LARGE_FONT = pygame.font.SysFont('comicsans', 25)


    SIDE_PAD = 100 # 50 px left, 50 px right
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height)) # creating pygame window
        pygame.display.set_caption("Algorithm Visualizer")

        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst) # getting min list value
        self.max_val = max(lst) # getting max list value
        

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst)) # area to represent blocks div by num of blocks
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val)) # total height drawable area, dynamically allocated
        self.start_x = self.SIDE_PAD // 2 # finding start x allocating for padding

def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR) # draw then update, redraw canvas every frame

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN) # text, anti-aliasing,color
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 5))
    
    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK) # text, anti-aliasing,color
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 45)) # centering top left hand. Middle = text width / 2 - screen width / 2.
    
    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort ", 1, draw_info.BLACK) # text, anti-aliasing,color
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 75))
    
    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD, 
                        draw_info.height - draw_info.TOP_PAD) # erasing just the list rectangles

        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height
        print(x, y)

        color = draw_info.GRADIENTS[i % 3] # always returns 0, 1, or 2; keeps colours separated

        if i in color_positions:
            color = color_positions[i]


        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))
    
    if clear_bg:
        pygame.display.update()




def generate_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val) # generating a random list
        lst.append(val)

    return lst

def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst)-1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j+1] = lst[j + 1], lst[j] # swapping pos without temp var
                draw_list(draw_info, {j: draw_info.GREEN, j+1: draw_info.RED}, True) # setting dict values for color
                yield True # call function for each swap. yields control back to where called.
                # generator, pausing and resuming from yield key origin
    
    return lst


# TODO: Implement other sort algorithms
def insertion_sort(draw_info, ascending=True):
    pass


def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    
    draw_info = VizInfo(800, 600, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort # change this to use different algo
    sorting_algo_name = "Bubble Sort" # change this to use different algo
    sorting_algorithm_generator = None

    while run: #pygame needs an event loop
        clock.tick(60) # fps, times run per second. To speed up algo increase this number.

        if sorting:
            try:
                next(sorting_algorithm_generator) # if sorting, try calling next on gen
            except StopIteration: # fails when generator is done
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)

        pygame.display.update() # update screen

        for event in pygame.event.get(): # list of events since last loop
            if event.type == pygame.QUIT: # hitting red x in corner
                run = False

            if event.type != pygame.KEYDOWN: # if event isn't keydown, continue
                continue

            if event.key == pygame.K_r: # is key an r?
                lst = generate_starting_list(n, min_val, max_val) # reset list
                draw_info.set_list(lst) # update list to be drawn
                sorting = False

            elif event.key == pygame.K_SPACE and sorting == False: # is key a space and not already sorting?
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending) # var stores generator object created by algo sorting function

            elif event.key == pygame.K_a and not sorting: # is key an a and not already sorting?
                ascending = True

            elif event.key == pygame.K_d and not sorting: # is key a d and not already sorting?
                ascending = False
            elif event.key == pygame.K_i and not sorting: # is key a d and not already sorting?
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting: # is key a d and not already sorting?
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"

    
    pygame.quit()

if __name__ == "__main__":
    main()



