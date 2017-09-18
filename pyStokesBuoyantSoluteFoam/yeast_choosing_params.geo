// We comment out the parameter definitions, as they should be set via
// command line input. 
/*
lc = .1;
r_yeast = 0.5;
r_petri = 6.46;
slice_angle = 2.5; // degrees
*/

// Create the base points

ori = newp; Point(ori) = {0, 0, 0, lc};

top_ori = newp; Point(top_ori) = {0, 0, 1, lc};

top_yeast= newp; Point(top_yeast) = {r_yeast, 0, 1, lc};

top_petri= newp; Point(top_petri) = {r_petri, 0, 1, lc};

bot_petri = newp; Point(bot_petri) = {r_petri, 0, 0, lc};

bot_yeast = newp; Point(bot_yeast) = {r_yeast, 0, 0, lc};

// Create lines joining the points
ori_to_top = newl; Line(ori_to_top) = {ori, top_ori};

top_to_yeast = newl; Line(top_to_yeast) = {top_ori, top_yeast};

top_yeast_to_petri = newl; Line(top_yeast_to_petri) = {top_yeast, top_petri};

top_petri_to_bot = newl; Line(top_petri_to_bot) = {top_petri, bot_petri};

petri_bot_to_yeast = newl; Line(petri_bot_to_yeast) = {bot_petri, bot_yeast};

yeast_bot_to_ori = newl; Line(yeast_bot_to_ori) = {bot_yeast, ori};

// Create a line loop
domain_line_loop = newll;
Line Loop(domain_line_loop) = {ori_to_top, top_to_yeast,
                               top_yeast_to_petri, top_petri_to_bot,
                               petri_bot_to_yeast, yeast_bot_to_ori};

domain_surf = news;
Plane Surface(domain_surf) = {domain_line_loop};

//Create the structured mesh: need to specify the four corners.
Transfinite Surface {domain_surf} = {ori, top_ori, top_petri, bot_petri}; 
Recombine Surface {domain_surf};

// Now rotate and extrude to create the radially symmetric mesh...
Rotate{ {0, 0, 1}, {0, 0, 0}, -(.5*slice_angle/180)*Pi}
{
  Surface{domain_surf};
}

surf_vector[] = Extrude{ {0, 0, 1}, {0, 0, 0}, (slice_angle/180)*Pi}
{
  Surface{domain_surf};
  Layers{1};
  Recombine;
};

Coherence;

Physical Volume("internal") = surf_vector[1];

// NO SPACES ALLOWED, OR EVERYTHING GETS FUCKED UP
Physical Surface("left_wedge") = surf_vector[0];
Physical Surface("right_wedge") = {domain_surf};
Physical Surface("yeast_top") = surf_vector[2];
Physical Surface("top_petri") =  surf_vector[3];
Physical Surface("petri_edge") = surf_vector[4];
Physical Surface("bottom_petri") = surf_vector[5];
Physical Surface("yeast_bottom") = surf_vector[6];

