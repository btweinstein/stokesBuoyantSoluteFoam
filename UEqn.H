    // Momentum predictor

    tmp<fvVectorMatrix> tUEqn
    (
	//Pay attention to signs...we need the negative 
	// sign on the laplacian for whatever reason...
	-fvm::laplacian(nu_star, U)
    );

    fvVectorMatrix& UEqn = tUEqn.ref();

    UEqn.relax();

    if (simple.momentumPredictor())
    {	
        vector all_U_res = solve(
	    UEqn 
	    == 
	    fvc::reconstruct((
	      - Ra * ghf * fvc::snGrad(c) 
	      - fvc::snGrad(p)
	    )*mesh.magSf())
	).initialResidual();
	// Get the maximum residual
	U_res_init = all_U_res[0];
	for(int i=1; i < all_U_res.size(); i++)
	{
	    double cur_U = all_U_res[i];
	    if (cur_U > U_res_init) U_res_init = cur_U;
	}
    }
