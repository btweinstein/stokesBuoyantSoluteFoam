//**** MAIN FIELDS ****

Info<< "Reading field p_rgh\n" << endl;
volScalarField p_rgh
(
    IOobject
    (
        "p_rgh",
        runTime.timeName(),
        mesh,
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);

Info << "Reading field U\n" << endl;
volVectorField U
(
    IOobject
    (
        "U",
        runTime.timeName(),
        mesh,
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);

Info<< "Reading field c\n" << endl;
volScalarField c
(
    IOobject
    (
        "c",
        runTime.timeName(),
        mesh,
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);

//**** READING IN TRANSPORT PROPERTIES ****

#include "createPhi.H"

singlePhaseTransportModel laminarTransport(U, phi);

dimensionedScalar Ra(
    "Ra",
    dimensionSet(0, 4, -2, 0, -1, 0, 0),
    laminarTransport
);

Info<< "Creating turbulence model\n" << endl;
autoPtr<incompressible::turbulenceModel> turbulence
(
    incompressible::turbulenceModel::New(U, phi, laminarTransport)
);

dimensionedScalar D_star
(
	"D_star",
	dimensionSet(0, 2, -1, 0, 0, 0, 0),
	1.0
);

//**** GRAVITY ****

// In my implementation, gh and ghf are dimensionless! Bad things happen if you don't do this.
Info<< "\nReading direction of gravity" << endl;
IOdictionary ghat_dict
(
    IOobject
    (
        "ghat",
        runTime.constant(),
        mesh,
        IOobject::MUST_READ,
        IOobject::NO_WRITE
    )
);
vector ghat = ghat_dict.lookup("ghat");

volScalarField gh("gh", ghat & mesh.C());
surfaceScalarField ghf("ghf", ghat & mesh.Cf());

volScalarField rhok("rhok", Ra*c); // For consistent notation with bousinesq

//**** PRESSURE (NEED GRAVITY FIRST) ****

Info << "Creating pressure fields...\n" << endl;

volScalarField p // Need gravity in order to deal with P
(
    IOobject
    (
        "p",
        runTime.timeName(),
        mesh,
        IOobject::NO_READ,
        IOobject::AUTO_WRITE
    ),
    p_rgh + rhok*gh
);

label pRefCell = 0;
scalar pRefValue = 0.0;
setRefCell(p, p_rgh, simple.dict(), pRefCell, pRefValue);
mesh.setFluxRequired(p.name());

if (p_rgh.needReference())
{
    p += dimensionedScalar
    (
        "p",
        p.dimensions(),
        pRefValue - getRefCellValue(p, pRefCell)
    );
}

mesh.setFluxRequired(p_rgh.name());


//**** READ THE RESIDUALS, REQUIRED FOR LOOPING SIMPLEFOAM ****


int min_stokes_iter;
int max_stokes_iter;
//Ignoring the residual of U in a certain direction is often required for axisymmetric simulations
int ignore_direction = -1; // 0: ignore x residual, 1: ignore y, 2: ignore z, -1: use U residual in every direction

dictionary simple_dict = mesh.solutionDict().subDict("SIMPLE");

simple_dict.lookup("min_iter") >> min_stokes_iter;
simple_dict.lookup("max_iter") >> max_stokes_iter;
ignore_direction = simple_dict.lookupOrDefault("ignore_direction", -1);

if(ignore_direction != -1){
    if (ignore_direction == 0) Info << "Ignoring Ux residual... \n" << endl;
    if (ignore_direction == 1) Info << "Ignoring Uy residual... \n" << endl;
    if (ignore_direction == 2) Info << "Ignoring Uz residual... \n" << endl;
}

dictionary res_dict = simple_dict.subDict("residualControl");

double p_converged, U_converged;

res_dict.lookup("p_rgh") >> p_converged;
res_dict.lookup("U") >> U_converged;