import rclpy
from rclpy.node import Node
from std_msgs.msg import String

import pygame
import threading


class ChatDisplay(Node):
    def __init__(self):
        super().__init__('chat_display')

        self.subscription = self.create_subscription(
            String,
            '/display_feed',
            self.receive_message,
            10
        )

        self.display_publisher = self.create_publisher(
            String,
            '/display',
            10
        )

        self.latest_message = "Waiting....."
        self.message_count = 0
        self.off = 0
        self.lock = threading.Lock()
        self.status_start=0
        self.status_grid=0
        self.status_flag=0
        self.status_goal=0
        self.status_new=0
        self.grid=[]
        self.last_move=""
        self.display_timer = self.create_timer(1.5, self.send_command)
    
    def reset_status(self):
        self.status_start=0
        self.status_grid=0
        self.status_flag=0
        self.status_goal=0
        self.status_new=0
        self.grid=[]
        self.last_move=""
    
    def receive_message(self, msg):
        with self.lock:
            self.latest_message = msg.data
            self.message_count += 1
        self.get_logger().info(f'GET: {msg.data}')
        if msg.data == 'CONNECTED':
            if self.status_new==0:
                self.status_new=1
        elif msg.data == 'DISCONNECTED':
            self.reset_status()
        elif msg.data.startswith(':OUTPUT_GRID'):
            self.grid = msg.data.split()[1:]
        elif msg.data in ('RIGHT', 'LEFT', 'UP', 'DOWN', 'COMPLETED','END'):
            self.last_move = msg.data 

    def get_display_data(self):
        with self.lock:
            return self.latest_message

    def send_command(self, command="EMPTY"):
        if self.display_publisher.get_subscription_count() == 0:
            self.latest_message = "DISCONNECTED"
            self.reset_status()
            self.get_logger().info('DISCONNECTED')
            return

        msg = String()
        msg.data = command
        self.display_publisher.publish(msg)
        self.get_logger().info(f'Send_Command : {msg.data}')

def collision(x,y,x1,y1,w,h):
    return (x1<=x and x<=x1+w) and (y1<=y and y<=y1+h)

def ros_spin_thread(node):
    rclpy.spin(node)


def run_pygame(node):
    pygame.init()
    width_screen=750
    height_screen=650
    screen = pygame.display.set_mode((width_screen, height_screen))
    pygame.display.set_caption('ROS2 Chat Display')

    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Comic Sans MS', 30, pygame.font.Font.bold)

    running = True
    s = 30
    duck_bot_tile = pygame.image.load("duck_bot.png").convert_alpha()
    duck_bot_tile = pygame.transform.scale(duck_bot_tile, (s, s))
    path_tile = pygame.image.load("path_tile.png").convert_alpha()
    path_tile = pygame.transform.scale(path_tile, (s, s))
    wall_tile = pygame.image.load("wall_tile.png").convert_alpha()
    wall_tile = pygame.transform.scale(wall_tile, (s, s))
    start_tile = pygame.image.load("start_tile.png").convert_alpha()
    start_tile = pygame.transform.scale(start_tile, (s, s))
    goal_tile = pygame.image.load("goal_tile.png").convert_alpha()
    goal_tile = pygame.transform.scale(goal_tile, (s, s))
    flag_tile = pygame.image.load("flag_tile.png").convert_alpha()
    flag_tile = pygame.transform.scale(flag_tile, (s, s))
    bom_tile = pygame.image.load("bom_tile.png").convert_alpha()
    bom_tile = pygame.transform.scale(bom_tile, (s, s))

    node.send_command("BOMBS")
    click_pos=(-1,-1)
    bx=0
    by=0
    dx=0
    dy=0
    fx=0
    fy=0
    intss=0
    init_flag=0
    koo=[]
    text_flag=''
    while running:
        grid=node.grid
        message = node.get_display_data()
        screen.fill((255, 255, 255))
        color=(0,100,0)
        if message=="DISCONNECTED":
            screen.fill((120, 120, 0))
            color=(100,0,0)
            click_pos=(-1,-1)
            bx=0
            by=0
            dx=0
            dy=0
            fx=0
            fy=0
            intss=0
            koo=[]
            text_flag=''
        elif node.status_new==1:
            pygame.draw.rect(screen, (255, 0, 0), (width_screen/2-150, height_screen/2-30, 300, 30))
            text_surface = font.render("CLICK - TO START", True, color)
            screen.blit(text_surface, (width_screen/2-130, height_screen/2-25))
            if collision(click_pos[0],click_pos[1],width_screen/2-150, height_screen/2-30, width_screen/2-150+300, height_screen/2-30+30):
                click_pos=(-1,-1)
                node.status_new=-1 # Run once
                node.send_command("START")
                node.status_start=1
        elif node.status_start==1:
            for i in range(len(grid)):
                for j in range(len(grid[i])):
                    if grid[i][j] == '.':
                        screen.blit(path_tile, (j*s+10, i*s+50))
                    elif grid[i][j] == '#':
                        screen.blit(wall_tile, (j*s+10, i*s+50))
                    elif grid[i][j] == 'S':
                        if intss==0:
                            intss=1
                            bx=j*s+10
                            by=i*s+50
                            dx=bx
                            dy=by
                        screen.blit(start_tile, (j*s+10, i*s+50))
                    elif grid[i][j] == 'G':
                        screen.blit(goal_tile, (j*s+10, i*s+50))
                    elif grid[i][j] == 'F':
                        screen.blit(path_tile, (j*s+10, i*s+50))
                        if init_flag==0:
                            fx=j*s+10
                            fy=i*s+50
                            init_flag=1
                    elif grid[i][j] == 'X':
                        screen.blit(bom_tile, (j*s+10, i*s+50))
            moves_now=""
            if not node.status_goal:
                if bx<dx:
                    bx+=1
                    moves_now='RIGHT'
                elif bx>dx:
                    bx-=1
                    moves_now='LEFT'
                elif by<dy:
                    by+=1
                    moves_now='DOWN'
                elif by>dy:
                    by-=1
                    moves_now='UP'
                else :
                    node.send_command("MOVE")
                    move = node.last_move
                    node.last_move=''
                    koo.append(move)
                    if move=='RIGHT':
                        dx=bx+s
                    elif move=='LEFT':
                        dx=bx-s
                    elif move=='UP':
                        dy=by-s
                    elif move=='DOWN':
                        dy=by+s
                    elif move=='COMPLETED' and node.status_flag==0:
                        node.send_command("MOVE-BASE")
                        node.last_move=''
                        node.status_flag=1
                        text_flag='FLAG CAPTURED 🚩'
                    elif move=='END':
                        node.status_goal=1
                        text_flag='MISSION COMPLETED'
            status_moves = font.render(moves_now, True, (10,170,60))
            screen.blit(status_moves, (300, 20))

            status_flag_captured = font.render(text_flag, True, (10,170,120))
            screen.blit(status_flag_captured, (450, 10))
            screen.blit(duck_bot_tile, (bx, by))
            if (bx>=fx-s+10 and bx<=fx+s-10) and (by>=fy-s+10 and by<=fy+s-10):
                fx=bx
                fy=by
            screen.blit(flag_tile, (fx, fy))
        text_surface = font.render("MESSAGE :"+message, True, color)
        screen.blit(text_surface, (10, 0))
        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                for i in koo:
                    print(i)
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pygame.image.save(screen, "screenshot.jpg")
                    click_pos = event.pos

    pygame.quit()


def main(args=None):
    rclpy.init(args=args)
    node = ChatDisplay()

    ros_thread = threading.Thread(target=ros_spin_thread, args=(node,), daemon=True)
    ros_thread.start()

    run_pygame(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()