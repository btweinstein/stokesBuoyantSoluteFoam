    // Solve the momentum equation

    tmp<fvVectorMatrix> tUEqn
    (
	    turbulence->divDevReff(U) // MUST BE LAMINAR
    );
    fvVectorMatrix& UEqn = tUEqn.ref();

    UEqn.relax();

    //TODO: Is this always necessary? Will my solution *not* converge if this is
    // not used?
    if (simple.momentumPredictor())
    {
        vector all_U_res = solve
        (
            UEqn
            ==
            fvc::reconstruct(
                (
                  - ghf * fvc::snGrad(rhok)
                  - fvc::snGrad(p_rgh)
                )*mesh.magSf()
            )
        ).initialResidual();
        U_res_init = 0.0;
	    for(int i=0; i < all_U_res.size(); i++)
	    {
	        double cur_U = all_U_res[i];
	        if ((cur_U > U_res_init) && (i != ignore_direction))
	        {
	            U_res_init = cur_U;
	        }
	    }
    }
