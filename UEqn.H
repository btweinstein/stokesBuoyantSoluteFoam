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
        solve(UEqn == -fvc::grad(p));
    }
