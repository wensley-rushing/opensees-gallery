## CE 222 Final Project - Jose Yeckle
# Shear analysis of a RC column section

from sectionproperties.analysis import Section
from sectionproperties.pre import Material
from sectionproperties.pre.library import concrete_rectangular_section
import numpy as np
import json
import veux


def create_fibers(mesh, sec):
    fibers = []
    # ASSUMPTION
    T3 = [0, 1, 2]
    vertices = mesh["vertices"]
    for triangle in mesh["triangles"]:
        # Triangle is a list of indices that identify the nodes
        # of a given triangle
        # quad = [
        #     [(1/3, 1/3, 1/3), 1]
        # ]
        quad = [
            [(2/3, 1/6, 1/6), 1/3],
            [(1/6, 2/3, 1/6), 1/3],
            [(1/6, 1/6, 2/3), 1/3]
        ]

        vi = vertices[triangle[T3[1]]] - vertices[triangle[T3[0]]]
        vj = vertices[triangle[T3[2]]] - vertices[triangle[T3[0]]]

        area = np.linalg.norm(np.cross([*vi, 0], [*vj, 0]))/2

        for point, weight in quad:
            # TODO
            B = np.zeros((2, 3))
            fiber = {
                "location": (sum(vertices[triangle[T3]])/3).tolist(),
                "area": area*weight
            }

            omega = [
                # omega
                sum(sec.section_props.omega[triangle[T3]])/3,
                # omega_{,x} and omega_{,y}
                *B@sec.section_props.omega[triangle[T3]]
            ]

            omega = [float(i) for i in omega]

            phi = [0, 0, 0]
            psi = [0, 0, 0]

            fiber["warp"] = [omega, phi, psi]

            fibers.append(fiber)

    return fibers

def render_field(sec, name):
    field = getattr(sec.section_props, name)

    depth = 600
    scale = float((depth/8)/max(field))

    artist = veux.create_artist((
        geom.mesh["vertices"], geom.mesh["triangles"]), ndf=1)
    
    artist.draw_outlines()
    artist.draw_surfaces(state=lambda i: field[i], scale=scale)
    veux.serve(artist)

def create_section(verbose=False):

    # Define the concrete material
    concrete = Material(
        name="Concrete",
        elastic_modulus=30.1e3,
        poissons_ratio=0.2,
        density=2.4e-6,
        yield_strength=32,
        color="lightgrey"
    )

    # Define the steel material
    steel = Material(
        name="Steel",
        elastic_modulus=200e3,
        poissons_ratio=0.3,
        density=7.85e-6,
        yield_strength=500,
        color="grey"
    )

    # Create the geometry
    geom = concrete_rectangular_section(
        d=600,
        b=300,
        dia_top=16,
        area_top=200,
        n_top=3,
        c_top=32,
        dia_bot=20,
        area_bot=310,
        n_bot=3,
        c_bot=42,
        dia_side=12,
        area_side=110,
        n_side=3,
        c_side=57,
        n_circle=16,
        conc_mat=concrete,
        steel_mat=steel
    )
    if verbose:
        ei = sec.get_eic(e_ref=concrete)
        print(ei)
        ea = sec.get_ea(e_ref=concrete)
        print(ea)
        print(f"I_eff = {ei[0]:.3e} mm6")
        print(f"I_rec = {(300 * 600**3 / 12):.3e} mm6")
        ej = sec.get_ej(e_ref=concrete)
        print(f"EJ = {ej:.3e} mm6")

    return geom


if __name__ == "__main__":
    geom = create_section()

    geom.create_mesh(mesh_sizes=[200], coarse=False)
    sec = Section(geometry=geom)


    sec.calculate_geometric_properties()
    sec.calculate_warping_properties()

    fibers = create_fibers(geom.mesh, sec)


    path_to_file = "./mesh.json"
    with open(path_to_file,"w") as file:
        json.dump(fibers,file)

    render_field(sec, "psi_shear")

    # sec.plot_mesh()
