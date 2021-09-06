#! /usr/bin/python2

from operations import OperationBuilder
from itertools import product

left_margin_mm = 25
bottom_margin_mm = 25
pocket_x_mm = 105  # Should be about 5mm larger than your PCB blank size
pocket_y_mm = 165  # Should be about 5mm larger than your PCB blank size
pocket_depth_mm = 1.5  # Should be about 0.5mm less than your PCB blank thickness
bolt_diameter_mm = 4.0  # Just pick this to be a suitable size, you'll drill it out later
bolt_offset_mm = 6
bolt_drill_depth_mm = 10.0  # WARNING: Make sure this is less than you MDF thickness (or you'll drill your bed)

if __name__ == '__main__':

    pocket_bottom = bottom_margin_mm
    pocket_top = pocket_bottom + pocket_y_mm
    pocket_left = left_margin_mm + bolt_offset_mm
    pocket_right = pocket_left + pocket_x_mm

    ob = OperationBuilder(safe_z=10.0, feed_speed=2000, step_down=1.0, step_over=2.5,
                          cutter_radius=(6.0/2))

    ob.pocket(top_z=0.0, bottom_z=-pocket_depth_mm,
              left_x=pocket_left, right_x=pocket_right,
              bottom_y=pocket_bottom, top_y=pocket_top, dog_bone=True)

    ob = OperationBuilder(safe_z=10.0, feed_speed=2000, step_down=1.0, step_over=1.0,
                          cutter_radius=(3.175/2))

    bolt_hole_radius_mm = (bolt_diameter_mm/2.0)
    hole_locations = product(
        [(pocket_left - bolt_offset_mm - bolt_hole_radius_mm), (pocket_right + bolt_offset_mm + bolt_hole_radius_mm)],
        [(pocket_top - bolt_offset_mm - bolt_hole_radius_mm), (pocket_bottom + bolt_offset_mm + bolt_hole_radius_mm)])

    for (hx, hy) in hole_locations:
        ob.hole(top_z=0.0, bottom_z=-bolt_drill_depth_mm, centre_x=hx, centre_y=hy, radius=bolt_diameter_mm/2.0)
