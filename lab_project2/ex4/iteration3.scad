// Improved Simplified Airbus A330-200 Parametric Model
// Units: metres
// Purpose: Exercise 4 - VLM + LLM + OpenSCAD aircraft generation

$fn = 72;

// =====================================================
// Display mode
// Change this to inspect individual components:
// "fuselage", "wing", "htail", "vtail", "engines", "all"
// =====================================================
show_mode = "all";

// =====================================================
// Main parameters from A330-200 table
// =====================================================

fuselage_length = 58.82;
fuselage_diameter = 5.64;
fuselage_radius = fuselage_diameter / 2;

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
engine_radius = engine_diameter / 2;

// Vertical tail estimated from area target
// Area approx = 0.5 * (root + tip) * height
vtail_height = 9.5;
vtail_root_chord = 8.0;
vtail_tip_chord = 3.1;
vtail_sweep = 35;
vtail_thickness = 0.35;

// Approximate longitudinal locations
wing_x_root = -8.0;
wing_z_root = -0.20;

htail_x_root = fuselage_length/2 - 8.2;
htail_z_root = 2.4;

vtail_x_root = fuselage_length/2 - 9.5;
vtail_z_root = fuselage_radius - 0.15;

// =====================================================
// Helper functions
// =====================================================

function absval(x) = x < 0 ? -x : x;

function wing_chord_at_y(y) =
    wing_root_chord + 
    (wing_tip_chord - wing_root_chord) * absval(y) / (wing_span / 2);

function wing_le_at_y(y) =
    wing_x_root
    + 0.25 * wing_root_chord
    + absval(y) * tan(wing_sweep25)
    - 0.25 * wing_chord_at_y(y);

function wing_z_at_y(y) =
    wing_z_root + absval(y) * tan(wing_dihedral);

module ellipsoid(rx, ry, rz) {
    scale([rx, ry, rz])
        sphere(1);
}

// =====================================================
// Fuselage
// =====================================================

module fuselage() {
    color("gold")
    union() {
        // Nose section
        hull() {
            translate([-fuselage_length/2, 0, 0])
                ellipsoid(0.15, 0.20, 0.20);

            translate([-fuselage_length/2 + 7.5, 0, 0])
                ellipsoid(2.0, fuselage_radius, fuselage_radius);
        }

        // Main cylindrical body
        hull() {
            translate([-fuselage_length/2 + 7.5, 0, 0])
                ellipsoid(2.0, fuselage_radius, fuselage_radius);

            translate([fuselage_length/2 - 13.0, 0, 0])
                ellipsoid(2.0, fuselage_radius, fuselage_radius);
        }

        // Aft fuselage transition
        // This section starts the upward tail-cone sweep.
        hull() {
            translate([fuselage_length/2 - 13.0, 0, 0])
                ellipsoid(2.0, fuselage_radius, fuselage_radius);

            translate([fuselage_length/2 - 7.0, 0, 0.70])
                ellipsoid(1.6, fuselage_radius * 0.72, fuselage_radius * 0.72);
        }

        // Upswept tail cone
        // The final point is higher than the main fuselage centerline.
        hull() {
            translate([fuselage_length/2 - 7.0, 0, 0.70])
                ellipsoid(1.6, fuselage_radius * 0.72, fuselage_radius * 0.72);

            translate([fuselage_length/2, 0, 1.25])
                ellipsoid(0.45, 0.65, 0.65);
        }
    }
}

// =====================================================
// Main wing
// =====================================================

module wing_half(side = 1) {
    semi_span = wing_span / 2;

    // Start from centreline so the wing intersects the fuselage.
    y_root = 0;
    y_tip = side * semi_span;

    x_root_le = wing_le_at_y(y_root);
    x_tip_le = wing_le_at_y(y_tip);

    z_root = wing_z_at_y(y_root);
    z_tip = wing_z_at_y(y_tip);

    c_root = wing_chord_at_y(y_root);
    c_tip = wing_chord_at_y(y_tip);

    t = wing_thickness;

    color("gold")
    polyhedron(
        points = [
            [x_root_le, y_root, z_root - t/2],
            [x_root_le + c_root, y_root, z_root - t/2],
            [x_tip_le + c_tip, y_tip, z_tip - t/2],
            [x_tip_le, y_tip, z_tip - t/2],

            [x_root_le, y_root, z_root + t/2],
            [x_root_le + c_root, y_root, z_root + t/2],
            [x_tip_le + c_tip, y_tip, z_tip + t/2],
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

    // Simple wing-body fairing / centre wing box
    color("gold")
    translate([wing_x_root + 4.5, 0, wing_z_root - 0.05])
        cube([7.0, fuselage_diameter * 1.05, 0.45], center = true);
}

// =====================================================
// Horizontal tail
// =====================================================

module htail_half(side = 1) {
    semi_span = htail_span / 2;

    y_root = 0;
    y_tip = side * semi_span;

    x_tip_le =
        htail_x_root
        + 0.25 * htail_root_chord
        + semi_span * tan(htail_sweep25)
        - 0.25 * htail_tip_chord;

    z_tip = htail_z_root + semi_span * tan(htail_dihedral);
    t = htail_thickness;

    color("gold")
    polyhedron(
        points = [
            [htail_x_root, y_root, htail_z_root - t/2],
            [htail_x_root + htail_root_chord, y_root, htail_z_root - t/2],
            [x_tip_le + htail_tip_chord, y_tip, z_tip - t/2],
            [x_tip_le, y_tip, z_tip - t/2],

            [htail_x_root, y_root, htail_z_root + t/2],
            [htail_x_root + htail_root_chord, y_root, htail_z_root + t/2],
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

    // Small central fairing to avoid disconnected look
    color("gold")
    translate([htail_x_root + 2.0, 0, htail_z_root])
        cube([4.0, 2.4, 0.35], center = true);
}

// =====================================================
// Vertical tail
// =====================================================

module vertical_tail() {
    x_tip_le = vtail_x_root + vtail_height * tan(vtail_sweep);

    color("gold")
    polyhedron(
        points = [
            [vtail_x_root, -vtail_thickness/2, vtail_z_root],
            [vtail_x_root + vtail_root_chord, -vtail_thickness/2, vtail_z_root],
            [x_tip_le + vtail_tip_chord, -vtail_thickness/2, vtail_z_root + vtail_height],
            [x_tip_le, -vtail_thickness/2, vtail_z_root + vtail_height],

            [vtail_x_root, vtail_thickness/2, vtail_z_root],
            [vtail_x_root + vtail_root_chord, vtail_thickness/2, vtail_z_root],
            [x_tip_le + vtail_tip_chord, vtail_thickness/2, vtail_z_root + vtail_height],
            [x_tip_le, vtail_thickness/2, vtail_z_root + vtail_height]
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

    // Simple dorsal fairing at tail root
    color("gold")
    translate([vtail_x_root + 2.5, 0, vtail_z_root - 0.1])
        cube([5.0, 1.2, 0.35], center = true);
}

// =====================================================
// Engines and pylons
// =====================================================

module engine(side = 1) {
    engine_y = side * 10.5;

    local_chord = wing_chord_at_y(engine_y);
    local_x_le = wing_le_at_y(engine_y);
    local_z = wing_z_at_y(engine_y);

    // Engine below and slightly forward of mid-chord
    engine_x = local_x_le + 0.38 * local_chord;
    engine_z = local_z - engine_radius - 1.0;

    color("lightgray")
    translate([engine_x, engine_y, engine_z])
        rotate([0,90,0])
            cylinder(h = engine_length, r = engine_radius, center = true);

    // Intake disk
    color("black")
    translate([engine_x - engine_length/2 - 0.03, engine_y, engine_z])
        rotate([0,90,0])
            cylinder(h = 0.06, r = engine_radius * 0.78, center = true);

    // Pylon height calculated to connect engine to wing
    pylon_height = local_z - (engine_z + engine_radius);

    color("dimgray")
    translate([engine_x + 0.2, engine_y, engine_z + engine_radius + pylon_height/2])
        cube([0.7, 0.45, pylon_height], center = true);
}

module engines() {
    engine(1);
    engine(-1);
}

// =====================================================
// Final assembly
// =====================================================

module aircraft() {
    fuselage();
    main_wing();
    horizontal_tail();
    vertical_tail();
    engines();
}

// =====================================================
// Component inspection selector
// =====================================================

if (show_mode == "fuselage") {
    fuselage();
}
else if (show_mode == "wing") {
    main_wing();
}
else if (show_mode == "htail") {
    horizontal_tail();
}
else if (show_mode == "vtail") {
    vertical_tail();
}
else if (show_mode == "engines") {
    engines();
}
else {
    aircraft();
}