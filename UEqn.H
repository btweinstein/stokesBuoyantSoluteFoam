    // Momentum predictor

    tmp<fvVectorMatrix> tUEqn
    (
	//Pay attention to signs...we need the negative 
	// sign on the laplacian for whatever reason...
	-fvm::laplacian(nu_star, U) == source
    );

    fvVectorMatrix& UEqn = tUEqn.ref();

    UEqn.relax();

    if (simple.momentumPredictor())
    {	
        vector all_U_res = solve(UEqn == -fvc::grad(p)).initialResidual();
	U_res_init = all_U_res[0];
	for(int i=1; i < all_U_res.size(); i++)
	{
	    double cur_U = all_U_res[i];
	    if (cur_U > U_res_init) U_res_init = cur_U;
	}
    }
