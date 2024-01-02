"""
The ribbon tool includes a series of different animated physics based drawing methods dealing with the relationships
between different nodes. Each tick of animation each node performs its generic actions to update its positions.
Special care is taken to indicate how the drawing between the several nodes should take place.
"""

import math

import wx

from meerk40t.gui.scene.sceneconst import RESPONSE_CHAIN, RESPONSE_CONSUME
from meerk40t.gui.toolwidgets.toolwidget import ToolWidget
from meerk40t.tools.geomstr import Geomstr


class RibbonNode:
    def __init__(self, ribbon):
        self.brush = wx.Brush(wx.RED)
        self.pen = wx.Pen(wx.BLUE)
        self.diameter = 5000
        self.ribbon = ribbon
        self.position = None

    def get(self, index):
        return self.ribbon.nodes[index].position

    def tick(self):
        pass

    def process_draw(self, gc: wx.GraphicsContext):
        if not self.position:
            return
        gc.PushState()
        gc.SetPen(self.pen)
        gc.SetBrush(self.brush)
        gc.DrawEllipse(self.position[0], self.position[1], self.diameter, self.diameter)
        gc.PopState()


class OrientationNode(RibbonNode):
    """
    Orientation node is a 5 node positional. It is located at the reference node. At some angle and some distance away.
    """

    def __init__(
        self, ribbon, ref_node=0, a0=None, a1=None, d0=None, d1=None, dx=0., dy=0., d_theta=0.
    ):
        super().__init__(ribbon)
        self.ref_node = ref_node
        self.a0 = a0
        self.a1 = a1
        self.d0 = d0
        self.d1 = d1
        self.dx = dx
        self.dy = dy
        self.d_theta = d_theta

    def tick(self):
        ref_pos = self.get(self.ref_node)
        angle_start = self.get(self.a0)
        angle_end = self.get(self.a1)
        angle = Geomstr.angle(None, complex(*angle_start), complex(*angle_end))
        angle += self.d_theta

        distance_start = self.get(self.d0)
        distance_end = self.get(self.d1)
        distance = Geomstr.distance(
            None, complex(*distance_start), complex(*distance_end)
        )
        x = distance * math.cos(angle) + ref_pos[0] + self.dx
        y = distance * math.sin(angle) + ref_pos[1] + self.dy
        self.position = [x, y]


class GravityNode(RibbonNode):
    """
    Gravity node moves towards the node index it is attracted to at the given friction and attraction amount
    """

    def __init__(self, ribbon, attract_node=0):
        super().__init__(ribbon)
        self.friction = 0.05
        self.distance = 50
        self.attraction = 500
        self.velocity = [0.0, 0.0]
        self.attract_node = attract_node

    def tick(self):
        towards_pos = self.get(self.attract_node)
        if self.position is None:
            self.position = list(self.ribbon.position)
        vx = self.velocity[0] * (1 - self.friction)
        vy = self.velocity[1] * (1 - self.friction)
        angle = Geomstr.angle(None, complex(*towards_pos), complex(*self.position))
        vx -= self.attraction * math.cos(angle)
        vy -= self.attraction * math.sin(angle)

        self.velocity[0] = vx
        self.velocity[1] = vy
        self.position[0] += vx
        self.position[1] += vy


class PositionNode(RibbonNode):
    """
    Position node is simply the ribbon's last identified position as a node.
    """

    def __init__(self, ribbon):
        super().__init__(ribbon)
        self.ribbon = ribbon
        self.brush = wx.Brush(wx.RED)
        self.pen = wx.Pen(wx.BLUE)

    def tick(self):
        self.position = self.ribbon.position


class DrawSequence:
    """
    Draw sequence is what sort of drawn connections should occur between the different nodes and in what sequences.

    There are three levels of steps.
    1. The outermost is the series level and each series level step is drawn completely independent of any other series.
    These are disjointed paths.
    2. The step level is done in tick order.
    3. The indexes are performed in order during a tick.
    """

    def __init__(self, ribbon, sequences):
        self.series = {}
        self.tick_index = 0
        self.ribbon = ribbon
        self.pen = wx.Pen(wx.BLUE)
        self.sequences = sequences

    @classmethod
    def zig(cls, ribbon):
        """
        This is one path, [] and each is in a 4 tick sequence. The first sequence is 0 the second 0, third 1 and then 1
        So this draws between element 0, then element 0, then element 1, then element 1. Performing a zig-zag.
        @param ribbon:
        @return:
        """
        return cls(ribbon, sequences=[[[0], [0], [1], [1]]])

    @classmethod
    def bounce(cls, ribbon, *args):
        return cls(ribbon, sequences=[[list(args)]])

    def tick(self):
        """
        Process draw sequencing for the given tick.
        @return:
        """
        self.tick_index += 1
        for s, sequence in enumerate(self.sequences):
            series = self.series.get(s)
            if series is None:
                # Add series if not init
                series = []
                self.series[s] = series

            q = self.tick_index % len(sequence)
            seq = sequence[q]
            for i in seq:
                x, y = self.ribbon.nodes[i].position
                series.append((x, y))

    def process_draw(self, gc: wx.GraphicsContext):
        """
        Draws the current sequence.
        @param gc:
        @return:
        """
        gc.SetPen(self.pen)
        for q in self.series:
            series = self.series[q]
            gc.StrokeLines(series)

    def get_path(self):
        """
        Get the sequence as a geomstr path.
        @return: geomstr return object
        """

        g = Geomstr()
        for q in self.series:
            series = self.series[q]
            g.polyline(points=[complex(x, y) for x, y in series])
        return g

    def clear(self):
        self.series.clear()


class Ribbon:
    def __init__(self):
        self.nodes = []
        self.sequence = DrawSequence.zig(self)
        self.position = None

    @classmethod
    def gravity_tool(cls):
        """
        Gravity tool is a position node and a single gravity node that moves towards it.
        @return:
        """
        obj = cls()
        obj.nodes.append(PositionNode(obj))
        obj.nodes.append(GravityNode(obj, 0))
        obj.sequence = DrawSequence.zig(obj)
        return obj

    @classmethod
    def line_gravity_tool(cls):
        """
        Gravity line tool is a position node, being tracked by a gravity node, which in turn is tracked by another such
        node. The draw sequence bounces between the two gravity nodes.

        @return:
        """
        obj = cls()
        obj.nodes.append(PositionNode(obj))
        obj.nodes.append(GravityNode(obj, 0))
        obj.nodes.append(GravityNode(obj, 1))
        obj.sequence = DrawSequence.bounce(obj, 1, 2)
        return obj

    def tick(self):
        """
        Delegate to nodes and sequence.
        @return:
        """
        for node in self.nodes:
            node.tick()
        self.sequence.tick()

    def process_draw(self, gc: wx.GraphicsContext):
        """
        Delegate to nodes and sequence.
        @return:
        """
        for node in self.nodes:
            node.process_draw(gc)
        self.sequence.process_draw(gc)

    def get_path(self):
        """
        Delegate to sequence.
        @return:
        """
        return self.sequence.get_path()

    def clear(self):
        self.sequence.clear()


class RibbonTool(ToolWidget):
    """
    Ribbon Tool draws new segments by animating some click and press locations.
    """

    def __init__(self, scene, mode="gravity"):
        ToolWidget.__init__(self, scene)
        self.stop = False
        if mode == "gravity":
            self.ribbon = Ribbon.gravity_tool()
        elif mode == "line":
            self.ribbon = Ribbon.line_gravity_tool()
        else:
            self.ribbon = Ribbon.gravity_tool()

    def process_draw(self, gc: wx.GraphicsContext):
        self.ribbon.process_draw(gc)

    def tick(self):
        self.ribbon.tick()
        self.scene.request_refresh()
        if self.stop:
            return False
        return True

    def event(
        self, window_pos=None, space_pos=None, event_type=None, modifiers=None, **kwargs
    ):
        # We don't set tool_active here, as this can't be properly honored...
        # And we don't care about nearest_snap either...
        response = RESPONSE_CHAIN
        if event_type == "leftdown":
            self.stop = False
            self.ribbon.position = space_pos[:2]
            self.scene.animate(self)
            response = RESPONSE_CONSUME
        elif event_type == "move" or event_type == "hover":
            self.ribbon.position = space_pos[:2]
            response = RESPONSE_CONSUME
        elif event_type == "lost" or (event_type == "key_up" and modifiers == "escape"):
            self.stop = True
            self.ribbon.clear()
            if self.scene.pane.tool_active:
                self.scene.pane.tool_active = False
                self.scene.request_refresh()
                return RESPONSE_CONSUME
            else:
                return RESPONSE_CHAIN
        elif event_type == "leftup":
            self.stop = True
            t = self.ribbon.get_path()
            if not t:
                return RESPONSE_CONSUME
            elements = self.scene.context.elements
            node = elements.elem_branch.add(
                geometry=t,
                type="elem path",
                stroke_width=elements.default_strokewidth,
                stroke=elements.default_stroke,
                fill=elements.default_fill,
            )
            if elements.classify_new:
                elements.classify([node])
            self.ribbon.clear()
            response = RESPONSE_CONSUME
        return response
