import pygame
import sys

# ---------------- NODE ----------------
class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.next = None


# ---------------- LINKED LIST ----------------
class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert_after(self, current, new_node):
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        elif current == self.tail:
            self.tail.next = new_node
            self.tail = new_node
        else:
            new_node.next = current.next
            current.next = new_node

    def print_points(self):
        cur = self.head
        while cur:
            print(cur.x, cur.y)
            cur = cur.next

    def split(self):
        cur = self.head
        suc = cur.next

        while suc:
            avg_x = (cur.x + suc.x) / 2
            avg_y = (cur.y + suc.y) / 2
            self.insert_after(cur, Node(avg_x, avg_y))
            cur = suc
            suc = cur.next

        avg_x = (cur.x + self.head.x) / 2
        avg_y = (cur.y + self.head.y) / 2
        self.insert_after(cur, Node(avg_x, avg_y))

    def average(self):
        cur = self.head
        suc = cur.next

        head_x = self.head.x
        head_y = self.head.y

        while suc:
            cur.x = (cur.x + suc.x) / 2
            cur.y = (cur.y + suc.y) / 2
            cur = suc
            suc = cur.next

        cur.x = (cur.x + head_x) / 2
        cur.y = (cur.y + head_y) / 2

    def subdivide(self):
        self.split()
        self.average()

    def to_list(self):
        pts = []
        cur = self.head
        while cur:
            pts.append((cur.x, cur.y))
            cur = cur.next
        return pts


# ---------------- FIND NODE (FOR DRAGGING) ----------------
def find_closest_node(point_list, mouse_pos, radius=10):
    cur = point_list.head
    while cur:
        dx = cur.x - mouse_pos[0]
        dy = cur.y - mouse_pos[1]
        if dx*dx + dy*dy < radius*radius:
            return cur
        cur = cur.next
    return None


# ---------------- LOAD ----------------
def load_points(filename):
    ll = LinkedList()

    try:
        with open(filename, "r") as f:
            coords = f.read().split()
        coords = list(map(float, coords))
    except:
        print("⚠️ Using default points")
        coords = [100, 100, 200, 200, 300, 100]

    prev = None
    for i in range(0, len(coords), 2):
        node = Node(coords[i], coords[i+1])
        ll.insert_after(prev, node)
        prev = node

    return ll


# ---------------- MAIN ----------------
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Subdivision Project")
clock = pygame.time.Clock()

# ✅ LOAD FILE (your path)
point_list = load_points("C:/Users/mm566064/Downloads/Points.txt")

# ✅ SAVE ORIGINAL TRIANGLE
original_shape = point_list.to_list()

# DRAGGING VARIABLES
selected_node = None
dragging = False

running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # -------- KEYBOARD --------
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                print("Subdivide")
                point_list.subdivide()

            elif event.key == pygame.K_l:
                print("Split")
                point_list.split()

            elif event.key == pygame.K_a:
                print("Average")
                point_list.average()

            elif event.key == pygame.K_p:
                print("Points:")
                point_list.print_points()

            elif event.key == pygame.K_q:
                print("Exiting program...")
                running = False

        # -------- MOUSE (DRAGGING) --------
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            selected_node = find_closest_node(point_list, mouse_pos)
            if selected_node:
                dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            selected_node = None

        elif event.type == pygame.MOUSEMOTION:
            if dragging and selected_node:
                mouse_pos = pygame.mouse.get_pos()
                selected_node.x = mouse_pos[0]
                selected_node.y = mouse_pos[1]

    # UPDATED SHAPE
    new_shape = point_list.to_list()

    # 🔵 ORIGINAL TRIANGLE
    pygame.draw.lines(screen, (0, 200, 255), True, original_shape, 2)

    # 🟠 SUBDIVIDED SHAPE
    pygame.draw.lines(screen, (255, 120, 0), True, new_shape, 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()