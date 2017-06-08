    // Momentum predictor

    tmp<fvVectorMatrix> tUEqn
    (
	-fvm::laplacian(nu, U)
    );

    fvVectorMatrix& UEqn = tUEqn.ref();

    UEqn.relax();

    if (simple.momentumPredictor())
    {
        solve(UEqn == -fvc::grad(p));
    }
