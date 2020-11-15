#! /usr/bin/python2

from operations import OperationBuilder

if __name__ == '__main__':

    ob = OperationBuilder(safe_z=10.0, feed_speed=2000, step_down=1.0, step_over=1.0,
                          cutter_radius=(3.175/2))

    ob.pocket(top_z=0.0, bottom_z=-5.0, left_x=20.0, right_x=42.175, bottom_y=-5.0, top_y=245.0, dog_bone=False)
    ob.pocket(top_z=0.0, bottom_z=-5.0, left_x=48.175, right_x=131.825, bottom_y=-5.0, top_y=245.0, dog_bone=False)
    ob.pocket(top_z=0.0, bottom_z=-5.0, left_x=137.825, right_x=160.0, bottom_y=-5.0, top_y=245.0, dog_bone=False)
    ob.hole(top_z=0.0, bottom_z=-17.0, centre_x=15.375, centre_y=25.0, radius=3.0)
    ob.hole(top_z=0.0, bottom_z=-17.0, centre_x=15.375, centre_y=215.0, radius=3.0)
    ob.hole(top_z=0.0, bottom_z=-17.0, centre_x=164.625, centre_y=25.0, radius=3.0)
    ob.hole(top_z=0.0, bottom_z=-17.0, centre_x=164.625, centre_y=215.0, radius=3.0)

    with open('./bed_underside_prog_1.ngc', 'wt') as f:
        f.write(ob.get_g_code())

    ob2 = OperationBuilder(safe_z=10.0, feed_speed=2000, step_down=1.0, step_over=1.0,
                           cutter_radius=(3.175/2))

    ob2.pocket(top_z=0.0, bottom_z=-5.0, left_x=-5.0, right_x=22.0, bottom_y=-5.0, top_y=245.0, dog_bone=False)
    ob2.pocket(top_z=0.0, bottom_z=-5.0, left_x=158.0, right_x=185.0, bottom_y=-5.0, top_y=245.0, dog_bone=False)

    with open('./bed_underside_prog_2.ngc', 'wt') as f:
        f.write(ob2.get_g_code())
    
