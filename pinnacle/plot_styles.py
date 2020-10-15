
aesthetics_sp_d = {}
aesthetics_sp_d["color"] = 'blue'
aesthetics_sp_d["linewidth"] = None
aesthetics_sp_d["linestyle"] = None
aesthetics_sp_d["marker"] = 'o'
aesthetics_sp_d["markerfacecolor"] = 'cadetblue'
aesthetics_sp_d["markeredgewidth"] = 1
aesthetics_sp_d["markersize"] = 2
aesthetics_sp_d["markevery"] = 1
aesthetics_sp_d["alpha"] = 0.5

           
aesthetics_sp_cs = {}
aesthetics_sp_cs["color"] = 'black'
aesthetics_sp_cs["linewidth"] = None
aesthetics_sp_cs["linestyle"] = 'None'
aesthetics_sp_cs["marker"] = 'o'
aesthetics_sp_cs["markerfacecolor"] = 'white'
aesthetics_sp_cs["markeredgewidth"] = 1
aesthetics_sp_cs["markersize"] = 3
aesthetics_sp_cs["markevery"] = 1
aesthetics_sp_cs["alpha"] = 0.6

            
aesthetics_qq_cs = {}
aesthetics_qq_cs["color"] = 'slategrey'
aesthetics_qq_cs["linewidth"] = None
aesthetics_qq_cs["linestyle"] = 0
aesthetics_qq_cs["marker"] = 'o'
aesthetics_qq_cs["markerfacecolor"] = 'white'
aesthetics_qq_cs["markeredgewidth"] = 1
aesthetics_qq_cs["markersize"] = 2
aesthetics_qq_cs["markevery"] = 1
aesthetics_qq_cs["alpha"] = 0.3      
               
aesthetics_a_cs = {}
aesthetics_a_cs["color"] = 'slategrey'
aesthetics_a_cs["linewidth"] = None
aesthetics_a_cs["linestyle"] = 'None'
aesthetics_a_cs["marker"] = 'o'
aesthetics_a_cs["markerfacecolor"] = 'white'
aesthetics_a_cs["markeredgewidth"] = 1
aesthetics_a_cs["markersize"] = 1.3
aesthetics_a_cs["markevery"] = 1
aesthetics_a_cs["alpha"] = 0.2      
                                        

def cycling_attrs():

    import itertools as it

    global icolors, imarkers, istyles, iwidths, ifaces, ialpha, imrkevry

    ccolors = ["steelblue"] * 5 + ["peru"] * 5 + ["darkmagenta"] * 5 +\
              ["rebeccapurple"] * 5 + ["crimson"] * 5
    cmarkers = ["o", ".", "o", "x", "D"]
    cstyles = ["-", "-", "--", "--", ":"]
    cwidths = [2, 1, 1, 1, 2]
    cwidths = [3] * 2 + [1] * 7
    cfaces = ccolors[:]
    for i, _ in enumerate(cfaces):
        if i % 5 == 0 or i % 5 == 4:
            cfaces[i] = "white"
    calpha = [1.0] * 5 + [1.0] * 5 + [1.0] * 5
    cmrkevry = [(2, 3), (3, 2), (1, 5)]

    icolors = it.cycle(ccolors)
    imarkers = it.cycle(cmarkers)
    istyles = it.cycle(cstyles)
    iwidths = it.cycle(cwidths)
    ifaces = it.cycle(cfaces)
    ialpha = it.cycle(calpha)
    imrkevry = it.cycle(cmrkevry)


def aes_attrs():

    global icolors, imarkers, istyles, iwidths, ifaces, ialpha, imrkevry

    aesthetics = {}
    aesthetics["color"] = next(icolors)
    aesthetics["linewidth"] = next(iwidths)
    aesthetics["linestyle"] = next(istyles)
    aesthetics["marker"] = next(imarkers)
    aesthetics["markerfacecolor"] = next(ifaces)
    aesthetics["markeredgewidth"] = 1
    aesthetics["markersize"] = 6
    aesthetics["markevery"] = next(imrkevry)
    aesthetics["alpha"] = next(ialpha)  

    return aesthetics
 
