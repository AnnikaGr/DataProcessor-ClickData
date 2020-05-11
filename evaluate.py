def evaluatePositions(mouse_click_list, stimulus):
    mouse_clicks_area1 = []
    mouse_clicks_area2 = []
    mouse_clicks_miss = []

    for mouse_click in mouse_click_list:
        appended = 0
        for rectangle in stimulus.areas_type1:
            if mouse_click.coord_x >= rectangle.left_boundary and mouse_click.coord_x <= rectangle.right_boundary and mouse_click.coord_y >= rectangle.bottom_boundary and mouse_click.coord_y <= rectangle.top_boundary:
                mouse_clicks_area1.append(mouse_click)
                appended = 1
        for rectangle in stimulus.areas_type2:
            if mouse_click.coord_x >= rectangle.left_boundary and mouse_click.coord_x <= rectangle.right_boundary and mouse_click.coord_y >= rectangle.bottom_boundary and mouse_click.coord_y <= rectangle.top_boundary:
                mouse_clicks_area2.append(mouse_click)
                appended = 1
        if appended == 0:
            mouse_clicks_miss.append(mouse_click)

    if len(mouse_click_list) > len(mouse_clicks_area1) + len(mouse_clicks_area2) + len(mouse_clicks_miss):
        raise ValueError('Some Mouseclick(s) must have been added to several lists')
    elif len(mouse_click_list) < len(mouse_clicks_area1) + len(mouse_clicks_area2) + len(mouse_clicks_miss):
        raise ValueError('Some Mouseclick(s) have not been added to any list')

    result = Result(mouse_clicks_area1, mouse_clicks_area2, mouse_clicks_miss)
    return result


class Result:
    def __init__(self, mouse_clicks_area1, mouse_clicks_area2, mouse_clicks_miss):
        self.mouse_clicks_area1 = mouse_clicks_area1
        self.mouse_clicks_area2 = mouse_clicks_area2
        self.mouse_clicks_miss = mouse_clicks_miss
