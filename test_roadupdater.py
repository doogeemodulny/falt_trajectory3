from roadupdater import *


def test_get_circles_from_data():
    data = read_data("input.json")
    roadupdater = RoadUpdater()
    roadupdater._RoadUpdater__get_circles_from_data(data)
    assert roadupdater.circles == [Circle(45.100101, 44.100101, 11),
                                   Circle(52.100201, 14.100201, 12),
                                   Circle(86.100301, 44.100301, 13)
                                   ]


def test_point_of_circle():
    data = read_data("input.json")
    roadupdater = RoadUpdater()
    roadupdater._RoadUpdater__get_circles_from_data(data)
    point = Point(85, 43)
    circle = Circle(86.100301, 44.100301, 13)
    assert roadupdater._RoadUpdater__point_of_circle(point) == [circle]


def test_nearest_crossed_circle():
    roadupdater = RoadUpdater()
    roadupdater._RoadUpdater__B = Point(100.100101, 13.100101)
    assert roadupdater._RoadUpdater__nearest_crossed_circle(Point(0.100301, 0.100301)) == Circle(52.100201, 14.100201,
                                                                                                 12)
    assert roadupdater._RoadUpdater__nearest_crossed_circle(Point(80.100201, 80.100201)) == Circle(86.100301, 44.100301,
                                                                                                   13)


def test_make_road_bypass():
    roadupdater = RoadUpdater()
    roadupdater._RoadUpdater__A = Point(0.100301, 0.100301)
    roadupdater._RoadUpdater__B = Point(100.100101, 13.100101)
    roadupdater._RoadUpdater__make_road()
    check_road = Road()
    check_road.add(Arc(Circle(52.100201, 14.100201, 12), Point(52.559351628382245, 2.108988354881235),
                       Point(54.85686835607951, 2.42112633254772)))
    check_road.add(Segment(Point(54.85686835607951, 2.42112633254772), Point(100.100101, 13.100101)))
    check_road.add(Segment(Point(0.100301, 0.100301), Point(52.559351628382245, 2.108988354881235)))
    assert roadupdater.road == check_road


def test_update_road_bypass():
    roadupdater = RoadUpdater()
    old_road = Road()
    old_road.add(Segment(Point(54.85686835607951, 2.42112633254772), Point(100.100101, 13.100101)))
    old_road.add(Arc(Circle(52.100201, 14.100201, 12), Point(52.559351628382245, 2.108988354881235),
                     Point(54.85686835607951, 2.42112633254772)))
    old_road.add(Segment(Point(0.100301, 0.100301), Point(52.559351628382245, 2.108988354881235)))
    updated_road = roadupdater.update_road(Point(0.100301, 0.100301), Point(100.100101, 13.100101))
    assert updated_road == old_road


def test_update_road_no_bypass():
    roadupdater = RoadUpdater()
    old_road2 = Road()
    old_road2.add(Segment(Point(0, 0), Point(30, 40)))
    assert roadupdater.update_road(Point(0, 0), Point(30, 40)) == old_road2
