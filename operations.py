

class OperationBuilder:

    def __init__(self, safe_z, feed_speed, step_down, step_over, cutter_radius, z_ramp_ratio=5.0):
        self.safe_z = safe_z
        self.feed_speed = feed_speed
        self.step_down = step_down
        self.step_over = step_over
        self.cutter_radius = cutter_radius
        self.z_ramp_ratio = z_ramp_ratio

        self.g_code_str = 'G17 G21 G90 G64 P0.01\n'
        self.g_code_str += 'F%d\n' % self.feed_speed

    def get_g_code(self):

        return self.g_code_str + 'M2\n'

    def pocket(self, top_z, bottom_z, left_x, right_x, bottom_y, top_y, dog_bone=False, minor_dim=None):

        g_code_str = '\n(Pocket)\n'

        if dog_bone:
            raise ValueError('Dog-boning not yet supported')

        # Mutate bounds.
        # We now make these the extent to which the cutter can move.
        left_x = left_x + self.cutter_radius
        right_x = right_x - self.cutter_radius
        top_y = top_y - self.cutter_radius
        bottom_y = bottom_y + self.cutter_radius


        g_code_str += 'G0 Z%.3f\n' % self.safe_z
        g_code_str += 'G0 X%.3f Y%.3f\n' % (left_x, top_y)

        g_code_str += 'G1 Z%.3f\n' % top_z
        # Now at the point we want to start milling from

        z_next_layer = top_z - self.step_down
        z_next_layer = max(bottom_z, z_next_layer)

        if minor_dim == 'x':
            x_is_minor_dim = True
        elif minor_dim == 'y':
            x_is_minor_dim = False
        elif minor_dim is None:
            x_is_minor_dim = (right_x - left_x) > (top_y - bottom_y)

        if x_is_minor_dim:
            layer_t_to_b = True
            x_dir_l_to_r = True
            while z_next_layer >= bottom_z:
                # Ramped plunge
                if x_dir_l_to_r:
                    x_plunge = left_x + self.step_down*self.z_ramp_ratio
                else:
                    x_plunge = right_x - self.step_down*self.z_ramp_ratio
                g_code_str += 'G1 X%.3f Z%.3f\n' % (x_plunge, z_next_layer)
                if x_dir_l_to_r:
                    g_code_str += 'G1 X%.3f\n' % left_x
                else:
                    g_code_str += 'G1 X%.3f\n' % right_x

                # Edge at the start
                x_edge1 = left_x if x_dir_l_to_r else right_x
                x_edge2 = right_x if x_dir_l_to_r else left_x
                y_edge1 = top_y if layer_t_to_b else bottom_y
                y_edge2 = bottom_y if layer_t_to_b else top_y
                g_code_str += 'G1 X%.3f Y%.3f\n' % (x_edge1, y_edge1)
                g_code_str += 'G1 X%.3f Y%.3f\n' % (x_edge1, y_edge2)
                g_code_str += 'G1 X%.3f Y%.3f\n' % (x_edge2, y_edge2)
                g_code_str += 'G1 X%.3f Y%.3f\n' % (x_edge2, y_edge1)
                g_code_str += 'G1 X%.3f Y%.3f\n' % (x_edge1, y_edge1)

                # Traverse the square
                if layer_t_to_b:
                    y_this_row = top_y
                else:
                    y_this_row = bottom_y

                while (y_this_row >= bottom_y) if layer_t_to_b else (y_this_row <= top_y):
                    if x_dir_l_to_r:
                        g_code_str += 'G1 X%.3f Y%.3f\n' % (left_x, y_this_row)
                        g_code_str += 'G1 X%.3f Y%.3f\n' % (right_x, y_this_row)
                    else:
                        g_code_str += 'G1 X%.3f Y%.3f\n' % (right_x, y_this_row)
                        g_code_str += 'G1 X%.3f Y%.3f\n' % (left_x, y_this_row)

                    # Set up for next row
                    x_dir_l_to_r = not x_dir_l_to_r
                    if layer_t_to_b:
                        if y_this_row == bottom_y:
                            break
                        y_this_row -= self.step_over
                        y_this_row = max(y_this_row, bottom_y)
                    else:
                        if y_this_row == top_y:
                            break
                        y_this_row += self.step_over
                        y_this_row = min(y_this_row, top_y)

                # Set up for next layer
                layer_t_to_b = not layer_t_to_b
                if z_next_layer == bottom_z:
                    break
                z_next_layer -= self.step_down
                z_next_layer = max(bottom_z, z_next_layer)
        else:
            layer_l_to_r = True
            y_dir_t_to_b = True
            while z_next_layer >= bottom_z:
                # Ramped plunge
                if y_dir_t_to_b:
                    y_plunge = top_y - self.step_down*self.z_ramp_ratio
                else:
                    y_plunge = bottom_y + self.step_down*self.z_ramp_ratio
                g_code_str += 'G1 Y%.3f Z%.3f\n' % (y_plunge, z_next_layer)
                if y_dir_t_to_b:
                    g_code_str += 'G1 Y%.3f\n' % top_y
                else:
                    g_code_str += 'G1 Y%.3f\n' % bottom_y

                # Edge at the start
                y_edge1 = top_y if y_dir_t_to_b else bottom_y
                y_edge2 = bottom_y if y_dir_t_to_b else top_y
                x_edge1 = left_x if layer_l_to_r else right_x
                x_edge2 = right_x if layer_l_to_r else left_x
                g_code_str += 'G1 X%.3f Y%.3f\n' % (x_edge1, y_edge1)
                g_code_str += 'G1 X%.3f Y%.3f\n' % (x_edge1, y_edge2)
                g_code_str += 'G1 X%.3f Y%.3f\n' % (x_edge2, y_edge2)
                g_code_str += 'G1 X%.3f Y%.3f\n' % (x_edge2, y_edge1)
                g_code_str += 'G1 X%.3f Y%.3f\n' % (x_edge1, y_edge1)

                # Traverse the square
                if layer_l_to_r:
                    x_this_col = left_x
                else:
                    x_this_col = right_x

                while (x_this_col <= right_x) if layer_l_to_r else (x_this_col >= left_x):
                    if y_dir_t_to_b:
                        g_code_str += 'G1 X%.3f Y%.3f\n' % (x_this_col, top_y)
                        g_code_str += 'G1 X%.3f Y%.3f\n' % (x_this_col, bottom_y)
                    else:
                        g_code_str += 'G1 X%.3f Y%.3f\n' % (x_this_col, bottom_y)
                        g_code_str += 'G1 X%.3f Y%.3f\n' % (x_this_col, top_y)

                    # Set up for next row
                    y_dir_t_to_b = not y_dir_t_to_b
                    if layer_l_to_r:
                        if x_this_col == right_x:
                            break
                        x_this_col += self.step_over
                        x_this_col = min(x_this_col, right_x)
                    else:
                        if x_this_col == left_x:
                            break
                        x_this_col -= self.step_over
                        x_this_col = max(x_this_col, left_x)

                # Set up for next layer
                layer_l_to_r = not layer_l_to_r
                if z_next_layer == bottom_z:
                    break
                z_next_layer -= self.step_down
                z_next_layer = max(bottom_z, z_next_layer)

                # FIXME - edges

        # Return to start point
        g_code_str += 'G1 Z%.3f\n' % self.safe_z
        g_code_str += 'G0 X%.3f Y%.3f\n' % (left_x, top_y)


        self.g_code_str += g_code_str

    def hole(self, top_z, bottom_z, centre_x, centre_y, radius):
        # WARNING - not currently functional for hole requiring more than one sprial
        motion_radius = radius - self.cutter_radius
        motion_cirumference = 2.0 * motion_radius * 3.14159
        depth = top_z - bottom_z

        z_per_circle = motion_cirumference
        num_circles = int(depth * self.z_ramp_ratio / z_per_circle) + 1

        g_code_str = '\n(Hole)\n'
        g_code_str += 'G1 Z%.3f\n' % self.safe_z
        g_code_str += 'G0 X%.3f Y%.3f\n' % (centre_x, centre_y) # Move to centre
        g_code_str += 'G1 Z%.3f\n' % top_z # Move to surface

        g_code_str += 'G91\n' # Relative mode
        g_code_str += 'G1 X%.3f\n' % motion_radius
        g_code_str += 'G3 Z%.3f I-%.3f P%d\n' % (-depth, motion_radius, num_circles)
        g_code_str += 'G1 X%.3f\n' % -motion_radius
        # Back out
        g_code_str += 'G1 Z%.3f\n' % (depth)
        g_code_str += 'G90\n' # Absolute mode

        # Return to safe-height
        g_code_str += 'G1 Z%.3f\n' % self.safe_z

        self.g_code_str += g_code_str

