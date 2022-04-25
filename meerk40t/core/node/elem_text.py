from meerk40t.core.node.node import Node

from copy import copy


class TextNode(Node):
    """
    TextNode is the bootstrapped node type for the 'elem text' type.
    """

    def __init__(self, text=None, matrix=None, fill=None, stroke=None, stroke_width=None, **kwargs):
        super(TextNode, self).__init__(type="elem text", **kwargs)
        self.text = text
        self.settings = kwargs
        if matrix is None:
            self.matrix = text.transform
        else:
            self.matrix = matrix
        if fill is None:
            self.fill = text.fill
        else:
            self.fill = fill
        if stroke is None:
            self.stroke = text.stroke
        else:
            self.stroke = stroke
        if stroke_width is None:
            self.stroke_width = text.stroke_width
        else:
            self.stroke_width = stroke_width
        self.lock = False

    def __copy__(self):
        return TextNode(
            text=copy(self.text),
            matrix=copy(self.matrix),
            fill=copy(self.fill),
            stroke=copy(self.stroke),
            stroke_width=self.stroke_width,
            **self.settings
        )

    # TODO: TEXTNode, bounds

    def scale_native(self, matrix):
        self.matrix *= matrix
        self.text.transform = self.matrix
        self._bounds_dirty = True

    def default_map(self, default_map=None):
        default_map = super(TextNode, self).default_map(default_map=default_map)
        default_map['element_type'] = "Text"
        default_map.update(self.settings)
        default_map['text'] = self.text.text
        default_map["stroke"] = self.stroke
        default_map["fill"] = self.fill
        default_map["stroke-width"] = self.stroke_width
        default_map['matrix'] = self.matrix
        return default_map

    def drop(self, drag_node):
        # Dragging element into element.
        if drag_node.type.startswith("elem"):
            self.insert_sibling(drag_node)
            return True
        return False

    def revalidate_points(self):
        bounds = self.bounds
        if bounds is None:
            return
        if len(self._points) < 9:
            self._points.extend([None] * (9 - len(self._points)))
        self._points[0] = [bounds[0], bounds[1], "bounds top_left"]
        self._points[1] = [bounds[2], bounds[1], "bounds top_right"]
        self._points[2] = [bounds[0], bounds[3], "bounds bottom_left"]
        self._points[3] = [bounds[2], bounds[3], "bounds bottom_right"]
        cx = (bounds[0] + bounds[2]) / 2
        cy = (bounds[1] + bounds[3]) / 2
        self._points[4] = [cx, cy, "bounds center_center"]
        self._points[5] = [cx, bounds[1], "bounds top_center"]
        self._points[6] = [cx, bounds[3], "bounds bottom_center"]
        self._points[7] = [bounds[0], cy, "bounds center_left"]
        self._points[8] = [bounds[2], cy, "bounds center_right"]
        obj = self.text
        if hasattr(obj, "point"):
            if len(self._points) <= 11:
                self._points.extend([None] * (11 - len(self._points)))
            start = obj.point(0)
            end = obj.point(1)
            self._points[9] = [start[0], start[1], "endpoint"]
            self._points[10] = [end[0], end[1], "endpoint"]

    def update_point(self, index, point):
        return False

    def add_point(self, point, index=None):
        return False