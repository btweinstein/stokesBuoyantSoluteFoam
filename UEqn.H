    // Solve the momentum equation

    tmp<fvVectorMatrix> tUEqn
    (
	-fvm::laplacian(nu_star, U)
    );
    fvVectorMatrix& UEqn = tUEqn.ref();

    UEqn.relax();

    if (simple.momentumPredictor())
    {
        vector all_U_res = solve
        (
            UEqn
          ==
            fvc::reconstruct
            (
                (
                  - ghf * fvc::snGrad(rhok)
                  - fvc::snGrad(p_rgh)
                )*mesh.magSf()
            )
        );
        U_res_init = all_U_res[0];
	    for(int i=1; i < all_U_res.size(); i++)
	    {
	        double cur_U = all_U_res[i];
	        if (cur_U > U_res_init) U_res_init = cur_U;
	    }
    }
