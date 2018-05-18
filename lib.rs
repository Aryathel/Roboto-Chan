extern crate libc;

#[no_mangle]
pub unsafe extern "C" fn calc_base_degrees(point_x: f64, point_y: f64) -> i32 {
    let dist_to_point = (point_x.powi(2) + point_y.powi(2)).sqrt();
    let mut champ = 0;
    let mut min_err = 100.0;
    for i in 64i32..181 {
        let new_err = ((point_x - dist_to_point * (i as f64).to_radians().cos()).powi(2)
            + (point_y - dist_to_point * (i as f64).to_radians().sin()).powi(2)).sqrt();
        if new_err < min_err {
            champ = i;
            min_err = new_err;
        }
    }
    champ
}

#[no_mangle]
pub unsafe extern "C" fn calc_base_us(point_x: f64, point_y: f64, point_z: f64) -> i32 {
    let angle_to_point = (point_y / point_x).atan();
    let actual_x = point_x - 13.625 * ; //13.625
    let actual_y =
    let actual_z = point_z - 6.075; //-1.2 for screw to top face of bottom of servo mount,
    // -3.25 for thickness of bottom of servo mount, -1.625 to centre of claw piece
    let dist_to_point = (point_x.powi(2) + point_y.powi(2)).sqrt();
    let mut champ = 0;
    let mut min_err = 100.0;
    for i in 1200i32..2376 {
        let mapped_angle = (i as f64 - 1200.0) * 116.0 / 1175.0 + 64.0;
        let new_err = ((point_x - dist_to_point * mapped_angle.to_radians().cos()).powi(2)
            + (point_y - dist_to_point * mapped_angle.to_radians().sin()).powi(2)).sqrt();
        if new_err < min_err {
            champ = i;
            min_err = new_err;
        }
    }
    champ
}

// Fix once base ones are fixed
#[no_mangle]
pub unsafe extern "C" fn calc_right_degrees(point_x: f64, point_y: f64, point_z: f64) -> i32 {
    let dist_to_point = (point_x.powi(2) + point_y.powi(2) + point_z.powi(2)).sqrt();
    let xy_dist_to_point = (point_x.powi(2) + point_y.powi(2)).sqrt();
    let slope = point_z / xy_dist_to_point;
}

// Fix once base ones are fixed
#[no_mangle]
pub unsafe extern "C" fn calc_left_degrees(point_x: f64, point_y: f64, point_z: f64) -> i32 {
    let dist_to_point = (point_x.powi(2) + point_y.powi(2) + point_z.powi(2)).sqrt();
    let xy_dist_to_point = (point_x.powi(2) + point_y.powi(2)).sqrt();
    let angle_xy_z = (point_z / xy_dist_to_point).atan();

}