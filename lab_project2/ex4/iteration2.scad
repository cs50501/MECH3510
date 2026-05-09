// Simplified Airbus A330-200 Parametric Model
// Units: metres

$fn = 64;

// -----------------------------
// Main parameters
// -----------------------------

fuselage_length = 58.82;
fuselage_diameter = 5.64;

wing_span = 60.30;
wing_root_chord = 10.56;
wing_tip_chord = 2.46;
wing_sweep25 = 30;
wing_dihedral = 4.3;
wing_thickness = 0.35;

htail_span = 19.4;
htail_root_chord = 4.5;
htail_tip_chord = 2.5;
htail_sweep25 = 25;
htail_dihedral = 6.63;
htail_thickness = 0.25;

engine_length = 4.173;
engine_diameter = 2.90;

// -----------------------------
// Helper modules
// -----------------------------

module ellipsoid(rx, ry, rz) {
    scale([rx, ry, rz])
        sphere(1);
}

module fuselage() {
    color("white")
    union() {
        // Nose section
        hull() {
            translate([-fuselage_length/2, 0, 0])
                ellipsoid(0.2, 0.3, 0.3);
            translate([-fuselage_length/2 + 8, 0, 0])
                ellipsoid(2.5, fuselage_diameter/2, fuselage_diameter/2);
        }

        // Main cylindrical body
        hull() {
            translate([-fuselage_length/2 + 8, 0, 0])
                ellipsoid(2.5, fuselage_diameter/2, fuselage_diameter/2);
            translate([fuselage_length/2 - 10, 0, 0])
                ellipsoid(2.5, fuselage_diameter/2, fuselage_diameter/2);
        }

        // Tail cone
        hull() {
            translate([fuselage_length/2 - 10, 0, 0])
                ellipsoid(2.5, fuselage_diameter/2, fuselage_diameter/2);
            translate([fuselage_length/2, 0, 0])
                ellipsoid(0.3, 0.8, 0.8);
        }
    }
}

module wing_half(side = 1, x_root = -8, z_root = 0) {
    semi_span = wing_span / 2;
    x_tip_le = x_root 
             + 0.25 * wing_root_chord 
             + semi_span * tan(wing_sweep25) 
             - 0.25 * wing_tip_chord;
    z_tip = z_root + semi_span * tan(wing_dihedral);

    y_root = side * fuselage_diameter / 2;
    y_tip = side * semi_span;

    t = wing_thickness;

    color("lightgray")
    polyhedron(
        points = [
            [x_root, y_root, z_root - t/2],
            [x_root + wing_root_chord, y_root, z_root - t/2],
            [x_tip_le + wing_tip_chord, y_tip, z_tip - t/2],
            [x_tip_le, y_tip, z_tip - t/2],

            [x_root, y_root, z_root + t/2],
            [x_root + wing_root_chord, y_root, z_root + t/2],
            [x_tip_le + wing_tip_chord, y_tip, z_tip + t/2],
            [x_tip_le, y_tip, z_tip + t/2]
        ],
        faces = [
            [0,1,2,3],
            [4,7,6,5],
            [0,4,5,1],
            [1,5,6,2],
            [2,6,7,3],
            [3,7,4,0]
        ]
    );
}

module main_wing() {
    wing_half(1);
    wing_half(-1);
}

module htail_half(side = 1, x_root = 21, z_root = 2.4) {
    semi_span = htail_span / 2;
    x_tip_le = x_root 
             + 0.25 * htail_root_chord 
             + semi_span * tan(htail_sweep25) 
             - 0.25 * htail_tip_chord;
    z_tip = z_root + semi_span * tan(htail_dihedral);

    y_root = side * 1.2;
    y_tip = side * semi_span;

    t = htail_thickness;

    color("lightgray")
    polyhedron(
        points = [
            [x_root, y_root, z_root - t/2],
            [x_root + htail_root_chord, y_root, z_root - t/2],
            [x_tip_le + htail_tip_chord, y_tip, z_tip - t/2],
            [x_tip_le, y_tip, z_tip - t/2],

            [x_root, y_root, z_root + t/2],
            [x_root + htail_root_chord, y_root, z_root + t/2],
            [x_tip_le + htail_tip_chord, y_tip, z_tip + t/2],
            [x_tip_le, y_tip, z_tip + t/2]
        ],
        faces = [
            [0,1,2,3],
            [4,7,6,5],
            [0,4,5,1],
            [1,5,6,2],
            [2,6,7,3],
            [3,7,4,0]
        ]
    );
}

module horizontal_tail() {
    htail_half(1);
    htail_half(-1);
}

module vertical_tail() {
    x_root = 21;
    z_root = fuselage_diameter / 2 - 0.2;

    fin_height = 8.5;
    root_chord = 7.0;
    tip_chord = 2.7;
    sweep = 35;
    thickness = 0.35;

    x_tip_le = x_root + fin_height * tan(sweep);

    color("lightgray")
    polyhedron(
        points = [
            [x_root, -thickness/2, z_root],
            [x_root + root_chord, -thickness/2, z_root],
            [x_tip_le + tip_chord, -thickness/2, z_root + fin_height],
            [x_tip_le, -thickness/2, z_root + fin_height],

            [x_root, thickness/2, z_root],
            [x_root + root_chord, thickness/2, z_root],
            [x_tip_le + tip_chord, thickness/2, z_root + fin_height],
            [x_tip_le, thickness/2, z_root + fin_height]
        ],
        faces = [
            [0,1,2,3],
            [4,7,6,5],
            [0,4,5,1],
            [1,5,6,2],
            [2,6,7,3],
            [3,7,4,0]
        ]
    );
}

module engine(side = 1) {
    x_engine = -3.0;
    y_engine = side * 10.5;
    z_engine = -3.0;

    color("silver")
    translate([x_engine, y_engine, z_engine])
        rotate([0,90,0])
            cylinder(h = engine_length, r = engine_diameter/2, center = true);

    // Intake opening
    color("black")
    translate([x_engine - engine_length/2 - 0.02, y_engine, z_engine])
        rotate([0,90,0])
            cylinder(h = 0.05, r = engine_diameter*0.42, center = true);

    // Simple pylon
    color("gray")
    translate([x_engine, y_engine, z_engine + 1.7])
        cube([1.0, 0.35, 2.0], center = true);
}

module engines() {
    engine(1);
    engine(-1);
}

// -----------------------------
// Final assembly
// -----------------------------

module aircraft() {
    fuselage();
    main_wing();
    horizontal_tail();
    vertical_tail();
    engines();
}

aircraft();