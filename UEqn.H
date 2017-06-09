    // Solve the momentum equation

    tmp<fvVectorMatrix> tUEqn
    (
	-fvm::laplacian(nu_star, U)
    );
    fvVectorMatrix& UEqn = tUEqn.ref();

    UEqn.relax();

    if (simple.momentumPredictor())
    {
        solve
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
    }
