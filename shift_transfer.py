from manim import *

def rotate_l(l):
    return [l[-1]] + l[:-1]

bit_string = "1000101101010101"
bit_list = list(bit_string)

class SpiScene(Scene):
    def construct(self):
        box=[]
        bits = []

        for i in range(16):
            if i == 0:
                box.append(Rectangle(height=0.5, width=0.5).move_to([-5, -2, 0]))
                bits.append(Text(bit_list[0], color=BLUE).move_to([-5, -2, 0]).scale(0.7))
            elif i < 8:
                box.append(Rectangle(height=0.5, width=0.5).move_to([-5, 0.5*i-2, 0]))
                bits.append(Text(bit_list[i], color=BLUE).move_to([-5, 0.5*i-2, 0]).scale(0.7))
            else:
                box.append(Rectangle(height=0.5, width=0.5).move_to([5, 1.5 - 0.5*(i%8), 0]))
                bits.append(Text(bit_list[i], color=ORANGE).move_to([5, 1.5 - 0.5*(i%8), 0]).scale(0.7))
        boxes = VGroup(box)
        data = VGroup(bits)
        self.add(boxes)
        self.add(data)
        self.add(Text("Main", color=BLUE).next_to(box[7], UP).shift(0.5*UP).scale(0.5))
        self.add(Text("Sub", color=ORANGE).next_to(box[8], UP).shift(0.5*UP).scale(0.5))
        self.wait(3)

        # shift the left up and the right down
        master = []
        slave = []
        tx_buffer = Text("11110101", color=BLUE).arrange(DOWN)
        slave_tx = Text("11001110", color=ORANGE).arrange(DOWN)
        for i in range(len(bits)):
            master_buffer = VGroup(bits[:8])
            slave_buffer = VGroup(bits[-8:])
            if i == 8:
                for j in range(8):
                    temp = bits[j].copy()
                    temp2 = bits[j+8].copy()
                    master.append(temp.next_to(box[j], LEFT))
                    slave.append(temp2.next_to(box[j+8], RIGHT))
                self.play([Write(el) for el in master] + [Indicate(el, color=WHITE) for el in boxes[:8]] + [Write(el) for el in slave] + [Indicate(el, color=WHITE) for el in boxes[-8:]], run_time=1.5)
                self.wait(1)
                master_group = VGroup(master)
                slave_group = VGroup(slave)
                self.play(master_group.animate.shift(LEFT+2*DOWN).scale(0.5), slave_group.animate.shift(RIGHT+2*DOWN).scale(0.5))

                self.play(Write(tx_buffer.next_to(master_group, UP).scale(0.5)), Write(slave_tx.next_to(slave_group, UP).scale(0.5)))
                self.wait(1)
                self.play(tx_buffer.animate.shift(RIGHT+1.55*DOWN).scale(1.7), [slave_tx[i].animate.next_to(boxes[8+i], RIGHT).scale(1.7) for i in range(len(slave_tx))])
                self.wait(1)
                self.play(tx_buffer.animate.shift(0.7*RIGHT), slave_tx.animate.shift(0.6*LEFT))
                self.play(Unwrite(data), run_time=0.2)
                self.remove(*bits)
                bits = [Text(index, color=BLUE).move_to(boxes[7-i].get_center()) for i, index in enumerate("11110101")] + [Text(index, color=ORANGE).move_to(boxes[8+i].get_center()) for i, index in enumerate("11001110")]
                master_buffer = VGroup(bits[:8])
                slave_buffer = VGroup(bits[-8:])
                self.play(ReplacementTransform(tx_buffer, master_buffer), ReplacementTransform(slave_tx, slave_buffer))
                bits = bits[:8][::-1] + bits[-8:]
                self.wait(1)
            self.play(master_buffer.animate.shift(0.5*UP), slave_buffer.animate.shift(0.5*DOWN))
            self.play(bits[7].animate.move_to([5,2,0]), bits[-1].animate.move_to([-5,-2.5,0]), run_time=0.2)
            self.play(bits[7].animate.shift(0.5*DOWN), bits[-1].animate.shift(0.5*UP))
            bits = rotate_l(bits)
        temp = [el.copy() for el in bits]
        m_group = VGroup(temp[:8])
        s_group = VGroup(temp[-8:])
        self.play([Write(temp[i].next_to(box[i], LEFT)) for i in range(8)] + [Write(temp[8+i].next_to(box[8+i], RIGHT)) for i in range(8)] + [Indicate(el, color=WHITE) for el in boxes], run_time=1.5)        
        self.play([m_group.animate.shift(0.5*LEFT+2*DOWN).scale(0.5), s_group.animate.shift(0.5*RIGHT+2*DOWN).scale(0.5)])
        self.wait(3)
