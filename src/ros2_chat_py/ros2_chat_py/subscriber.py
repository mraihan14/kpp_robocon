import rclpy
from rclpy.node import Node
from std_msgs.msg import String


# START, FLAG, BASE 

class ChatNode(Node):
    def __init__(self):
        super().__init__('chat_node_py')

        self.exist = 0
        self.command_start = 0
        self.code_name="Kwik"
        self.connect=0
        self.failed_message = String()
        self.failed_message.data = 'FAILED-CONNECTION'
        self.grids=""
        self.send_grid=0
        # --- BAGIAN 1: urus balasan ke publisher (bergantung pada /chatter) ---
        self.subscription_chatter = self.create_subscription(
            String,
            '/chatter',
            self.handle_reply,
            10
        )

        # --- BAGIAN 1b: dengar event klik dari display ---

        self.reply_publisher = self.create_publisher(
            String,
            '/chatter_reply',
            10
        )

        self.subs_display = self.create_subscription(
            String,
            '/display',
            self.show_display,
            10
        )

        self.reply_counter = 0

        # --- BAGIAN 2: display feed, independen, jalan sendiri pakai timer ---
        self.display_publisher = self.create_publisher(
            String,
            '/display_feed',
            10
        )
        self.display_counter = 0
        self.display_timer = self.create_timer(1.5, self.handle_display)

    def handle_reply(self, msg):
        if msg.data.startswith(":OUTPUT_GRID"):
            out=String()
            out.data=msg.data
            self.display_publisher.publish(out)
        if msg.data.startswith("MOVE"):
            out=String()
            out.data=msg.data.split(' ')[1]
            self.display_publisher.publish(out)
            self.get_logger().info(f'C++ Sent to /chatter_reply: {msg.data}  {out.data}')
        self.connect=1
        reply = String()
        reply.data="CONNECTED"
        self.reply_publisher.publish(reply)
        #self.get_logger().info(f'C++ Sent to /chatter_reply: {msg.data}')

    def show_display(self, msg):
        if msg.data=='START':
            reply = String()
            reply.data="GRID"
            self.reply_publisher.publish(reply)
        elif msg.data=="MOVE":
            reply = String()
            reply.data="MOVE"
            self.reply_publisher.publish(reply)
        elif msg.data=="MOVE-BASE":
            reply = String()
            reply.data="MOVE-BASE"
            self.reply_publisher.publish(reply)
        #self.get_logger().info(f'Terima pesan dari display: {msg.data}')

    def handle_display(self):
        if self.reply_publisher.get_subscription_count() == 0:
            self.connect=0

        if self.display_publisher.get_subscription_count() == 0:
            self.get_logger().info('Connection Failed')
            self.display_publisher.publish(self.failed_message)
            return

        out = String()
        out.data = 'CONNECTED'
        if self.connect==0:
            out.data="DISCONNECTED"
        self.display_publisher.publish(out)
        self.get_logger().info(f'Status: {out.data}')


def main(args=None):
    rclpy.init(args=args)
    node = ChatNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()